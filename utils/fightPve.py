from .adb_helper import auto_setup_adb, ADBHelper, get_project_path, StopScriptException
import time
import os

def fight_pve():
    # Configuration automatique de ADB
    adb = auto_setup_adb(verbose=False)
    
    region_end = (376, 943, 428, 974) 
    region_end_2 = (374, 942, 430, 972)
    end_image_path = get_project_path("img/ok-end-level.png")
    
    # ---------------- ATTENDRE LA FIN DU COMBAT ----------------
    while True:
        level_end_visible = adb.compare_region_with_image(
            reference_image_path=end_image_path,
            region=region_end,
            threshold=0.9,
        )
        level_end_visible_2 = adb.compare_region_with_image(
            reference_image_path=end_image_path,
            region=region_end_2,
            threshold=0.9,
        )
        if level_end_visible or level_end_visible_2:
            break
        
        time.sleep(0.5)

    # ---------------- Clique sur le bouton ok de fin de répétition ----------------
    print("Repeat end")
    adb.tap(399, 956)
    time.sleep(1)

    # ---------------- Clique sur le bouton ok de fin de niveau ----------------
    print("Level finished")
    adb.tap(510, 1011)
