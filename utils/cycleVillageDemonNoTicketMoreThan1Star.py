import time
from . import tap, wait_for_image, wait_for_color
from .battlePreparation import run_battle_preparation
from .fightPve import fight_pve
from .battlePreparationEquipementAuto import battle_preparation_equipement_auto


def cycle_village_demon_no_ticket_more_than_1_stars(difficulty_image_path, region_difficulty, cancel_color):
    # ---------------- Savoir si on est dans le choix de la difficulté de la mission ----------------
    wait_for_image(difficulty_image_path, region_difficulty, 0.9)

    # ---------------- Cliquer sur la dernière difficulté ----------------
    print("Last difficulty")
    tap(399, 444)
    time.sleep(0.5)

    # ---------------- Faire la preparation ----------------
    run_battle_preparation()

    # ---------------- Faire le fight PVE ----------------
    fight_pve()

    # ---------------- Attendre l'apparition de la couleur du bouton annuler du demon apparu ----------------
    wait_for_color(347, 940, cancel_color, 10)
    time.sleep(0.8)
    print("Demon appeared")
    tap(347, 940)
    time.sleep(1)


def cycle_village_demon_no_ticket_more_than_1_stars_auto(difficulty_image_path, region_difficulty, cancel_color):
    # ---------------- Savoir si on est dans le choix de la difficulté de la mission ----------------
    wait_for_image(difficulty_image_path, region_difficulty, 0.9)

    # ---------------- Cliquer sur la dernière difficulté ----------------
    print("Last difficulty")
    tap(399, 444)
    time.sleep(0.5)

    # ---------------- Faire la preparation ----------------
    battle_preparation_equipement_auto()

    # ---------------- Faire le fight PVE ----------------
    fight_pve()

    # ---------------- Attendre l'apparition de la couleur du bouton annuler du demon apparu ----------------
    wait_for_color(347, 940, cancel_color, 10)
    time.sleep(0.8)
    print("Demon appeared")
    tap(347, 940)
    time.sleep(1)
