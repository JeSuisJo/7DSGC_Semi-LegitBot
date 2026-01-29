from .adb_helper import auto_setup_adb, ADBHelper, get_project_path, StopScriptException, KeyCode

import time
import os

def run_battle_preparation_ticket():
    # Configuration automatique de ADB
    adb = auto_setup_adb(verbose=False)
    
    region_prep = (175, 997, 218, 1032)
    prep_image_path = get_project_path("img/prep.png")
    region_rulstats = (4, 9, 60, 62)
    rulstats_image_path = get_project_path("img/return.png")
    region_diamond = (363, 662, 425, 698)
    diamond_image_path = get_project_path("img/diamond.png")
    
    # ---------------- Savoir si on est dans la preparation du combat ----------------
    while True:
        in_prep_screen = adb.compare_region_with_image(
            reference_image_path=prep_image_path,
            region=region_prep,
            threshold=0.9,
        )
        if in_prep_screen:
            break

        time.sleep(0.5)

    # ---------------- Clique sur l'achevement auto ----------------
    print("Ticket menu")
    adb.tap(609, 1025)
    time.sleep(0.5)

    # ---------------- Savoir si on est dans le menu des tickets ----------------
    while True:
        if adb.is_color_at(
            469,
            855,
            target_color=(42, 158, 104),
            tolerance=10,
        ):
            break
        time.sleep(0.5)

    # ---------------- Clique sur le maximum de tickets ----------------
    while True:
        if adb.is_color_at(
            579,
            700,
            target_color=(199, 155, 53),
            tolerance=10,
        ):
            break
        adb.tap(579, 700)
        print("Clicking for the maximum tickets use")
        time.sleep(0.5)
        
    # ---------------- Clique sur le lancement du niveau avec les tickets ----------------
    print("Starting level with tickets")
    adb.tap(411, 869)
    time.sleep(1)

    # ---------------- Si plus d'act et demande des diamants alors on stop le script ----------------
    diamond_popup = adb.compare_region_with_image(
        reference_image_path=diamond_image_path,
        region=region_diamond,
        threshold=0.9,
    )
    if diamond_popup:
        raise StopScriptException("No more ACT and no more potions")
        
    # ---------------- TANT QUE LES RULSTATS SONT PAS FINI ON CLIQUE----------------
    while True:
        level_finished = adb.compare_region_with_image(
            reference_image_path=rulstats_image_path,
            region=region_rulstats,
            threshold=0.9
        )
        if level_finished:
            print("Level finished")
            break
        adb.tap(397, 116)
        time.sleep(0.5)
        
    # ---------------- Clique sur le bouton retour ----------------
    time.sleep(0.8)
    print("Return")
    adb.tap(43, 29)
    time.sleep(0.5)
    
