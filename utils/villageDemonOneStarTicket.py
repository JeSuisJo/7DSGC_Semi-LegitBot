from utils.adb_helper import auto_setup_adb, StopScriptException, get_project_path
import time
import os

region_home = (615, 1005, 662, 1041)
home_image_path = get_project_path("img/home.png")

def village_demon_one_star_ticket():
    # Configuration automatique de ADB
    adb = auto_setup_adb(verbose=True)
    os.system('cls')
    print("=" * 50)
    print(" Auto demon farm mode")
    print("=" * 50)

    # ---------------- Savoir si le achevement multiple est activé ----------------
    if adb.is_color_at(
        648, 262,
        target_color=(114, 91, 58),
        tolerance=10
    ):
        print("Activated achievement auto")
        adb.tap(648, 262)
        time.sleep(0.5)

    # ---------------- Cliquer sur le les demons 1 etoile ----------------
    adb.tap(241, 363)
    time.sleep(1)

    # ---------------- Check les 6 villages si il y a l'achevement multiple activé dessus ----------------
    # Village 1
    if adb.is_color_at(
        200, 414,
        target_color=(235, 204, 49),
        tolerance=10
    ):
        time.sleep(0.5)
    else:
        print("Activated achievement auto")
        adb.tap(200, 414)
        time.sleep(0.5)

    # Village 2
    if adb.is_color_at(
        395, 414,
        target_color=(233, 200, 45),
        tolerance=10
    ):
        time.sleep(0.5)
    else:
        print("Activated achievement auto")
        adb.tap(395, 414)
        time.sleep(0.5)

    # Village 3
    if adb.is_color_at(
        588, 414,
        target_color=(236, 205, 51),
        tolerance=10
    ):
        time.sleep(0.5)
    else:
        print("Activated achievement auto")
        adb.tap(588, 414)
        time.sleep(0.5)

    # Village 4
    if adb.is_color_at(
        201, 578,
        target_color=(251, 239, 79),
        tolerance=10
    ):
        time.sleep(0.5)
    else:
        print("Activated achievement auto")
        adb.tap(201, 578)
        time.sleep(0.5)

    # Village 5
    if adb.is_color_at(
        395, 579,
        target_color=(241, 215, 58),
        tolerance=10
    ):
        time.sleep(0.5)
    else:
        print("Activated achievement auto")
        adb.tap(395, 579)
        time.sleep(0.5)

    # Village 6
    if adb.is_color_at(
        590, 579,
        target_color=(241, 217, 61),
        tolerance=10
    ):
        time.sleep(0.5)
    else:
        print("Activated achievement auto")
        adb.tap(590, 579)
        time.sleep(0.5)

    # ---------------- Faire l'achevement auto ----------------
    print("Clear all 6 villages")
    adb.tap(402, 894)
    time.sleep(2)

    # ---------------- Savoir si on a plus de potions  ----------------
    at_tavern = adb.compare_region_with_image(
        reference_image_path=home_image_path,
        region=region_home,
        threshold=0.9,
    )
    if at_tavern:
        raise StopScriptException("No more ACT and no more potions")

    # ---------------- Attendre la fin du clear ----------------
    while True:
        if adb.is_color_at(
            455, 959,
            target_color=(46, 167, 113),
            tolerance=10
        ):
            print("Clear finished")
            adb.tap(455, 959)
            time.sleep(0.5)
            break
        time.sleep(0.5)
