from . import tap, path, wait_for_image, compare_image
from utils.fightDemon import load_config
from utils.Daily3v3Pvp import Daily_3v3

import time
import os

def Daily_pvp():
    config = load_config()
    region_home = (615, 1005, 662, 1041)
    home_image_path = path("img/home.png")
    region_pvp = (245, 995, 278, 1025)
    pvp_image_path = path("img/pvp.png")
    region_pvp_finish = (637, 1001, 666, 1022)
    pvp_finish_image_path = path("img/pvp-finsh.png")
    region_pvp_leave = (380, 580, 425, 607)
    pvp_leave_image_path = path("img/ok_leave.png")
    region_diamond = (363, 583, 425, 619)
    diamond_image_path = path("img/diamond.png")
    no_more_diamond_image_path = path("img/no-diam.png")
    region_auto_fight = (753, 20, 780, 45)
    auto_fight_image_path = path("img/auto-fight.png")
    region_pvp_rank_up = (377, 972, 423, 996)
    pvp_rank_up_image_path = path("img/ok-rank-pvp.png")

    Daily_3v3()

    # ---------------- Savoir si on est dans la taverne ----------------
    wait_for_image(home_image_path, region_home, 0.9)

    # ---------------- Clique sur le bouton menu deroulant ----------------
    tap(51, 891)
    time.sleep(0.7)

    if config.get("pvp_stuff") == "true":
        print("Going to PvP (with equipment)")
        tap(51, 663)
        time.sleep(0.5)
    else:
        print("Going to PvP (no equipment)")
        tap(51, 737)
        time.sleep(0.5)

    # ---------------- Savoir si on est dans le menu ----------------
    wait_for_image(pvp_image_path, region_pvp, 0.9)
    print("Preparing to use all tickets")

    # ---------------- Loop de game jusqu'a avoir le diamand qui apparait ----------------
    while True:
        if compare_image(diamond_image_path, region_diamond, 0.9):
            print("No more PvP tickets")
            tap(589, 336)
            time.sleep(0.8)
            tap(504, 1008)
            break

        if compare_image(no_more_diamond_image_path, region_diamond, 0.9):
            print("No more PvP tickets")
            tap(589, 336)
            time.sleep(0.8)
            tap(504, 1008)
            break

        tap(741, 482)

        if compare_image(pvp_image_path, region_pvp, 0.9):
            time.sleep(0.5)
            tap(405, 1014)
            time.sleep(1.5)

        if compare_image(auto_fight_image_path, region_auto_fight, 0.9):
            time.sleep(0.5)
            tap(712, 26)
            time.sleep(0.5)
            while True:
                if compare_image(pvp_leave_image_path, region_pvp_leave, 0.9):
                    time.sleep(0.5)
                    tap(399, 590)

                pvp_fight_finished = compare_image(pvp_finish_image_path, region_pvp_finish, 0.9)
                tap(758, 514)

                if pvp_fight_finished:
                    time.sleep(0.5)
                    tap(294, 1002)
                    time.sleep(0.7)
                    break

                time.sleep(0.5)

        if compare_image(pvp_rank_up_image_path, region_pvp_rank_up, 0.9):
            tap(399, 979)
            time.sleep(0.5)

        if compare_image(pvp_finish_image_path, region_pvp_finish, 0.9):
            time.sleep(0.5)
            tap(294, 1002)
            time.sleep(0.7)

        time.sleep(0.5)

    # ---------------- Savoir si on est dans la taverne ----------------
    wait_for_image(home_image_path, region_home, 0.9)
    time.sleep(0.8)
