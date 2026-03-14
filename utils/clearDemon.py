from . import tap, path, is_color, compare_image
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

def detect_demons_in_villages():
    # ---------------- Savoir si le achevement multiple est activé ----------------
    if is_color(561, 268, (76, 59, 35), 10):
        print("Activated achievement auto")
        tap(561, 268)
        time.sleep(0.5)

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

    for village_num in range(1, 7):
        region = village_regions[village_num]
        village_folder = f"img/village-demon/village-{village_num}"

        best_match = None
        for demon_name in demon_names:
            demon_image_path = path(f"{village_folder}/{demon_name}.png")
            if compare_image(demon_image_path, region, 0.9):
                best_match = demon_name
                break

        detected_demons[village_num] = best_match
        print(f"Village {village_num}: {best_match if best_match else 'No demon detected'}")

    return detected_demons


def clear_demons(target_demons=None):
    from .fightDemon import fight_demon

    # 1) Détecter les démons dans tous les villages (scan initial unique)
    detected = detect_demons_in_villages()

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
            tap(click_x, click_y)
            time.sleep(0.5)

            # 5) Lancer le combat contre ce démon
            fight_demon(demon_name)

    print("\nAll demons cleared!")
