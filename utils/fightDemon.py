from .adb_helper import auto_setup_adb, ADBHelper, get_project_path, StopScriptException, KeyCode
import time
import os
import json
from .goToBossMenu import go_to_boss_menu

# Coordonnées des boutons de difficulté
DIFFICULTY_BUTTONS = {
    "easy": (405, 363),
    "hard": (414, 509),
    "extreme": (414, 658),
    "hell": (405, 813),
}

region_potion = (366, 333, 427, 411)
potion_image_path = get_project_path("img/act.png")
region_menu_demon = (641, 1001, 677, 1030)
menu_demon_image_path = get_project_path("img/menu-demon.png")
region_auto_fight = (753, 20, 780, 45)
auto_fight_image_path = get_project_path("img/auto-fight.png")
region_end_fight_demon = (376, 1001, 424, 1028)
end_fight_demon_image_path = get_project_path("img/end-fight-demon.png")
region_home = (615, 1005, 662, 1041)
home_image_path = get_project_path("img/home.png")
region_diamond = (363, 662, 425, 698)
diamond_image_path = get_project_path("img/diamond.png")

def load_config():
    config_path = get_project_path("config.json")
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Warning: config.json not found at {config_path}")
        return {}
    except json.JSONDecodeError:
        print(f"Warning: Invalid JSON in config.json")
        return {}

def fight_demon(adb, demon_name):
    if adb is None:
        adb = auto_setup_adb(verbose=False)
    
    # Charger la configuration
    config = load_config()
    demon_difficulties = config.get("demon_difficulties", {})
    difficulty_name = demon_difficulties.get(demon_name)
    
    if not difficulty_name:
        print(f"Warning: No difficulty configured for demon '{demon_name}', using 'easy' as default")
        difficulty_name = "easy"
    
    region_difficulty_demon = (603, 356, 635, 394)
    difficulty_demon_image_path = get_project_path("img/difficulty-demon.png")
    
    # ---------------- Savoir si on est dans le menu des démons ----------------
    while True:
        at_difficulty_menu = adb.compare_region_with_image(
            reference_image_path=difficulty_demon_image_path,
            region=region_difficulty_demon,
            threshold=0.9,
        )
        if at_difficulty_menu:
            break
        time.sleep(0.5)

    # ---------------- Cliquer sur le bouton de difficulté selon le démon et la difficulté choisie dans le config.json ----------------
    button_coords = DIFFICULTY_BUTTONS.get(difficulty_name)
    if not button_coords:
        print(f"Error: Unknown difficulty '{difficulty_name}' for demon '{demon_name}'")
        return
    
    print(f"Selecting difficulty: {difficulty_name}")
    adb.tap(button_coords[0], button_coords[1])
    time.sleep(0.5)

    # ---------------- Chercher le ok des affrontements multiples avec plus de 3 demons ----------------
    if adb.is_color_at(
        470, 959,
        target_color=(40, 154, 97),
        tolerance=10
    ):
        print("Start the demon")
        adb.tap(470, 959)
        time.sleep(0.5)

    # ---------------- Chercher le ok des affrontements multiples avec moins de ou = a 3 demons ----------------
    if adb.is_color_at(
    468, 851,
    target_color=(49, 161, 105),
    tolerance=10
    ):
        print("Start the demon")
        adb.tap(468, 851)
        time.sleep(0.5)

    time.sleep(1.5)

    # ---------------- Savoir si on est dans le menu des démons ----------------
    while True:
        in_demon_menu = adb.compare_region_with_image(
            reference_image_path=menu_demon_image_path,
            region=region_menu_demon,
            threshold=0.9,
        )
        if in_demon_menu:
            break
        # ---------------- Savoir si on a plus d'act  ----------------
        no_more_act = adb.compare_region_with_image(
            reference_image_path=potion_image_path,
            region=region_potion,
            threshold=0.9,
        )
        if no_more_act:
            print("No more ACT, refill potions")
            adb.tap(405, 818)
            time.sleep(0.7)
            adb.tap(button_coords[0], button_coords[1])
            time.sleep(0.7)
            # + 3 demons
            if adb.is_color_at(
                468, 851,
                target_color=(49, 161, 105),
                tolerance=10
            ):
                print("Restarting the demon")
                adb.tap(468, 851)
                time.sleep(0.5)
            # - 3 demons
            if adb.is_color_at(
                470, 959,
                target_color=(40, 154, 97),
                tolerance=10
            ):
                print("Restarting the demon")
                adb.tap(470, 959)
                time.sleep(0.5)

        # ---------------- Savoir si on a plus de potions ----------------
        diamond_popup = adb.compare_region_with_image(
            reference_image_path=diamond_image_path,
            region=region_diamond,
            threshold=0.9,
        )
        if diamond_popup:
            raise StopScriptException("No more ACT and no more potions")
        time.sleep(0.5)

    # ---------------- Cliquer sur l'invitation ia allier ----------------
    print("Add IA Friends")
    adb.tap(238, 754)
    time.sleep(2)

    # ---------------- Savoir si on est dans le menu des amis IA avec la couleur ----------------
    while True:
        # Avec histoirique de la IA
        if adb.is_color_at(
            677, 372,
            target_color=(189, 145, 0),
            tolerance=10
        ):
            print("IA Friends added")
            adb.tap(677, 372)
            time.sleep(0.5)
            break

        # Sans historique de la IA
        if adb.is_color_at(
            677, 354,
            target_color=(190, 146, 0),
            tolerance=10
        ):
            print("IA Friends added")
            adb.tap(677, 354)
            time.sleep(0.5)
            break
        time.sleep(0.5)

    # ---------------- Savoir si on est dans le menu des démons ----------------
    while True:
        in_demon_menu = adb.compare_region_with_image(
            reference_image_path=menu_demon_image_path,
            region=region_menu_demon,
            threshold=0.9,
        )
        if in_demon_menu:
            break
        time.sleep(0.5)

    # ---------------- Cliquer sur la preparation du combat ----------------
    print("Combat preparation")
    adb.tap(408, 1000)
    time.sleep(0.8)
    adb.tap(408, 1000)
    time.sleep(0.5)

    # ---------------- Attendre le bouton auto  ----------------
    while True:
        auto_fight_visible = adb.compare_region_with_image(
            reference_image_path=auto_fight_image_path,
            region=region_auto_fight,
            threshold=0.9,
        )
        if auto_fight_visible:
            print("Mode auto")
            adb.tap(712, 26)
            break

        adb.tap(399, 1058)
        time.sleep(0.5)

    # ---------------- Attendre la fin du combat ----------------
    while True:
        demon_fight_finished = adb.compare_region_with_image(
            reference_image_path=end_fight_demon_image_path,
            region=region_end_fight_demon,
            threshold=0.9,
        )
        if demon_fight_finished:
            print("Combat finished")
            adb.tap(402, 1008)
            break

        time.sleep(0.5)
        adb.tap(399, 1058)
        time.sleep(0.5)
        adb.tap(400, 969)
        time.sleep(1)

    # ---------------- Savoir si on est dans la taverne ----------------
    while True:
        at_tavern = adb.compare_region_with_image(
            reference_image_path=home_image_path,
            region=region_home,
            threshold=0.9,
        )
        if at_tavern:
            break
        time.sleep(0.5)

    # ---------------- Cliquer sur le menu combat  ----------------
    time.sleep(5)
    go_to_boss_menu()
    time.sleep(0.5)