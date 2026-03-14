from . import tap, path, compare_image
import time
import os

def fight_pve():
    region_end = (376, 943, 428, 974)
    region_end_2 = (374, 942, 430, 972)
    end_image_path = path("img/ok-end-level.png")

    # ---------------- ATTENDRE LA FIN DU COMBAT ----------------
    while True:
        if compare_image(end_image_path, region_end, 0.9) or compare_image(end_image_path, region_end_2, 0.9):
            break
        time.sleep(0.5)

    # ---------------- Clique sur le bouton ok de fin de répétition ----------------
    print("Repeat end")
    tap(399, 956)
    time.sleep(1)

    # ---------------- Clique sur le bouton ok de fin de niveau ----------------
    print("Level finished")
    tap(510, 1011)
