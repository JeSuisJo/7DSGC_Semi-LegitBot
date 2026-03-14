from . import tap, path, wait_for_image, is_color, compare_image
from utils.fightDemon import load_config

import time
import os

def Daily_3v3():
    os.system('cls')
    print("=" * 50)
    print(" Daily mode : PVP 7/8")
    print("=" * 50)

    config = load_config()
    region_home = (615, 1005, 662, 1041)
    home_image_path = path("img/home.png")
    region_hub = (562, 345, 617, 402)
    hub_image_path = path("img/hub.png")
    region_3v3 = (730, 139, 769, 171)
    image_path_3v3 = path("img/3v3.png")
    region_in_3v3 = (251, 1008, 285, 1042)
    image_path_in_3v3_pvp = path("img/in_3v3_pvp.png")
    region_pvp_finish = (637, 1001, 666, 1022)
    pvp_finish_image_path = path("img/pvp-finsh.png")
    region_in_menu = (4, 9, 60, 62)
    in_menu_image_path = path("img/return.png")

    # ---------------- Savoir si on est dans la taverne ----------------
    wait_for_image(home_image_path, region_home, 0.9)

    # ---------------- Clique sur le bouton menu combat ----------------
    print("Menu")
    tap(738, 745)
    time.sleep(0.5)

    # ---------------- Savoir si on est dans le menu ----------------
    wait_for_image(hub_image_path, region_hub, 0.9)

    # ---------------- Cliquer sur le 3v3 ----------------
    tap(577, 751)
    time.sleep(0.5)

    # ---------------- Savoir si on est dans la preparation du combat ----------------
    while True:
        if compare_image(image_path_3v3, region_3v3, 0.9):
            time.sleep(0.5)
            break

        if is_color(477, 889, (36, 144, 89), 10):
            tap(477, 889)
            time.sleep(0.5)

        if is_color(592, 874, (40, 149, 97), 10):
            tap(592, 874)
            time.sleep(0.5)

    time.sleep(0.5)

    # ---------------- Savoir si il y a le daily reward du 3v3 ----------------
    time.sleep(3)
    if is_color(550, 185, (125, 250, 98), 50):
        print("Take reward 3v3")
        tap(551, 189)
        time.sleep(1.5)
        tap(551, 189)
        time.sleep(1.5)
    else:
        print("No reward for now")
        time.sleep(1.5)

    # ---------------- Savoir si l'utilisateur veut faire le 3v3 ou non ----------------
    if config.get("only_reward_3v3") == "true":
        print("Only taking the reward for the 3v3")
        tap(43, 32)
    else:
        while True:
            tap(586, 424)
            time.sleep(1)

            wait_for_image(image_path_in_3v3_pvp, region_in_3v3, 0.9)
            time.sleep(1.5)
            tap(402, 1029)
            time.sleep(3)

            if compare_image(in_menu_image_path, region_in_menu, 0.9):
                print("All tickets used")
                tap(34, 35)
                time.sleep(0.8)
                tap(34, 35)
                time.sleep(0.5)
                break

            wait_for_image(pvp_finish_image_path, region_pvp_finish, 0.9)
            time.sleep(1.5)
            tap(399, 1008)

            wait_for_image(image_path_3v3, region_3v3, 0.9)
            time.sleep(2)
