from utils.adb_helper import auto_setup_adb, get_project_path, ADBHelper
from utils.cycleVillageDemonNoTicket import cycle_village_demon_no_ticket
from utils.cycleVillageDemonNoTicket import cycle_village_demon_no_ticket_auto
import time
import os
from utils.fightDemon import load_config
from utils.cycleVillageDemonNoTicketMoreThan1Star import cycle_village_demon_no_ticket_more_than_1_stars
from utils.cycleVillageDemonNoTicketMoreThan1Star import cycle_village_demon_no_ticket_more_than_1_stars_auto

def village_demon_daily():
    # Configuration automatique de ADB
    adb = auto_setup_adb(verbose=False)
    config = load_config()
    os.system('cls')
    print("=" * 50)
    print(" Daily mode : Village Clear 3/8")
    print("=" * 50)

    region_difficulty = (604, 437, 635, 470)
    difficulty_image_path = get_project_path("img/difficulty.png")
    cancel_color = (151, 70, 48)


    # ---------------- Cliquer sur le les demons selon le nombre d'etoiles----------------
    if config.get("daily_demon_stars") == "1":
        adb.tap(241, 363)
    elif config.get("daily_demon_stars") == "2":
        adb.tap(414, 371)
    elif config.get("daily_demon_stars") == "3":
        adb.tap(589, 374)
    time.sleep(1)

    # ---------------- Savoir si l'achevement auto est activé ----------------
    if adb.is_color_at(
        647, 261,
        target_color=(60, 124, 170),
        tolerance=10
    ):
        print("Desactivated achievement auto")
        adb.tap(647, 261)
        time.sleep(0.5)

    # ---------------- Cliquer sur le premier village ----------------
    print("First village")
    adb.tap(200, 485)
    time.sleep(0.5)

    # ---------------- Cycle le village des demons selon le nombre d'etoiles ----------------
    if config.get("daily_demon_stars") == "1":
        cycle_village_demon_no_ticket(
            adb=adb,
            difficulty_image_path=difficulty_image_path,
            region_difficulty=region_difficulty,
            cancel_color=cancel_color,
        )
    elif config.get("daily_demon_stars") > "1":
        cycle_village_demon_no_ticket_more_than_1_stars(
            adb=adb,
            difficulty_image_path=difficulty_image_path,
            region_difficulty=region_difficulty,
            cancel_color=cancel_color,
        )
    time.sleep(0.5)

    # ---------------- Aller au deuxieme village ----------------
    os.system('cls')
    print("=" * 50)
    print(" Daily mode : Village Clear 3/8")
    print("=" * 50)
    print("Second village")
    adb.tap(659, 146)
    time.sleep(0.5)

    # ---------------- Cycle le village des demons selon le nombre d'etoiles ----------------
    if config.get("daily_demon_stars") == "1":
        cycle_village_demon_no_ticket_auto(
            adb=adb,
            difficulty_image_path=difficulty_image_path,
            region_difficulty=region_difficulty,
            cancel_color=cancel_color,
        )
    elif config.get("daily_demon_stars") > "1":
        cycle_village_demon_no_ticket_more_than_1_stars_auto(
            adb=adb,
            difficulty_image_path=difficulty_image_path,
            region_difficulty=region_difficulty,
            cancel_color=cancel_color,
        )
    
    # ---------------- Aller au troisieme village ----------------
    os.system('cls')
    print("=" * 50)
    print(" Daily mode : Village Clear 3/8")
    print("=" * 50)
    print("Third village")
    adb.tap(659, 146)
    time.sleep(0.5)

    # ---------------- Cycle le village des demons selon le nombre d'etoiles ----------------
    if config.get("daily_demon_stars") == "1":
        cycle_village_demon_no_ticket_auto(
            adb=adb,
            difficulty_image_path=difficulty_image_path,
            region_difficulty=region_difficulty,
            cancel_color=cancel_color,
        )
    elif config.get("daily_demon_stars") > "1":
        cycle_village_demon_no_ticket_more_than_1_stars_auto(
            adb=adb,
            difficulty_image_path=difficulty_image_path,
            region_difficulty=region_difficulty,
            cancel_color=cancel_color,
        )

    # ---------------- Aller au quatrieme village ----------------
    os.system('cls')
    print("=" * 50)
    print(" Daily mode : Village Clear 3/8")
    print("=" * 50)
    print("Fourth village")
    adb.tap(659, 146)
    time.sleep(0.5)

    # ---------------- Cycle le village des demons selon le nombre d'etoiles ----------------
    if config.get("daily_demon_stars") == "1":
        cycle_village_demon_no_ticket_auto(
            adb=adb,
            difficulty_image_path=difficulty_image_path,
            region_difficulty=region_difficulty,
            cancel_color=cancel_color,
        )
    elif config.get("daily_demon_stars") > "1":
        cycle_village_demon_no_ticket_more_than_1_stars_auto(
            adb=adb,
            difficulty_image_path=difficulty_image_path,
            region_difficulty=region_difficulty,
            cancel_color=cancel_color,
        )
    
    # ---------------- Aller au cinquieme village ----------------
    os.system('cls')
    print("=" * 50)
    print(" Daily mode : Village Clear 3/8")
    print("=" * 50)
    print("Fifth village")
    adb.tap(659, 146)
    time.sleep(0.5)

    # ---------------- Cycle le village des demons selon le nombre d'etoiles ----------------
    if config.get("daily_demon_stars") == "1":
        cycle_village_demon_no_ticket_auto(
            adb=adb,
            difficulty_image_path=difficulty_image_path,
            region_difficulty=region_difficulty,
            cancel_color=cancel_color,
        )
    elif config.get("daily_demon_stars") > "1":
        cycle_village_demon_no_ticket_more_than_1_stars_auto(
            adb=adb,
            difficulty_image_path=difficulty_image_path,
            region_difficulty=region_difficulty,
            cancel_color=cancel_color,
        )

    # ---------------- Aller au sixieme village ----------------
    os.system('cls')
    print("=" * 50)
    print(" Daily mode : Village Clear 3/8")
    print("=" * 50)
    print("Sixth village")
    adb.tap(659, 146)
    time.sleep(0.5)

    # ---------------- Cycle le village des demons selon le nombre d'etoiles ----------------
    if config.get("daily_demon_stars") == "1":
        cycle_village_demon_no_ticket_auto(
            adb=adb,
            difficulty_image_path=difficulty_image_path,
            region_difficulty=region_difficulty,
            cancel_color=cancel_color,
        )
    elif config.get("daily_demon_stars") > "1":
        cycle_village_demon_no_ticket_more_than_1_stars_auto(
            adb=adb,
            difficulty_image_path=difficulty_image_path,
            region_difficulty=region_difficulty,
            cancel_color=cancel_color,
        )
        
    # ---------------- Retour au menu des boss ----------------
    print("Return to the boss menu")
    adb.tap(156, 240)
    time.sleep(0.5)
