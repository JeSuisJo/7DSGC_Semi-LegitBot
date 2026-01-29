from .adb_helper import auto_setup_adb, ADBHelper, get_project_path, StopScriptException
import time
import os

def food_preparation():
    # Configuration automatique de ADB
    adb = auto_setup_adb(verbose=False)
    os.system('cls')
    print("=" * 50)
    print(" Daily mode : Food preparation 2/8")
    print("=" * 50)
    region_home = (615, 1005, 662, 1041)
    home_image_path = get_project_path("img/home.png")
    region_in_menu = (4, 9, 60, 62)
    in_menu_image_path = get_project_path("img/return.png")

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

    # ---------------- Cliquer sur le menu deroulant ----------------
    adb.tap(57, 894)
    time.sleep(0.8)

    # ---------------- Cliquer sur le bouton de food ----------------
    print("")
    adb.tap(57, 737)
    time.sleep(0.8)

    # ---------------- Savoir si on est dans un menu ----------------
    while True:
        in_menu = adb.compare_region_with_image(
            reference_image_path=in_menu_image_path,
            region=region_in_menu,
            threshold=0.9,
        )
        if in_menu:
            break
        time.sleep(0.5)

    # ---------------- Cliquer sur le menu cuisine ----------------
    print("Recipe menu")
    time.sleep(2)
    adb.tap(75, 1002)

    # ---------------- Prendre la premiere bouffe a craft ----------------
    while True:
        if adb.is_color_at(
            604, 504,
            target_color=(186, 128, 12),
            tolerance=10
        ):
            print("First recipe")
            adb.tap(604, 504)
            time.sleep(0.5)
            break
        time.sleep(0.5)

    # ---------------- Cliquer sur la cuisiner le plat ----------------
    time.sleep(1)
    adb.tap(405, 1008)

    # ---------------- Attendre soit que ce soit fini ----------------
    while True:
        # ---------------- Plus de bouffe a craft 
        if adb.is_color_at(
            570, 969,
            target_color=(108, 108, 108),
            tolerance=10
        ):
            print("Food cook finished")
            time.sleep(0.5)
            break

        # ---------------- Encore de la bouffe a craft 
        if adb.is_color_at(
            570, 969,
            target_color=(231, 163,  20),
            tolerance=10
        ):
            print("Food cook finished")
            time.sleep(0.5)
            break

        time.sleep(0.5)

    # ---------------- Retourne au lobby ----------------
    time.sleep(1)
    adb.tap(40, 32)
    time.sleep(3)
    adb.tap(40, 32)

    # ---------------- Savoir si on est dans un menu ----------------
    while True:
        in_menu = adb.compare_region_with_image(
            reference_image_path=in_menu_image_path,
            region=region_in_menu,
            threshold=0.9,
        )
        if in_menu:
            break
        time.sleep(0.5)
