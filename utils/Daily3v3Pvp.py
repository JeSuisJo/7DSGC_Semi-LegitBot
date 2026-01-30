from .adb_helper import auto_setup_adb, ADBHelper, get_project_path, StopScriptException, KeyCode
from utils.fightDemon import load_config

import time
import os

def Daily_3v3():
    # Configuration automatique de ADB
    adb = auto_setup_adb(verbose=False)
    os.system('cls')
    print("=" * 50)
    print(" Daily mode : PVP 7/8")
    print("=" * 50)

    config = load_config()
    region_home = (615, 1005, 662, 1041)
    home_image_path = get_project_path("img/home.png")
    region_hub = (562, 345, 617, 402)
    hub_image_path = get_project_path("img/hub.png")
    region_3v3 = (730, 139, 769, 171)
    image_path_3v3 = get_project_path("img/3v3.png")
    region_in_3v3 = (251, 1008, 285, 1042)
    image_path_in_3v3_pvp = get_project_path("img/in_3v3_pvp.png")
    region_pvp_finish = (637, 1001, 666, 1022)
    pvp_finish_image_path = get_project_path("img/pvp-finsh.png")
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

    # ---------------- Clique sur le bouton menu combat ----------------
    print("Menu")
    adb.tap(738, 745)
    time.sleep(0.5)

    # ---------------- Savoir si on est dans le menu ----------------
    while True:
        in_hub = adb.compare_region_with_image(
            reference_image_path=hub_image_path,
            region=region_hub,
            threshold=0.9,
        )
        if in_hub:
            break
        time.sleep(0.5)

    # ---------------- Cliquer sur le 3v3 ----------------
    adb.tap(577, 751)
    time.sleep(0.5)
    
    # ---------------- Savoir si on est dans la preparation du combat ----------------
    while True:
        in_3v3_prep = adb.compare_region_with_image(
            reference_image_path=image_path_3v3,
            region=region_3v3,
            threshold=0.9,
        )
        if in_3v3_prep:
            time.sleep(0.5)
            break

        # ---------------- Reward daily et le ok 
        weekly_reward_color = adb.get_color_at(
            477, 889, 
            target_color=(36, 144, 89), 
            tolerance=10)
        if weekly_reward_color:
            adb.tap(477, 889)
            time.sleep(0.5)


        # ---------------- Rejoindre toutes les leagues pvp
        rejoin_pvp_league_color = adb.get_color_at(
            592, 874,
            target_color= (40, 149, 97),
            tolerance=10
        )

        if rejoin_pvp_league_color:
            adb.tap(592, 874)
            time.sleep(0.5)

    time.sleep(0.5)

    # ---------------- Savoir si il y a le daily reward du 3v3 ----------------
    time.sleep(2.5)
    daily_reward_3v3_color = adb.get_color_at(
        550, 185,
        target_color= (125, 250, 98),
        tolerance=50
    )

    if daily_reward_3v3_color:
        print("Take reward 3v3")
        adb.tap(551, 189)
        time.sleep(1.5)
        adb.tap(551, 189)
        time.sleep(0.5)
    else:
        print("No reward for now")
        time.sleep(0.5)
    
    # ---------------- Savoir si l'utilisateur veut faire le 3v3 ou non ----------------
    if config.get("only_reward_3v3") == "true":
        print("Only taking the reward for the 3v3")
        adb.tap(43, 32)
    else:
        while True:
            # ---------------- Lance le premier de la liste de fight
            adb.tap(586, 424)
            time.sleep(1)

            # ---------------- Attends de savoir si on est dans le choix des teams et lancer
            while True:
                in_3v3_team_select = adb.compare_region_with_image(
                    reference_image_path=image_path_in_3v3_pvp,
                    region=region_in_3v3,
                    threshold=0.9,
                )
                if in_3v3_team_select:
                    time.sleep(1.5)
                    adb.tap(402, 1029)
                    time.sleep(3)
                    break

            # ---------------- Attendre 3s et si il trouve le return alors il y a plus de ticket alons sort de la boucle
            no_more_tickets = adb.compare_region_with_image(
                reference_image_path=in_menu_image_path,
                region=region_in_menu,
                threshold=0.9,
            )
            if no_more_tickets:
                print("All tickets used")
                adb.tap(34, 35)
                time.sleep(0.8)
                adb.tap(34, 35)
                time.sleep(0.5)
                break
            
            # ---------------- Ok de fin de fight
            while True:
                pvp_fight_finished = adb.compare_region_with_image(
                    reference_image_path=pvp_finish_image_path,
                    region=region_pvp_finish,
                    threshold=0.9,
                )
                if pvp_fight_finished:
                    time.sleep(1.5)
                    adb.tap(399, 1008)
                    break

            # ---------------- savoir si on est de retour a la listes des fights
            while True:
                back_to_3v3_list = adb.compare_region_with_image(
                    reference_image_path=image_path_3v3,
                    region=region_3v3,
                    threshold=0.9,
                )
                if back_to_3v3_list:
                    time.sleep(2)
                    break

