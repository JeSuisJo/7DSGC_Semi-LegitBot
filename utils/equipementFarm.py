from .adb_helper import auto_setup_adb, ADBHelper, get_project_path, StopScriptException, KeyCode
from utils.battlePreparationEquipement import run_battle_preparation_equipement
from utils.battlePreparationEquipementAuto import battle_preparation_equipement_auto
from utils.fightPve import fight_pve
import time
import os

def equipement_farm():
    # Configuration automatique de ADB
    adb = auto_setup_adb(verbose=False)
    
    region_home = (615, 1005, 662, 1041)
    home_image_path = get_project_path("img/home.png")
    region_hub = (562, 345, 617, 402)
    hub_image_path = get_project_path("img/hub.png")
    region_equipement = (175, 788, 228, 834)
    equipement_image_path = get_project_path("img/equipement.png")
    region_difficulty = (604, 357, 635, 390)
    difficulty_image_path = get_project_path("img/difficulty.png")

    # ---------------- Choix entre set ou équipement ----------------
    print("What do you want to farm?")
    print("1 : Equipment")
    print("2 : Set")
    
    while True:
        try:
            farm_type_choice = input("Your choice (1-2): ").strip()
            farm_type = int(farm_type_choice)
            if farm_type == 1 or farm_type == 2:
                break
            else:
                print("Please enter 1 or 2")
        except ValueError:
            print("Please enter a valid number")
    
    # ---------------- Choix du nombre selon le type ----------------
    if farm_type == 1:
        # Farmer des équipements
        while True:
            try:
                num_equipements = int(input("How many equipments do you want to farm? ").strip())
                if num_equipements >= 1:
                    loop_farm = num_equipements
                    break
                else:
                    print("Please enter a number greater or equal to 1")
            except ValueError:
                print("Please enter a valid number")
    else:
        # Farmer des sets
        while True:
            try:
                num_sets = int(input("How many sets do you want to farm? ").strip())
                if num_sets >= 1:
                    loop_farm = num_sets * 5
                    print(f"{num_sets} set(s) to farm")
                    break
                else:
                    print("Please enter a number greater or equal to 1")
            except ValueError:
                print("Please enter a valid number")

    # ---------------- Choix du type d'équipement à farmer ----------------
    print("Choice of the equipment to farm:")
    print("1 : Attack")
    print("2 : Defence")
    print("3 : HP")
    print("4 : Crit Chance")
    print("5 : Crit Resistance")
    print("6 : Recovery Rate")
    
    while True:
        try:
            choice = input("Your choice (1-6): ").strip()
            equipement_type = int(choice)
            if 1 <= equipement_type <= 6:
                break
            else:
                print("Please enter a number between 1 and 6")
        except ValueError:
            print("Please enter a valid number")
    
    equipement_names = {
        1: "Attack",
        2: "Defence",
        3: "HP",
        4: "Crit Chance",
        5: "Crit Resistance",
        6: "Recovery Rate"
    }
    
    print(f"Selected equipment: {equipement_names[equipement_type]}\n")

    # ---------------- Boucle de farm ----------------
    for i in range(1, loop_farm + 1):
        os.system('cls')
        print("=" * 50)
        print(f"Equipment farm {i} of {loop_farm}")
        print("=" * 50)
        # ---------------- Savoir si on est dans la taverne ----------------
        while True:
            at_tavern = adb.compare_region_with_image(
                reference_image_path=home_image_path,
                region=region_home,
                threshold=0.9,
            )
            if at_tavern:
                break
            adb.tap(127, 24)
            time.sleep(0.5)

        # ---------------- Clique sur le bouton menu combat ----------------
        print("Menu")
        adb.tap(738, 745)
        time.sleep(0.5)

        # ---------------- Savoir si on est dans le menu ----------------
        while True:
            in_hub = adb.compare_region_with_image(
                reference_image_path=hub_image_path,
                region=region_hub,
                threshold=0.9,
            )
            if in_hub:
                break
            time.sleep(0.5)

        # ---------------- Swipe vers le bas pour aller vers le menu des equipements  ----------------
        adb.swipe(402, 839, 402, 576, 300)
        time.sleep(0.8)

        # ---------------- Clique sur le bouton equipements ----------------
        print("Equipment")
        adb.tap(250, 815)
        time.sleep(0.5)

        # ---------------- Savoir si on est dans le menu des equipements ----------------
        while True:
            in_equipment_menu = adb.compare_region_with_image(
                reference_image_path=equipement_image_path,
                region=region_equipement,
                threshold=0.8,
            )
            if in_equipment_menu:
                break
            time.sleep(0.5)

        # ---------------- Clique sur l'equipement a farm selon le choix de l'utilisateur ----------------
        if equipement_type == 1:
            print("Attack")
            adb.tap(200, 588)
        elif equipement_type == 2:
            print("Defence")
            adb.tap(335, 590)
        elif equipement_type == 3:
            print("HP")
            adb.tap(466, 585)
        elif equipement_type == 4:
            print("Crit Chance")
            adb.tap(601, 590)
        elif equipement_type == 5:
            print("Crit Resistance")
            adb.tap(203, 798)
        elif equipement_type == 6:
            print("Recovery Rate")
            adb.tap(329, 807)

        time.sleep(0.5)

        # ---------------- Clique sur le de lancement de la mission selon la couleur trouvée ----------------
        while True:
            mission_color = adb.get_color_at(639, 503)

            if ADBHelper.color_matches(mission_color, (0, 124, 130), tolerance=10):
                print("Start mission")
                adb.tap(586, 485)
                time.sleep(0.7)
                adb.tap(586, 485)
                break
            elif ADBHelper.color_matches(mission_color, (216, 150, 16), tolerance=10):
                print("Go to quest")
                adb.tap(586, 485)
                break
            elif ADBHelper.color_matches(mission_color, (33, 154, 98), tolerance=10):
                print("Finish mission")
                adb.tap(586, 485)
                time.sleep(1.5)
                adb.tap(399, 132)
                time.sleep(1)
                adb.tap(399, 719)
                time.sleep(1)
                adb.tap(586, 485)
                break

            time.sleep(0.5)

        # ---------------- Savoir si on est dans le choix de la difficulté de la mission ----------------
        while True:
            at_difficulty_menu = adb.compare_region_with_image(
                reference_image_path=difficulty_image_path,
                region=region_difficulty,
                threshold=0.9,
            )
            if at_difficulty_menu:
                break
            time.sleep(0.5)

        # ---------------- Cliquer sur la derniere difficulté ----------------
        print("Last difficulty")
        adb.tap(408, 661)
        time.sleep(0.5)

        # ---------------- Faire le battle preparation si la boucle est a 1  ----------------
        if i == 1:
            run_battle_preparation_equipement()
            time.sleep(0.5)

        # ---------------- Faire le battle preparation ticket si la boucle est a plus de 1  ----------------
        if i > 1:
            battle_preparation_equipement_auto()
            time.sleep(0.5)

        # ---------------- Faire le fight PVE  ----------------
        fight_pve()
        time.sleep(0.5)

        # ---------------- Savoir si on a fini le niveau ----------------
        while True:
            level_finished = adb.compare_region_with_image(
                reference_image_path=difficulty_image_path,
                region=region_difficulty,
                threshold=0.9,
            )
            if level_finished:
                break
            adb.tap(127, 24)
            time.sleep(0.5)

        # ---------------- Retour a la taverne  ----------------
        print("Return to the tavern")
        adb.tap(148, 1011)
        time.sleep(0.5)



    