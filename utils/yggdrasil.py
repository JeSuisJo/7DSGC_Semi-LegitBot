from . import tap, path, wait_for_image
import time
import os
from utils.fightDemon import load_config
from utils.battlePreparationTicket import run_battle_preparation_ticket
from utils.battlePreparation import run_battle_preparation

def run_yggdrasil():
    config = load_config()
    os.system('cls')
    print("=" * 50)
    print(" Daily mode : Yggdrasil 5/8")
    print("=" * 50)

    region_home = (615, 1005, 662, 1041)
    home_image_path = path("img/home.png")
    region_hub = (562, 345, 617, 402)
    hub_image_path = path("img/hub.png")
    region_yggdrasil = (375, 38, 426, 82)
    yggdrasil_image_path = path("img/yggdrasil.png")
    region_yggdrasil_difficulty = (565, 886, 608, 929)
    yggdrasil_difficulty_image_path = path("img/yggdrasil_difficulty.png")

    # ---------------- Savoir si on est dans la taverne ----------------
    wait_for_image(home_image_path, region_home, 0.9)

    # ---------------- Clique sur le bouton menu combat ----------------
    print("Menu")
    tap(738, 745)
    time.sleep(0.5)

    # ---------------- Savoir si on est dans le menu ----------------
    wait_for_image(hub_image_path, region_hub, 0.9)

    # ---------------- Cliquer sur le menu Yggdrasil ----------------
    print("Yggdrasil")
    tap(563, 888)
    time.sleep(0.5)

    # ---------------- Savoir si on est dans le menu Yggdrasil ----------------
    wait_for_image(yggdrasil_image_path, region_yggdrasil, 0.9)

    # ---------------- Cliquer sur le level selon la configuration ----------------
    if config.get("yggdrasil_level") == "blue":
        tap(192, 497)
    elif config.get("yggdrasil_level") == "yellow":
        tap(551, 357)
    elif config.get("yggdrasil_level") == "red":
        tap(568, 748)

    # ---------------- Savoir si on est dans le menu de la difficulté Yggdrasil ----------------
    wait_for_image(yggdrasil_difficulty_image_path, region_yggdrasil_difficulty, 0.9)

    # ---------------- Cliquer sur la difficulté selon la configuration ----------------
    if config.get("yggdrasil_memory") == "1":
        tap(411, 900)
    elif config.get("yggdrasil_memory") == "2":
        tap(405, 766)
    elif config.get("yggdrasil_memory") == "3":
        tap(405, 625)
    elif config.get("yggdrasil_memory") == "4":
        tap(408, 485)
    elif config.get("yggdrasil_memory") == "5":
        tap(411, 333)

    # ---------------- Faire la preparation du combat selon la configuration ----------------
    if config.get("daily_use_ticket") == "true":
        run_battle_preparation_ticket()
    else:
        run_battle_preparation()

    # ---------------- Savoir si on a fini le niveau ----------------
    wait_for_image(home_image_path, region_home, 0.9)

    # ---------------- Retourner a la taverne ----------------
    print("Return to the tavern")
    tap(148, 1011)
