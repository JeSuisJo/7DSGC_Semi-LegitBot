from . import tap, path, stop, wait_for_image, is_color, compare_image
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
potion_image_path = path("img/act.png")
region_menu_demon = (641, 1001, 677, 1030)
menu_demon_image_path = path("img/menu-demon.png")
region_auto_fight = (753, 20, 780, 45)
auto_fight_image_path = path("img/auto-fight.png")
region_end_fight_demon = (376, 1001, 424, 1028)
end_fight_demon_image_path = path("img/end-fight-demon.png")
region_home = (615, 1005, 662, 1041)
home_image_path = path("img/home.png")
region_diamond = (363, 662, 425, 698)
diamond_image_path = path("img/diamond.png")

def load_config():
    config_path = path("config.json")
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Warning: config.json not found at {config_path}")
        return {}
    except json.JSONDecodeError:
        print(f"Warning: Invalid JSON in config.json")
        return {}

def fight_demon(demon_name):
    config = load_config()
    demon_difficulties = config.get("demon_difficulties", {})
    difficulty_name = demon_difficulties.get(demon_name)

    if not difficulty_name:
        print(f"Warning: No difficulty configured for demon '{demon_name}', using 'easy' as default")
        difficulty_name = "easy"

    region_difficulty_demon = (603, 356, 635, 394)
    difficulty_demon_image_path = path("img/difficulty-demon.png")

    # ---------------- Savoir si on est dans le menu des démons ----------------
    wait_for_image(difficulty_demon_image_path, region_difficulty_demon, 0.9)

    # ---------------- Cliquer sur le bouton de difficulté selon le démon et la difficulté choisie dans le config.json ----------------
    button_coords = DIFFICULTY_BUTTONS.get(difficulty_name)
    if not button_coords:
        print(f"Error: Unknown difficulty '{difficulty_name}' for demon '{demon_name}'")
        return

    print(f"Selecting difficulty: {difficulty_name}")
    tap(button_coords[0], button_coords[1])
    time.sleep(0.5)

    # ---------------- Chercher le ok des affrontements multiples avec plus de 3 demons ----------------
    if is_color(470, 959, (40, 154, 97), 10):
        print("Start the demon")
        tap(470, 959)
        time.sleep(0.5)

    # ---------------- Chercher le ok des affrontements multiples avec moins de ou = a 3 demons ----------------
    if is_color(468, 851, (49, 161, 105), 10):
        print("Start the demon")
        tap(468, 851)
        time.sleep(0.5)

    time.sleep(1.5)

    # ---------------- Savoir si on est dans le menu des démons ----------------
    while True:
        if compare_image(menu_demon_image_path, region_menu_demon, 0.9):
            break
        # ---------------- Savoir si on a plus d'act  ----------------
        if compare_image(potion_image_path, region_potion, 0.9):
            print("No more ACT, refill potions")
            tap(405, 818)
            time.sleep(0.7)
            tap(button_coords[0], button_coords[1])
            time.sleep(0.7)
            if is_color(468, 851, (49, 161, 105), 10):
                print("Restarting the demon")
                tap(468, 851)
                time.sleep(0.5)
            if is_color(470, 959, (40, 154, 97), 10):
                print("Restarting the demon")
                tap(470, 959)
                time.sleep(0.5)

        # ---------------- Savoir si on a plus de potions ----------------
        if compare_image(diamond_image_path, region_diamond, 0.9):
            stop("No more ACT and no more potions")
        time.sleep(0.5)

    # ---------------- Cliquer sur l'invitation ia allier ----------------
    print("Add IA Friends")
    tap(238, 754)
    time.sleep(2)

    # ---------------- Savoir si on est dans le menu des amis IA avec la couleur ----------------
    while True:
        if is_color(677, 372, (189, 145, 0), 10):
            print("IA Friends added")
            tap(677, 372)
            time.sleep(0.5)
            break
        if is_color(677, 354, (190, 146, 0), 10):
            print("IA Friends added")
            tap(677, 354)
            time.sleep(0.5)
            break
        time.sleep(0.5)

    # ---------------- Savoir si on est dans le menu des démons ----------------
    wait_for_image(menu_demon_image_path, region_menu_demon, 0.9)

    # ---------------- Cliquer sur la preparation du combat ----------------
    print("Combat preparation")
    tap(408, 1000)
    time.sleep(0.8)
    tap(408, 1000)
    time.sleep(0.5)

    # ---------------- Attendre le bouton auto  ----------------
    while True:
        if compare_image(auto_fight_image_path, region_auto_fight, 0.9):
            print("Mode auto")
            tap(712, 26)
            break
        tap(399, 1058)
        time.sleep(0.5)

    # ---------------- Attendre la fin du combat ----------------
    while True:
        if compare_image(end_fight_demon_image_path, region_end_fight_demon, 0.9):
            print("Combat finished")
            tap(402, 1008)
            break
        time.sleep(0.5)
        tap(399, 1058)
        time.sleep(0.5)
        tap(400, 969)
        time.sleep(1)

    # ---------------- Savoir si on est dans la taverne ----------------
    wait_for_image(home_image_path, region_home, 0.9)

    # ---------------- Cliquer sur le menu combat  ----------------
    time.sleep(5)
    go_to_boss_menu()
    time.sleep(0.5)
