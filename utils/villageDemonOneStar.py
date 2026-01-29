from utils.adb_helper import auto_setup_adb, get_project_path, ADBHelper
from utils.cycleVillageDemonNoTicket import cycle_village_demon_no_ticket
from utils.cycleVillageDemonNoTicket import cycle_village_demon_no_ticket_auto
import time
import os

def village_demon_one_star():
    # Configuration automatique de ADB
    adb = auto_setup_adb(verbose=False)
    os.system('cls')
    print("=" * 50)
    print(" Auto demon farm mode")
    print("=" * 50)

    region_difficulty = (604, 437, 635, 470)
    difficulty_image_path = get_project_path("img/difficulty.png")
    cancel_color = (151, 70, 48)


    # ---------------- Cliquer sur le les demons 1 etoile ----------------
    adb.tap(241, 363)
    time.sleep(1)

    # ---------------- Savoir si l'achevement auto est activé ----------------
    if adb.is_color_at(
        647, 261,
        target_color=(60, 124, 170),
        tolerance=10
    ):
        print("Deactivated achievement auto")
        adb.tap(647, 261)
        time.sleep(0.5)

    # ---------------- Cliquer sur le premier village ----------------
    print("First village")
    adb.tap(200, 485)
    time.sleep(0.5)

    # ---------------- Cycle le village des demons 1 etoile sans ticket  ----------------
    cycle_village_demon_no_ticket(
        adb=adb,
        difficulty_image_path=difficulty_image_path,
        region_difficulty=region_difficulty,
        cancel_color=cancel_color,
    )

    # ---------------- Aller au deuxieme village ----------------
    os.system('cls')
    print("=" * 50)
    print(" Auto demon farm mode")
    print("=" * 50)
    print("Second village")
    adb.tap(659, 146)
    time.sleep(0.5)

    # ---------------- Cycle le village des demons 1 etoile sans ticket  ----------------
    cycle_village_demon_no_ticket_auto(
        adb=adb,
        difficulty_image_path=difficulty_image_path,
        region_difficulty=region_difficulty,
        cancel_color=cancel_color,
    )

    # ---------------- Aller au troisieme village ----------------
    os.system('cls')
    print("=" * 50)
    print(" Auto demon farm mode")
    print("=" * 50)
    print("Third village")
    adb.tap(659, 146)
    time.sleep(0.5)

    # ---------------- Cycle le village des demons 1 etoile sans ticket  ----------------
    cycle_village_demon_no_ticket_auto(
        adb=adb,
        difficulty_image_path=difficulty_image_path,
        region_difficulty=region_difficulty,
        cancel_color=cancel_color,
    )

    # ---------------- Aller au quatrieme village ----------------
    os.system('cls')
    print("=" * 50)
    print(" Auto demon farm mode")
    print("=" * 50)
    print("Fourth village")
    adb.tap(659, 146)
    time.sleep(0.5)

    # ---------------- Cycle le village des demons 1 etoile sans ticket  ----------------
    cycle_village_demon_no_ticket_auto(
        adb=adb,
        difficulty_image_path=difficulty_image_path,
        region_difficulty=region_difficulty,
        cancel_color=cancel_color,
    )

    # ---------------- Aller au cinquieme village ----------------
    os.system('cls')
    print("=" * 50)
    print(" Auto demon farm mode")
    print("=" * 50)
    print("Fifth village")
    adb.tap(659, 146)
    time.sleep(0.5)

    # ---------------- Cycle le village des demons 1 etoile sans ticket  ----------------
    cycle_village_demon_no_ticket_auto(
        adb=adb,
        difficulty_image_path=difficulty_image_path,
        region_difficulty=region_difficulty,
        cancel_color=cancel_color,
    )

    # ---------------- Aller au sixieme village ----------------
    os.system('cls')
    print("=" * 50)
    print(" Auto demon farm mode")
    print("=" * 50)
    print("Sixth village")
    adb.tap(659, 146)
    time.sleep(0.5)

    # ---------------- Cycle le village des demons 1 etoile sans ticket  ----------------
    cycle_village_demon_no_ticket_auto(
        adb=adb,
        difficulty_image_path=difficulty_image_path,
        region_difficulty=region_difficulty,
        cancel_color=cancel_color,
    )

    # ---------------- Retour au menu des boss ----------------
    print("Return to the boss menu")
    adb.tap(156, 240)
    time.sleep(0.5)