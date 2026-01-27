from .adb_helper import auto_setup_adb, get_project_path, ADBHelper
from collections import Counter
import time
import os

# Coordonnées pour chaques villages
VILLAGE_CLICK_COORDS = {
    1: (200, 450),
    2: (393, 456),
    3: (595, 450),
    4: (197, 620),
    5: (399, 611),
    6: (595, 623),
}

def detect_demons_in_villages(adb=None):
    # ---------------- Savoir si le achevement multiple est activé ----------------
    if adb.is_color_at(
        561, 268,
        target_color=(76, 59, 35),
        tolerance=10
    ):
        print("Activated achievement auto")
        adb.tap(561, 268)
        time.sleep(0.5)

    if adb is None:
        adb = auto_setup_adb(verbose=False)
    
    temp_screenshot = "temp_demon_scan.png"
    if not adb.screenshot(temp_screenshot):
        print("Error: Could not take screenshot")
        return {}
    
    # Liste des démons possibles
    demon_names = ['bellmoth', 'grey', 'howlex', 'indura', 'red', 'original_demon']
    
    # Régions pour chaque village
    village_regions = {
        1: (189, 397, 221, 429),
        2: (375, 400, 419, 432),
        3: (575, 400, 611, 429),
        4: (187, 563, 223, 598),
        5: (379, 563, 420, 597),
        6: (575, 563, 612, 595)
    }
    
    detected_demons = {}
    
    try:
        # Pour chaque village
        for village_num in range(1, 7):
            region = village_regions[village_num]
            village_folder = f"img/village-demon/village-{village_num}"
            
            best_match = None
            best_similarity = 0.0
            
            # Tester chaque démon possible
            for demon_name in demon_names:
                demon_image_path = get_project_path(f"{village_folder}/{demon_name}.png")
                
                # Comparer la région avec l'image du démon (réutilise le screenshot)
                is_match, similarity = adb.compare_region_with_image(
                    reference_image_path=demon_image_path,
                    region=region,
                    threshold=0.9,
                    screenshot_path=temp_screenshot  # Réutilise le screenshot existant
                )
                
                # Garder le meilleur match
                if similarity > best_similarity:
                    best_similarity = similarity
                    if is_match:
                        best_match = demon_name
                        # OPTIONNEL: Arrêter dès qu'on trouve un match (plus rapide)
                        # break
            
            # Si un match a été trouvé (au-dessus du seuil)
            if best_match and best_similarity >= 0.9:
                detected_demons[village_num] = best_match
                print(f"Village {village_num}: {best_match}")
            else:
                detected_demons[village_num] = None
                print(f"Village {village_num}: No demon detected")
    
    finally:
        # Nettoyer le screenshot temporaire
        import os
        resolved_path = adb._resolve_path(temp_screenshot)
        if os.path.exists(resolved_path):
            try:
                os.remove(resolved_path)
            except:
                pass
    
    return detected_demons


def clear_demons(adb=None, target_demons=None):
    if adb is None:
        adb = auto_setup_adb(verbose=False)
    
    # Import de fightDemon
    from .fightDemon import fight_demon
    
    # 1) Détecter les démons dans tous les villages (scan initial unique)
    detected = detect_demons_in_villages(adb)
    
    # 2) Filtrer éventuellement sur certains démons
    if target_demons:
        filtered = {
            village_num: demon_name
            for village_num, demon_name in detected.items()
            if demon_name in target_demons
        }
    else:
        # Garder seulement les villages où un démon a été détecté
        filtered = {v: d for v, d in detected.items() if d is not None}
    
    if not filtered:
        print("\nNo demons detected to clear.")
        return
    
    # 3) Compter les occurrences de chaque démon
    counts = Counter(filtered.values())
    # Trier les démons du plus fréquent au moins fréquent
    ordered_demons = [name for name, _ in counts.most_common()]
    
    # 4) Pour chaque démon unique (dans l'ordre de fréquence)
    for demon_name in ordered_demons:
        # Trouver le PREMIER village où ce démon apparaît
        village_to_click = None
        for village_num, demon_name_detected in filtered.items():
            if demon_name_detected == demon_name:
                village_to_click = village_num
                break
        
        if village_to_click:
            os.system('cls')
            print("=" * 50)
            print(f" Clear demons : {demon_name}")
            print("=" * 50)
            click_x, click_y = VILLAGE_CLICK_COORDS[village_to_click]
            adb.tap(click_x, click_y)
            time.sleep(0.5)
            
            # 5) Lancer le combat contre ce démon
            fight_demon(adb, demon_name)
    
    print("\nAll demons cleared!")