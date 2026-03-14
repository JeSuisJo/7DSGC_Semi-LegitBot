from . import tap, path, stop, wait_for_image, compare_image
import time
import os

def battle_preparation_equipement_auto():
    region_prep = (175, 997, 218, 1032)
    prep_image_path = path("img/prep.png")
    region_potion = (365, 333, 429, 411)
    potion_image_path = path("img/act.png")
    region_diamond = (363, 662, 425, 698)
    diamond_image_path = path("img/diamond.png")

    # ---------------- Savoir si on est dans la preparation du combat ----------------
    wait_for_image(prep_image_path, region_prep, 0.9)

    # ---------------- Clique sur la configuration du mode automatique ----------------
    print("Auto mode")
    tap(194, 1017)
    time.sleep(0.5)

    # ---------------- Lancement du combat ----------------
    time.sleep(0.8)
    print("Starting battle")
    tap(406, 1016)
    time.sleep(1.7)

    # ---------------- Si plus d'act alors mettre des potions ----------------
    if compare_image(potion_image_path, region_potion, 0.9):
        print("No more ACT, refill potions")
        tap(399, 805)
        time.sleep(0.7)
        print("Restarting battle")
        tap(406, 1016)

    # ---------------- Si plus d'act et demande des diamants alors on stop le script ----------------
    if compare_image(diamond_image_path, region_diamond, 0.9):
        stop("No more ACT and no more potions")
