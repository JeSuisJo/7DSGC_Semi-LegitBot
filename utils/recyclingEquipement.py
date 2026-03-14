from . import tap, path, wait_for_image, is_color, compare_image
import time
import os

def recycle_equipement():
    os.system('cls')
    print("=" * 50)
    print(" Recycling")
    print("=" * 50)
    region_home = (615, 1005, 662, 1041)
    home_image_path = path("img/home.png")
    region_in_menu = (4, 9, 60, 62)
    in_menu_image_path = path("img/return.png")

    # ---------------- Savoir si on est dans la taverne ----------------
    wait_for_image(home_image_path, region_home, 0.9)

    # ---------------- Cliquer sur le menu deroulant ----------------
    tap(57, 894)
    time.sleep(0.8)

    # ---------------- Cliquer sur le menu de recylage ----------------
    print("Recycling")
    tap(54, 555)
    time.sleep(0.5)

    # ---------------- Savoir si on est dans un menu ----------------
    wait_for_image(in_menu_image_path, region_in_menu, 0.9)

    # ---------------- Cliquer sur le menu de configuration de recyclage ----------------
    time.sleep(2)
    print("Configuration recycling")
    tap(180, 1043)

    # ---------------- Check des rareté enregistrer ----------------
    time.sleep(1)
    # ---------------- Check C ----------------
    if is_color(325, 210, (75, 68, 54), 10):
        print("Grade C activated")
        tap(325, 210)
    else:
        print("Grade C already activated")
    time.sleep(0.5)

    # ---------------- Check UC ----------------
    if is_color(382, 207, (111, 98, 74), 10):
        print("Grade UC activated")
        tap(382, 207)
    else:
        print("Grade UC already activated")
    time.sleep(0.5)

    # ---------------- Check R ----------------
    if is_color(434, 212, (58, 75, 85), 10):
        print("Grade R activated")
        tap(434, 212)
    else:
        print("Grade R already activated")
    time.sleep(0.5)

    # ---------------- Check SR ----------------
    if is_color(494, 214, (34, 18, 12), 10):
        print("Grade SR activated")
        tap(494, 214)
    else:
        print("Grade SR already activated")
    time.sleep(0.5)

    # ---------------- Check SSR pour le desactiver ----------------
    if is_color(545, 214, (92, 65, 130), 10):
        print("Grade SSR already deactivated")
    else:
        print("Grade SSR deactivated")
        tap(545, 214)
    time.sleep(0.5)

    # ---------------- Check si le enregistrer est actier ----------------
    if is_color(434, 547, (0, 134, 180), 10):
        print("Upgrade items already activated")
    else:
        print("Activated upgrade items")
        tap(434, 547)

    time.sleep(0.5)
    # ---------------- Check si la quantité est infini ----------------
    if is_color(596, 723, (1, 106, 142), 10):
        print("All items already activated")
    else:
        print("Activated select all items")
        tap(596, 723)

    # ---------------- Enregistrer la config ----------------
    time.sleep(0.5)
    tap(405, 973)
    time.sleep(0.5)

    # ---------------- Savoir si on est dans un menu ----------------
    while True:
        if compare_image(in_menu_image_path, region_in_menu, 0.9):
            break
        time.sleep(0.5)

    # ---------------- Reclyer tous les items  ----------------
    time.sleep(0.7)
    print("Recycling all items")
    tap(396, 1020)
    time.sleep(1)

    # ---------------- Savoir si il y a le ok des haut grade items recycler  ----------------
    if is_color(562, 625, (29, 148, 91), 10):
        print("High Grade Items for recycling accepted")
        tap(562, 625)
        time.sleep(0.5)

    # ---------------- Savoir si il y a le return ----------------
    time.sleep(2.5)
    while True:
        if compare_image(in_menu_image_path, region_in_menu, 0.9):
            print("All items are recycled")
            break

        if is_color(472, 1011, (62, 148, 79), 10):
            tap(472, 1011)
            time.sleep(0.5)

        tap(662, 32)
        time.sleep(0.5)

    # ---------------- Retourner en arriere ----------------
    time.sleep(1)
    tap(34, 32)
    time.sleep(0.5)

    # ---------------- Savoir si on est dans la taverne ----------------
    while True:
        if compare_image(home_image_path, region_home, 0.9):
            break
        time.sleep(0.5)
