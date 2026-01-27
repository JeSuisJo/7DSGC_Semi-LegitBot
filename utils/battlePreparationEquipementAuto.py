from .adb_helper import auto_setup_adb, ADBHelper, get_project_path, StopScriptException, KeyCode
import time
import os

def battle_preparation_equipement_auto():
    # Configuration automatique de ADB
    adb = auto_setup_adb(verbose=False)
    
    region_prep = (175, 997, 218, 1032)
    prep_image_path = get_project_path("img/prep.png")
    color_options_disabled = (54, 48, 39)
    color_options_enabled = (236, 203, 46)
    tolerance = 10
    region_potion = (365, 333, 429, 411)
    potion_image_path = get_project_path("img/act.png")
    region_diamond = (363, 662, 425, 698)
    diamond_image_path = get_project_path("img/diamond.png")
    
    # ---------------- Savoir si on est dans la preparation du combat ----------------
    while True:
        is_match, similarity = adb.compare_region_with_image(
            reference_image_path=prep_image_path,
            region=region_prep,
            threshold=0.9
        )
        
        if is_match:
            break
        
        time.sleep(0.5)
    
    # ---------------- Clique sur la configuration du mode automatique ----------------
    print("Auto mode")
    adb.tap(194, 1017)
    time.sleep(0.5)

    # ---------------- Lancement du combat ----------------
    time.sleep(0.8)
    print("Starting battle")
    adb.tap(406, 1016)
    time.sleep(1.7)
    
    # ---------------- Si plus d'act alors mettre des potions ----------------
    is_match, similarity = adb.compare_region_with_image(
        reference_image_path=potion_image_path,
        region=region_potion,
        threshold=0.9
    )
    
    if is_match:
        print("No more ACT, refill potions")
        adb.tap(399, 805)
        time.sleep(0.7)
        print("Restarting battle")
        adb.tap(406, 1016)
        
    # ---------------- Si plus d'act et demande des diamants alors on stop le script ----------------   
    is_match, similarity = adb.compare_region_with_image(
        reference_image_path=diamond_image_path,
        region=region_diamond,
        threshold=0.9
    )
    
    if is_match:
        raise StopScriptException("No more ACT and no more potions")

