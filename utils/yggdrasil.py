from utils.adb_helper import auto_setup_adb
import time
import os
from utils.adb_helper import get_project_path
from utils.fightDemon import load_config
from utils.battlePreparationTicket import run_battle_preparation_ticket
from utils.battlePreparation import run_battle_preparation

def run_yggdrasil():
    # Configuration automatique de ADB
    adb = auto_setup_adb(verbose=True)
    config = load_config()
    os.system('cls')
    print("=" * 50)
    print(" Daily mode : Yggdrasil 5/8")
    print("=" * 50)


    region_home = (615, 1005, 662, 1041)
    home_image_path = get_project_path("img/home.png")
    region_hub = (562, 345, 617, 402)
    hub_image_path = get_project_path("img/hub.png")
    region_yggdrasil = (375, 38, 426, 82)
    yggdrasil_image_path = get_project_path("img/yggdrasil.png")
    region_yggdrasil_difficulty = (565, 886, 608, 929)
    yggdrasil_difficulty_image_path = get_project_path("img/yggdrasil_difficulty.png")

    # ---------------- Savoir si on est dans la taverne ----------------
    while True:
        is_match, similarity = adb.compare_region_with_image(
            reference_image_path=home_image_path,
            region=region_home,
            threshold=0.9,
        )
        if is_match:
            break
        time.sleep(0.5)
        
    # ---------------- Clique sur le bouton menu combat ----------------
    print("Menu")
    adb.tap(738, 745)
    time.sleep(0.5)

    # ---------------- Savoir si on est dans le menu ----------------
    while True:
        is_match, similarity = adb.compare_region_with_image(
            reference_image_path=hub_image_path,
            region=region_hub,
            threshold=0.9,
        )
        if is_match:
            break
        time.sleep(0.5)

    # ---------------- Cliquer sur le menu Yggdrasil ----------------
    print("Yggdrasil")
    adb.tap(563, 888)
    time.sleep(0.5)

    # ---------------- Savoir si on est dans le menu Yggdrasil ----------------
    while True:
        is_match, similarity = adb.compare_region_with_image(
            reference_image_path=yggdrasil_image_path,
            region=region_yggdrasil,
            threshold=0.9,
        )
        if is_match:
            break
        time.sleep(0.5)

    # ---------------- Cliquer sur le level selon la configuration ----------------
    if config.get("yggdrasil_level") == "blue":
        adb.tap(192, 497)
    elif config.get("yggdrasil_level") == "yellow":
        adb.tap(551, 357)
    elif config.get("yggdrasil_level") == "red":
        adb.tap(568, 748)

    # ---------------- Savoir si on est dans le menu de la difficulté Yggdrasil ----------------
    while True:
        is_match, similarity = adb.compare_region_with_image(
            reference_image_path=yggdrasil_difficulty_image_path,
            region=region_yggdrasil_difficulty,
            threshold=0.9,
        )
        if is_match:
            break
        time.sleep(0.5)

    # ---------------- Cliquer sur la difficulté selon la configuration ----------------
    if config.get("yggdrasil_memory") == "1":
        adb.tap(411, 900)
    elif config.get("yggdrasil_memory") == "2":
        adb.tap(405, 766)
    elif config.get("yggdrasil_memory") == "3":
        adb.tap(405, 625)
    elif config.get("yggdrasil_memory") == "4":
        adb.tap(408, 485)
    elif config.get("yggdrasil_memory") == "5":
        adb.tap(411, 333)

    # ---------------- Faire la preparation du combat selon la configuration ----------------
    if config.get("daily_use_ticket") == "true":
        run_battle_preparation_ticket()
    else:
        run_battle_preparation()

    # ---------------- Savoir si on a fini le niveau ----------------
    while True:
        is_match, similarity = adb.compare_region_with_image(
            reference_image_path=home_image_path,
            region=region_home,
            threshold=0.9,
        )
        if is_match:
            break
        time.sleep(0.5)
        
    # ---------------- Retourner a la taverne ----------------
    print("Return to the tavern")
    adb.tap(148, 1011)
    time.sleep(0.5)