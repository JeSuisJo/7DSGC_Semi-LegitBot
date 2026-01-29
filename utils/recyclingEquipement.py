from .adb_helper import auto_setup_adb, ADBHelper, get_project_path, StopScriptException
import time
import os

def recycle_equipement():
    # Configuration automatique de ADB
    adb = auto_setup_adb(verbose=False)
    os.system('cls')
    print("=" * 50)
    print(" Recycling")
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

    # ---------------- Cliquer sur le menu de recylage ----------------
    print("Recycling")
    adb.tap(54, 555)
    time.sleep(0.5)

    # ---------------- Savoir si on est dans un menu ----------------
    while True:
        in_menu = adb.compare_region_with_image(
            reference_image_path=in_menu_image_path,
            region=region_in_menu,
            threshold=0.9
        )
        if in_menu:
            break
        time.sleep(0.5)

    # ---------------- Cliquer sur le menu de configuration de recyclage ----------------
    time.sleep(2)
    print("Configuration recycling")
    adb.tap(180, 1043)

    # ---------------- Check des rareté enregistrer ----------------
    time.sleep(1)
    # ---------------- Check C ----------------
    color_c = adb.get_color_at(
        325, 210,
        target_color=(75, 68, 54),
        tolerance=10,
        )
    if color_c:
        print("Grade C activated")
        adb.tap(325, 210)
    else:
        print("Grade C already activated")
    time.sleep(0.5)

    # ---------------- Check UC ----------------
    color_uc = adb.get_color_at(
        382, 207,
        target_color=(111, 98, 74),
        tolerance=10,
        )
    if color_uc:
        print("Grade UC activated")
        adb.tap(382, 207)
    else:
        print("Grade UC already activated")
    time.sleep(0.5)

    # ---------------- Check R ----------------
    color_r = adb.get_color_at(
        434, 212,
        target_color=(58, 75, 85),
        tolerance=10,
        )
    if color_r:
        print("Grade R activated")
        adb.tap(434, 212)
    else:
        print("Grade R already activated")
    time.sleep(0.5)

    # ---------------- Check SR ----------------
    color_sr = adb.get_color_at(
        494, 214,
        target_color=(34, 18, 12),
        tolerance=10,
        )
    if color_sr:
        print("Grade SR activated")
        adb.tap(494, 214)
    else:
        print("Grade SR already activated")

    time.sleep(0.5)

    # ---------------- Check SSR pour le desactiver ----------------
    color_ssr = adb.get_color_at(
        545, 214,
        target_color=(92, 65, 130),
        tolerance=10,
        )
    if color_ssr:
        print("Grade SSR already deactivated")
    else:
        print("Grade SSR deactivated")
        adb.tap(545, 214)

    time.sleep(0.5)
    # ---------------- Check si le enregistrer est actier ----------------
    color_updrage = adb.get_color_at(
        434, 547,
        target_color= (0, 134, 180),
        tolerance=10
    )
    if color_updrage:
        print("Upgrade items already activated")
    else:
        print("Activated upgrade items")
        adb.tap(434, 547)
    
    time.sleep(0.5)
    # ---------------- Check si la quantité est infini ----------------
    color_how_many = adb.get_color_at(
        596, 723,
        target_color= (1, 106, 142),
        tolerance=10
    )
    if color_how_many:
        print("All items already activated")
    else:
        print("Activated select all items")
        adb.tap(596, 723)

    # ---------------- Enregistrer la config ----------------
    time.sleep(0.5)
    adb.tap(405, 973)
    time.sleep(0.5)

    # ---------------- Savoir si on est dans un menu ----------------
    while True:
        in_menu = adb.compare_region_with_image(
            reference_image_path=in_menu_image_path,
            region=region_in_menu,
            threshold=0.9
        )
        if in_menu:
            break
        time.sleep(0.5)

    # ---------------- Reclyer tous les items  ----------------
    time.sleep(0.7)
    print("Recycling all items")
    adb.tap(396, 1020)
    time.sleep(1)

    # ---------------- Savoir si il y a le ok des haut grade items recycler  ----------------
    color_high_grade = adb.get_color_at(
        562, 625,
        target_color= (29, 148, 91),
        tolerance=10
    )
    if color_high_grade:
        print("High Grade Items for recycling accepted")
        adb.tap(562, 625)
        time.sleep(0.5)

    # ---------------- Savoir si il y a le return ----------------
    time.sleep(2.5)
    while True:
        in_menu = adb.compare_region_with_image(
            reference_image_path=in_menu_image_path,
            region=region_in_menu,
            threshold=0.9
        )
        if in_menu:
            print("All items are recycled")
            break

        color_multi_items_ok = adb.get_color_at(
            472, 1011,
            target_color= (62, 148, 79),
            tolerance=10
        )
        if color_multi_items_ok:
            adb.tap(472, 1011)
            time.sleep(0.5)

        adb.tap(662, 32)
        time.sleep(0.5)

    # ---------------- Retourner en arriere ----------------
    time.sleep(1)
    adb.tap(34, 32)
    time.sleep(0.5)

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