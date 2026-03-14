from . import tap, path, wait_for_image, wait_for_color, is_color
import time
import os

def food_preparation():
    os.system('cls')
    print("=" * 50)
    print(" Daily mode : Food preparation 2/8")
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

    # ---------------- Cliquer sur le bouton de food ----------------
    print("")
    tap(57, 737)
    time.sleep(0.8)

    # ---------------- Savoir si on est dans un menu ----------------
    wait_for_image(in_menu_image_path, region_in_menu, 0.9)

    # ---------------- Cliquer sur le menu cuisine ----------------
    print("Recipe menu")
    time.sleep(2)
    tap(75, 1002)

    # ---------------- Prendre la premiere bouffe a craft ----------------
    wait_for_color(604, 504, (186, 128, 12), 10)
    print("First recipe")
    tap(604, 504)
    time.sleep(0.5)

    # ---------------- Cliquer sur la cuisiner le plat ----------------
    time.sleep(1)
    tap(405, 1008)

    # ---------------- Attendre soit que ce soit fini ----------------
    while True:
        # ---------------- Plus de bouffe a craft
        if is_color(570, 969, (108, 108, 108), 10):
            print("Food cook finished")
            time.sleep(0.5)
            break

        # ---------------- Encore de la bouffe a craft
        if is_color(570, 969, (231, 163,  20), 10):
            print("Food cook finished")
            time.sleep(0.5)
            break

        time.sleep(0.5)

    # ---------------- Retourne au lobby ----------------
    time.sleep(1)
    tap(40, 32)
    time.sleep(3)
    tap(40, 32)

    # ---------------- Savoir si on est dans un menu ----------------
    wait_for_image(in_menu_image_path, region_in_menu, 0.9)
