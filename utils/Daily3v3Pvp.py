from .adb_helper import auto_setup_adb, ADBHelper, get_project_path, StopScriptException, KeyCode
from utils.fightDemon import load_config

import time
import os

def Daily_3v3():
    # Configuration automatique de ADB
    adb = auto_setup_adb(verbose=False)
    config = load_config()
    region_home = (615, 1005, 662, 1041)
    home_image_path = get_project_path("img/home.png")
    region_hub = (562, 345, 617, 402)
    hub_image_path = get_project_path("img/hub.png")
    region_3v3 = (730, 139, 769, 171)
    image_path_3v3 = get_project_path("img/3v3.png")

    # ---------------- Savoir si on est dans la taverne ----------------
    while True:
        is_match, similarity = adb.compare_region_with_image(
            reference_image_path=home_image_path,
            region=region_home,
            threshold=0.9,
        )

        if is_match:
            break

        time.sleep(0.5)

    # ---------------- Clique sur le bouton menu combat ----------------
    print("Menu")
    adb.tap(738, 745)
    time.sleep(0.5)

    # ---------------- Savoir si on est dans le menu ----------------
    while True:
        is_match, similarity = adb.compare_region_with_image(
            reference_image_path=hub_image_path,
            region=region_hub,
            threshold=0.9,
        )

        if is_match:
            break
        time.sleep(0.5)

    # ---------------- Cliquer sur le 3v3 ----------------
    adb.tap(577, 751)
    time.sleep(0.5)
    
    # ---------------- Savoir si on est dans la preparation du combat ----------------
    while True:
        is_match, similarity = adb.compare_region_with_image(
            reference_image_path=image_path_3v3,
            region=region_3v3,
            threshold=0.9
        )

        if is_match:
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
    time.sleep(1.5)
    daily_reward_3v3_color = adb.get_color_at(
        551, 189,
        target_color= (40, 149, 97),
        tolerance=10
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
        print("caca")
