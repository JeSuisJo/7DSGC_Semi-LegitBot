from . import tap, path, stop, wait_for_image, wait_for_color, is_color, compare_image
import time
import os

def run_battle_preparation():
    region_prep = (175, 997, 218, 1032)
    prep_image_path = path("img/prep.png")
    color_options_disabled = (54, 48, 39)
    color_options_enabled = (236, 203, 46)
    tolerance = 10
    region_potion = (365, 333, 429, 411)
    potion_image_path = path("img/act.png")
    region_diamond = (363, 662, 425, 698)
    diamond_image_path = path("img/diamond.png")

    # ---------------- Savoir si on est dans la preparation du combat ----------------
    wait_for_image(prep_image_path, region_prep, 0.9)

    # ---------------- Clique sur la configuration du mode automatique ----------------
    print("Battle preparation configuration")
    tap(142, 1018)

    # ---------------- Savoir si on est dans la configuration du mode automatique avec la recherche du bouton ok ----------------
    wait_for_color(453, 754, (45, 169, 116), 10)

    # ---------------- Check des utilisation des potions automatiques ----------------
    while True:
        if is_color(239, 624, color_options_disabled, tolerance):
            tap(239, 624)
            print("Potions automatically activated")
            break
        if is_color(239, 624, color_options_enabled, tolerance):
            print("Potions already activated")
            break
        time.sleep(0.5)

    # ---------------- Check des répétitions du niveau ----------------
    while True:
        if is_color(239, 369, color_options_disabled, tolerance):
            tap(239, 369)
            print("Level repetitions set to infinite")
            break
        if is_color(239, 369, color_options_enabled, tolerance):
            print("Level repetitions already set to infinite")
            break
        time.sleep(0.5)

    # ---------------- Sauvegarde de la configuration automatique ----------------
    time.sleep(0.5)
    print("Saving configuration")
    tap(453, 754)

    # ---------------- Lancement du combat ----------------
    time.sleep(0.8)
    print("Starting battle")
    tap(406, 1016)
    time.sleep(1.7)

    # ---------------- Si plus d'act alors mettre des potions ----------------
    if compare_image(potion_image_path, region_potion, 0.9):
        print("No more ACT, refill potions")
        tap(399, 805)
        time.sleep(1)
        print("Restarting battle")
        tap(406, 1016)

    # ---------------- Si plus d'act et demande des diamants alors on stop le script ----------------
    if compare_image(diamond_image_path, region_diamond, 0.9):
        stop("No more ACT and no more potions")
