from utils.adb_helper import auto_setup_adb
import time
import os
from utils.collectBeer import collect_beer
# from utils.recyclingEquipement import recycle_equipement
from utils.fightDemon import load_config
from utils.goToBossMenu import go_to_boss_menu
from utils.villageDemonDaily import village_demon_daily
from utils.villageDemonDailyTicket import village_demon_daily_ticket
from utils.clearDemon import clear_demons
from utils.specialDungeon import run_special_dungeon
from utils.yggdrasil import run_yggdrasil
from utils.expeditions import run_expeditions
from utils.friendPoint import send_friends_points
from utils.food import food_preparation

def run_daily():
    # Configuration automatique de ADB
    adb = auto_setup_adb(verbose=True)
    config = load_config()
    os.system('cls')
    print("=" * 50)
    print(" Daily mode")
    print("=" * 50)

    # ---------------- Recycler les equipements ----------------
    # recycle_equipement()
    # time.sleep(0.5)

    # ---------------- Collecter la bierre 1/8 ----------------
    collect_beer()
    time.sleep(0.5)

    # ---------------- Faire de la nouriture 2/8 ----------------
    food_preparation()
    time.sleep(0.5)
    
    # ---------------- Faire les demons dailys 3/8 ----------------
    go_to_boss_menu()
    time.sleep(0.5)
    if config.get("daily_demon_ticket") == "true":
        village_demon_daily_ticket()
        time.sleep(0.5)
        clear_demons()
    else:
        village_demon_daily()
        time.sleep(0.5)
        clear_demons()

    # ---------------- Retourner a la taverne ----------------
    print("Return to the tavern")
    adb.tap(148, 1011)
    time.sleep(0.5)

    # ---------------- Faire le donjon special 4/8 ----------------
    run_special_dungeon()
    time.sleep(1)

    # ---------------- Faire Yggdrasil 5/8 ----------------
    run_yggdrasil()
    time.sleep(1)

    # ---------------- Faire les expeditions 6/8 ----------------
    run_expeditions()
    time.sleep(1)

    # ---------------- Faire le PVP 7/8 ----------------

    # --------------- Enovyer les points amis 8/8 ----------------
    send_friends_points()