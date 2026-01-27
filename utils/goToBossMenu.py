from utils.adb_helper import auto_setup_adb, get_project_path
import time
import os

def go_to_boss_menu():
    # Configuration automatique de ADB
    adb = auto_setup_adb(verbose=False)
    region_home = (615, 1005, 662, 1041)
    home_image_path = get_project_path("img/home.png")
    region_hub = (562, 345, 617, 402)
    hub_image_path = get_project_path("img/hub.png")
    region_boss = (121, 268, 163, 304)
    boss_image_path = get_project_path("img/boss.png")

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
    
    # ---------------- Cliquer sur le menu boss ----------------
    print("Boss menu")
    adb.tap(227, 494)
    time.sleep(0.5)

    # ---------------- Savoir si on est dans le menu boss ----------------
    while True:
        is_match, similarity = adb.compare_region_with_image(
            reference_image_path=boss_image_path,
            region=region_boss,
            threshold=0.9,
        )
        if is_match:
            break
        time.sleep(0.5)
