from utils.adb_helper import auto_setup_adb
from utils.fightDemon import load_config
import time
import os
from utils.adb_helper import get_project_path
from utils.battlePreparationTicket import run_battle_preparation_ticket
from utils.battlePreparation import run_battle_preparation

def run_special_dungeon():
    # Configuration automatique de ADB
    adb = auto_setup_adb(verbose=True)
    config = load_config()
    os.system('cls')
    print("=" * 50)
    print(" Daily mode : Special Dungeon 4/8")
    print("=" * 50)

    region_home = (615, 1005, 662, 1041)
    home_image_path = get_project_path("img/home.png")
    region_hub = (562, 345, 617, 402)
    hub_image_path = get_project_path("img/hub.png")
    region_special_dungeon = (358, 286, 476, 400)
    special_dungeon_image_path = get_project_path("img/special_dungeon.png")
    region_event = (473, 358, 560, 414)
    event_image_path = get_project_path("img/event.png")

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

    # ---------------- Cliquer sur le menu Fort Solgales ----------------
    print("Fort Solgales")
    adb.tap(227, 368)
    time.sleep(0.5)

    # ---------------- Savoir si on est dans le menu donjon special ----------------
    while True:
        is_match, similarity = adb.compare_region_with_image(
            reference_image_path=special_dungeon_image_path,
            region=region_special_dungeon,
            threshold=0.9,
        )
        if is_match:
            break
        time.sleep(0.5)

    # ---------------- Cliquer sur le menu donjon special ----------------
    print("Special dungeon")
    adb.tap(390, 322)
    time.sleep(0.5)

    # ---------------- Savoir si il y a un event en premier ----------------
    while True:
        is_match, similarity = adb.compare_region_with_image(
            reference_image_path=event_image_path,
            region=region_event,
            threshold=0.9,
        )
        if is_match:
            adb.tap(425, 541)
            time.sleep(0.7)
            adb.tap(390, 707)
            time.sleep(0.5)
            break
        time.sleep(0.5)

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
    adb.tap(154, 1014)
    time.sleep(0.5)