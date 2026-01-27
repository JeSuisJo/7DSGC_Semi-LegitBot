from .adb_helper import auto_setup_adb, ADBHelper, get_project_path, StopScriptException, KeyCode
import time
import os

def run_battle_preparation_equipement():
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
    print("Battle preparation configuration")
    adb.tap(142, 1018)
    
    # ---------------- Savoir si on est dans la configuration du mode automatique avec la recherche du bouton ok ----------------
    while True:
        ok_color = adb.get_color_at(
            453, 754,
            target_color=(45, 169, 116),
            tolerance=10
        )
        if ok_color:
            break
        time.sleep(0.5)
    
    # ---------------- Check des utilisation des potions automatiques ----------------
    while True:
        potions_color = adb.get_color_at(239, 624)
        
        if potions_color:
            # Si les potions automatiques est désactivé
            if ADBHelper.color_matches(potions_color, color_options_disabled, tolerance):
                adb.tap(239, 624)
                print("Potions automatically activated")
                break
            
            # Si les potions automatiques est activé
            elif ADBHelper.color_matches(potions_color, color_options_enabled, tolerance):
                print("Potions already activated")
                break
        
        time.sleep(0.5)
    
    # ---------------- Check des répétitions du niveau ----------------
    while True:
        level_repetitions_color = adb.get_color_at(239, 419)
        
        if level_repetitions_color:
            # Si la répétition du niveau est désactivé pour x fois
            if ADBHelper.color_matches(level_repetitions_color, color_options_disabled, tolerance):
                adb.tap(239, 419)
                time.sleep(0.5)
                adb.tap(493, 413)
                time.sleep(0.5)
                # Supprimer le premier caractère
                adb.input_keyevent(KeyCode.DELETE)
                time.sleep(0.3)
                # Supprimer le deuxième caractère
                adb.input_keyevent(KeyCode.DELETE)
                time.sleep(0.3)
                # Écrire "8"
                adb.input_text("8")
                print("Level repetitions set to 8")
                break
            
            # Si la répétition du niveau est activé pour x fois
            elif ADBHelper.color_matches(level_repetitions_color, color_options_enabled, tolerance):
                adb.tap(493, 413)
                time.sleep(0.5)
                # Supprimer le premier caractère
                adb.input_keyevent(KeyCode.DELETE)
                time.sleep(0.3)
                # Supprimer le deuxième caractère
                adb.input_keyevent(KeyCode.DELETE)
                time.sleep(0.3)
                # Écrire "8"
                adb.input_text("8")
                # Appuyer sur enter
                adb.input_keyevent(KeyCode.ENTER)
                time.sleep(0.3)
                print("Level repetitions set to 8")
                break
        
        time.sleep(0.5)
    
    # ---------------- Sauvegarde de la configuration automatique ----------------
    time.sleep(0.5)
    print("Saving configuration")
    adb.tap(453, 754)
    
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

