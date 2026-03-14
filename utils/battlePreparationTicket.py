from . import tap, path, stop, wait_for_image, wait_for_color, is_color, compare_image

import time
import os

def run_battle_preparation_ticket():
    region_prep = (175, 997, 218, 1032)
    prep_image_path = path("img/prep.png")
    region_rulstats = (4, 9, 60, 62)
    rulstats_image_path = path("img/return.png")
    region_diamond = (363, 662, 425, 698)
    diamond_image_path = path("img/diamond.png")

    # ---------------- Savoir si on est dans la preparation du combat ----------------
    wait_for_image(prep_image_path, region_prep, 0.9)

    # ---------------- Clique sur l'achevement auto ----------------
    print("Ticket menu")
    tap(609, 1025)
    time.sleep(0.5)

    # ---------------- Savoir si on est dans le menu des tickets ----------------
    wait_for_color(469, 855, (42, 158, 104), 10)

    # ---------------- Clique sur le maximum de tickets ----------------
    while True:
        if is_color(579, 700, (199, 155, 53), 10):
            break
        tap(579, 700)
        print("Clicking for the maximum tickets use")
        time.sleep(0.5)

    # ---------------- Clique sur le lancement du niveau avec les tickets ----------------
    print("Starting level with tickets")
    tap(411, 869)
    time.sleep(1)

    # ---------------- Si plus d'act et demande des diamants alors on stop le script ----------------
    if compare_image(diamond_image_path, region_diamond, 0.9):
        stop("No more ACT and no more potions")

    # ---------------- TANT QUE LES RULSTATS SONT PAS FINI ON CLIQUE----------------
    while True:
        if compare_image(rulstats_image_path, region_rulstats, 0.9):
            print("Level finished")
            break
        tap(397, 116)
        time.sleep(0.5)

    # ---------------- Clique sur le bouton retour ----------------
    time.sleep(0.8)
    print("Return")
    tap(43, 29)
    time.sleep(0.5)
