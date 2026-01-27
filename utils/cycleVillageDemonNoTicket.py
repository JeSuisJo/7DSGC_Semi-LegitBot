import time
from .battlePreparation import run_battle_preparation
from .fightPve import fight_pve
from .battlePreparationEquipementAuto import battle_preparation_equipement_auto


def cycle_village_demon_no_ticket(adb, difficulty_image_path, region_difficulty, cancel_color):
    # ---------------- Savoir si on est dans le choix de la difficulté de la mission ----------------
    while True:
        is_match, similarity = adb.compare_region_with_image(
            reference_image_path=difficulty_image_path,
            region=region_difficulty,
            threshold=0.9,
        )
        if is_match:
            break
        time.sleep(0.5)

    # ---------------- Cliquer sur la dernière difficulté ----------------
    print("Last difficulty")
    adb.tap(384, 737)
    time.sleep(0.5)

    # ---------------- Faire la preparation ----------------
    run_battle_preparation()

    # ---------------- Faire le fight PVE ----------------
    fight_pve()

    # ---------------- Attendre l'apparition de la couleur du bouton annuler du demon apparu ----------------
    while True:
        detected_color = adb.get_color_at(347, 940, target_color=cancel_color, tolerance=10)
        if detected_color:
            time.sleep(0.8)
            print("Demon appeared")
            adb.tap(347, 940)
            time.sleep(1)
            break
        time.sleep(0.5)


def cycle_village_demon_no_ticket_auto(adb, difficulty_image_path, region_difficulty, cancel_color):
    # ---------------- Savoir si on est dans le choix de la difficulté de la mission ----------------
    while True:
        is_match, similarity = adb.compare_region_with_image(
            reference_image_path=difficulty_image_path,
            region=region_difficulty,
            threshold=0.9,
        )
        if is_match:
            break
        time.sleep(0.5)

    # ---------------- Cliquer sur la dernière difficulté ----------------
    print("Last difficulty")
    adb.tap(384, 737)
    time.sleep(0.5)

    # ---------------- Faire la preparation ----------------
    battle_preparation_equipement_auto()

    # ---------------- Faire le fight PVE ----------------
    fight_pve()

    # ---------------- Attendre l'apparition de la couleur du bouton annuler du demon apparu ----------------
    while True:
        detected_color = adb.get_color_at(347, 940, target_color=cancel_color, tolerance=10)
        if detected_color:
            time.sleep(0.8)
            print("Demon appeared")
            adb.tap(347, 940)
            time.sleep(1)
            break
        time.sleep(0.5)

