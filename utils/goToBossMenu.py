from . import tap, path, wait_for_image
import time
import os

def go_to_boss_menu():
    region_home = (615, 1005, 662, 1041)
    home_image_path = path("img/home.png")
    region_hub = (562, 345, 617, 402)
    hub_image_path = path("img/hub.png")
    region_boss = (121, 268, 163, 304)
    boss_image_path = path("img/boss.png")

    # ---------------- Savoir si on est dans la taverne ----------------
    wait_for_image(home_image_path, region_home, 0.9)

    # ---------------- Clique sur le bouton menu combat ----------------
    print("Menu")
    tap(738, 745)
    time.sleep(0.5)

    # ---------------- Savoir si on est dans le menu ----------------
    wait_for_image(hub_image_path, region_hub, 0.9)

    # ---------------- Cliquer sur le menu boss ----------------
    print("Boss menu")
    tap(227, 494)
    time.sleep(0.5)

    # ---------------- Savoir si on est dans le menu boss ----------------
    wait_for_image(boss_image_path, region_boss, 0.9)
