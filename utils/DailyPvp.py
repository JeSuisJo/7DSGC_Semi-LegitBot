from .adb_helper import auto_setup_adb, ADBHelper, get_project_path, StopScriptException, KeyCode
from utils.fightDemon import load_config
from utils.Daily3v3Pvp import Daily_3v3

import time
import os

def Daily_pvp():
    # Configuration automatique de ADB
    adb = auto_setup_adb(verbose=False)
    config = load_config()
    region_home = (615, 1005, 662, 1041)
    home_image_path = get_project_path("img/home.png")
    region_pvp = (245, 995, 278, 1025)
    pvp_image_path = get_project_path("img/pvp.png")
    region_pvp_finish = (637, 1001, 666, 1022)
    pvp_finish_image_path = get_project_path("img/pvp-finsh.png")
    region_pvp_leave = (380, 580, 425, 607)
    pvp_leave_image_path = get_project_path("img/ok_leave.png")
    region_diamond = (363, 583, 425, 619)
    diamond_image_path = get_project_path("img/diamond.png")
    no_more_diamond_image_path = get_project_path("img/no-diam.png")
    region_auto_fight = (753, 20, 780, 45)
    auto_fight_image_path = get_project_path("img/auto-fight.png")
    region_pvp_rank_up = (377, 972, 423, 996)
    pvp_rank_up_image_path = get_project_path("img/ok-rank-pvp.png")

    Daily_3v3()

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

    # ---------------- Clique sur le bouton menu deroulant ----------------
    adb.tap(51, 891)
    time.sleep(0.7)

    # ---------------- Clique sur le combat pvp no stuff ----------------
    print("Going to PvP (no equipment)")
    adb.tap(51, 737)
    time.sleep(0.5)

    # ---------------- Savoir si on est dans le menu ----------------
    while True:
        in_pvp_menu = adb.compare_region_with_image(
            reference_image_path=pvp_image_path,
            region=region_pvp,
            threshold=0.9,
        )
        if in_pvp_menu:
            print("Preparing to use all tickets")
            break
        time.sleep(0.5)

    # ---------------- Loop de game jusqu'a avoir le diamand qui apparait ----------------
    while True:
        # ---------------- Il reste des diamants
        no_more_tickets = adb.compare_region_with_image(
            reference_image_path=diamond_image_path,
            region=region_diamond,
            threshold=0.9,
        )
        if no_more_tickets:
            print("No more PvP tickets")
            adb.tap(589, 336)
            time.sleep(0.8)
            adb.tap(504, 1008)
            break

        # ---------------- Il reste plus de diamants
        no_more_tickets = adb.compare_region_with_image(
            reference_image_path=no_more_diamond_image_path,
            region=region_diamond,
            threshold=0.9,
        )
        if no_more_tickets:
            print("No more PvP tickets")
            adb.tap(589, 336)
            time.sleep(0.8)
            adb.tap(504, 1008)
            break

        adb.tap(741, 482)

        # ---------------- Si on trouve le menu on lance le fight
        pvp_menu_found = adb.compare_region_with_image(
            reference_image_path=pvp_image_path,
            region=region_pvp,
            threshold=0.9,
        )
        if pvp_menu_found:
            time.sleep(0.5)
            adb.tap(405, 1014)
            time.sleep(1.5)

        # ---------------- Lancer le mode auto est attendre la fin et relancer le fight
        auto_fight_visible = adb.compare_region_with_image(
            reference_image_path=auto_fight_image_path,
            region=region_auto_fight,
            threshold=0.9,
        )
        if auto_fight_visible:
            time.sleep(0.5)
            adb.tap(712, 26)
            time.sleep(0.5)
            while True:
                # Ok abandon
                leave_confirm_visible = adb.compare_region_with_image(
                    reference_image_path=pvp_leave_image_path,
                    region=region_pvp_leave,
                    threshold=0.9,
                )
                if leave_confirm_visible:
                    time.sleep(0.5)
                    adb.tap(399, 590)

                # Fin de fight
                pvp_fight_finished = adb.compare_region_with_image(
                    reference_image_path=pvp_finish_image_path,
                    region=region_pvp_finish,
                    threshold=0.9,
                )
                if pvp_fight_finished:
                    time.sleep(0.5)
                    adb.tap(294, 1002)
                    time.sleep(0.7)
                    break

                time.sleep(0.5)

        rank_up_ok_visible = adb.compare_region_with_image(
            reference_image_path=pvp_rank_up_image_path,
            region=region_pvp_rank_up,
            threshold=0.9,
        )
        if rank_up_ok_visible:
            adb.tap(399, 979)
            time.sleep(0.5)
        
        # ---------------- Si le joueur en face a abandonné instantanément ----------------
        pvp_fight_finished = adb.compare_region_with_image(
            reference_image_path=pvp_finish_image_path,
            region=region_pvp_finish,
            threshold=0.9,
        )
        if pvp_fight_finished:
            time.sleep(0.5)
            adb.tap(294, 1002)
            time.sleep(0.7)

        time.sleep(0.5)

    # ---------------- Savoir si on est dans la taverne ----------------
    while True:
        at_tavern = adb.compare_region_with_image(
            reference_image_path=home_image_path,
            region=region_home,
            threshold=0.9,
        )
        if at_tavern:
            time.sleep(0.8)
            break
        time.sleep(0.5)