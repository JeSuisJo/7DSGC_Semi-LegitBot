from . import tap, path, wait_for_image, compare_image
from utils.fightDemon import load_config
import time
import os
from utils.battlePreparationTicket import run_battle_preparation_ticket
from utils.battlePreparation import run_battle_preparation

def run_special_dungeon():
    config = load_config()
    os.system('cls')
    print("=" * 50)
    print(" Daily mode : Special Dungeon 4/8")
    print("=" * 50)

    region_home = (615, 1005, 662, 1041)
    home_image_path = path("img/home.png")
    region_hub = (562, 345, 617, 402)
    hub_image_path = path("img/hub.png")
    region_special_dungeon = (358, 286, 476, 400)
    special_dungeon_image_path = path("img/special_dungeon.png")
    region_event = (473, 358, 560, 414)
    event_image_path = path("img/event.png")
    no_event_image_path = path("img/no-event.png")

    # ---------------- Savoir si on est dans la taverne ----------------
    wait_for_image(home_image_path, region_home, 0.9)

    # ---------------- Clique sur le bouton menu combat ----------------
    print("Menu")
    tap(738, 745)
    time.sleep(0.5)

    # ---------------- Savoir si on est dans le menu ----------------
    wait_for_image(hub_image_path, region_hub, 0.9)

    # ---------------- Cliquer sur le menu Fort Solgales ----------------
    print("Fort Solgales")
    tap(227, 368)
    time.sleep(0.5)

    # ---------------- Savoir si on est dans le menu donjon special ----------------
    wait_for_image(special_dungeon_image_path, region_special_dungeon, 0.9)

    # ---------------- Cliquer sur le menu donjon special ----------------
    print("Special dungeon")
    tap(390, 322)
    time.sleep(0.5)

    while True:
        if compare_image(event_image_path, region_event, 0.9):
            tap(425, 541)
            time.sleep(0.7)
            tap(390, 707)
            time.sleep(0.5)
            break

        if compare_image(no_event_image_path, region_event, 0.9):
            tap(463, 365)
            time.sleep(0.7)
            tap(460, 517)
            time.sleep(0.5)
            break

        time.sleep(0.5)

    # ---------------- Faire la preparation du combat selon la configuration ----------------
    if config.get("daily_use_ticket") == "true":
        run_battle_preparation_ticket()
    else:
        run_battle_preparation()

    # ---------------- Savoir si on a fini le niveau ----------------
    wait_for_image(home_image_path, region_home, 0.9)

    # ---------------- Retourner a la taverne ----------------
    print("Return to the tavern")
    tap(154, 1014)
    time.sleep(0.5)
