from .adb_helper import auto_setup_adb, ADBHelper, get_project_path, StopScriptException, KeyCode
from .fightDemon import load_config
import time
import os

def collect_beer():
    # Configuration automatique de ADB
    adb = auto_setup_adb(verbose=False)
    config = load_config()
    salon_design = config.get("salon_design")
    region_in_menu = (4, 9, 60, 62)
    in_menu_image_path = get_project_path("img/return.png")
    region_home = (615, 1005, 662, 1041)
    home_image_path = get_project_path("img/home.png")

    os.system('cls')
    print("=" * 50)
    print(" Daily mode : Collect Beer 1/8")
    print("=" * 50)
    
    # ---------------- Si on est dans le salon de la saison 1 ----------------
    if salon_design == "1":
        # ---------------- Savoir si on est a la taverne ----------------
        while True:
            is_match, similarity = adb.compare_region_with_image(
                reference_image_path=home_image_path,
                region=region_home,
                threshold=0.9
            )

            if is_match:
                break
            time.sleep(0.5)

        # ---------------- Clique sur le menu deroulant ----------------
        print("Going to the beer")
        adb.tap(54, 894)
        time.sleep(1)

        # ---------------- Clique sur l'onget de recyclement d'artefacts ----------------*
        adb.tap(60, 558)
        time.sleep(0.5)

        # ---------------- Savoir si on est dans un menu ----------------
        while True:
            is_match, similarity = adb.compare_region_with_image(
                reference_image_path=in_menu_image_path,
                region=region_in_menu,
                threshold=0.9
            )
            if is_match:
                break
            time.sleep(0.5)

        # ---------------- Retourner en arriere ----------------
        time.sleep(1)
        adb.tap(37, 29)
        time.sleep(1)

        # ---------------- Clique sur la bierre ----------------
        adb.tap(110, 392)
        time.sleep(1)

        # ---------------- Savoir si le beer est fini de collecter ----------------
        while True:
            is_match, similarity = adb.compare_region_with_image(
                reference_image_path=home_image_path,
                region=region_home,
                threshold=0.9
            )
            if is_match:
                print("Beer collected")
                break
            adb.tap(387, 120)
            time.sleep(0.5)

    # ---------------- Si on est dans le salon de la saison 3 ----------------
    elif salon_design == "2":
        # ---------------- Savoir si on est a la taverne ----------------
        while True:
            is_match, similarity = adb.compare_region_with_image(
                reference_image_path=home_image_path,
                region=region_home,
                threshold=0.9
            )

            if is_match:
                break
            time.sleep(0.5)

        # ---------------- Clique sur le menu deroulant ----------------
        print("Going to the beer")
        adb.tap(54, 894)
        time.sleep(1)

        # ---------------- Clique sur l'onget cusine ----------------
        adb.tap(54, 731)
        time.sleep(0.5)

        # ---------------- Savoir si on est dans un menu ----------------
        while True:
            is_match, similarity = adb.compare_region_with_image(
                reference_image_path=in_menu_image_path,
                region=region_in_menu,
                threshold=0.9
            )
            if is_match:
                break
            time.sleep(0.5)

        # ---------------- Retourner en arriere ----------------
        time.sleep(2)
        adb.tap(37, 29)
        time.sleep(0.5)

        # ---------------- Aller vers la bierre ----------------
        adb.swipe(408, 693, 43, 693, 800)
        time.sleep(0.5)

        # ---------------- Clique sur la bierre ----------------
        adb.tap(276, 336)
        time.sleep(0.2)
        adb.tap(335, 336)
        time.sleep(0.5)

        # ---------------- Savoir si le beer est fini de collecter ----------------
        while True:
            is_match, similarity = adb.compare_region_with_image(
                reference_image_path=home_image_path,
                region=region_home,
                threshold=0.9
            )
            if is_match:
                print("Beer collected")
                break
            adb.tap(387, 120)
            time.sleep(0.5)


    # ---------------- Si on est dans le salon de l'anime 4KOA ----------------
    elif salon_design == "3":
        # ---------------- Savoir si on est a la taverne ----------------
        while True:
            is_match, similarity = adb.compare_region_with_image(
                reference_image_path=home_image_path,
                region=region_home,
                threshold=0.9
            )

            if is_match:
                break
            time.sleep(0.5)

        # ---------------- Clique sur le menu deroulant ----------------
        print("Going to the beer")
        adb.tap(54, 894)
        time.sleep(1)

        # ---------------- Clique sur l'onget de modification de taverne ----------------
        adb.tap(57, 322)
        time.sleep(0.5)

        # ---------------- Savoir si on est dans un menu ----------------
        while True:
            is_match, similarity = adb.compare_region_with_image(
                reference_image_path=in_menu_image_path,
                region=region_in_menu,
                threshold=0.9
            )
            if is_match:
                break
            time.sleep(0.5)

        # ---------------- Retourner en arriere ----------------
        time.sleep(1)
        adb.tap(37, 29)
        time.sleep(0.5)

        # ---------------- Aller vers la bierre ----------------
        adb.swipe(422, 652, 16, 652, 1000)
        time.sleep(1)

        # ---------------- Collecter la bierre ----------------
        print("Collecting beer")
        adb.tap(212, 503)
        time.sleep(1)

        # ---------------- Savoir si le beer est fini de collecter ----------------
        while True:
            is_match, similarity = adb.compare_region_with_image(
                reference_image_path=home_image_path,
                region=region_home,
                threshold=0.9
            )
            if is_match:
                print("Beer collected")
                break
            adb.tap(387, 120)
            time.sleep(0.5)






