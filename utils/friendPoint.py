from .adb_helper import auto_setup_adb, ADBHelper, get_project_path, StopScriptException
import time
import os

def send_friends_points():
    # Configuration automatique de ADB
    adb = auto_setup_adb(verbose=False)
    os.system('cls')
    print("=" * 50)
    print(" Daily mode : Friends Points 8/8")
    print("=" * 50)
    region_home = (615, 1005, 662, 1041)
    home_image_path = get_project_path("img/home.png")
    region_option = (496, 205, 582, 265)
    option_image_path = get_project_path("img/friends.png")

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

    # ---------------- Aller dans le menu option ----------------
    print("Option")
    adb.tap(644, 1011)
    time.sleep(0.5)

    # ---------------- Savoir si on est dans le menu option ----------------
    while True:
        in_friends_options = adb.compare_region_with_image(
            reference_image_path=option_image_path,
            region=region_option,
            threshold=0.9,
        )
        if in_friends_options:
            break
        time.sleep(0.5)
    
    # ---------------- Cliquer sur les amis ----------------
    print("Friends list")
    adb.tap(563, 234)
    time.sleep(0.5)

    # ---------------- Que l'ont peux plus envoyé les points ----------------
    while not adb.get_color_at(392, 916, target_color=(114, 114, 114), tolerance=10):
        adb.tap(253, 921)
        time.sleep(0.5)

    adb.tap(253, 921)
    print("Friend points sent")

    # ---------------- Retour a la taverne ----------------
    time.sleep(0.5)
    adb.tap(162, 1014)