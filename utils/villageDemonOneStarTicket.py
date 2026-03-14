from . import tap, path, stop, is_color, compare_image, wait_for_color
import time
import os

region_home = (615, 1005, 662, 1041)
home_image_path = path("img/home.png")

def village_demon_one_star_ticket():
    os.system('cls')
    print("=" * 50)
    print(" Auto demon farm mode")
    print("=" * 50)

    # ---------------- Savoir si le achevement multiple est activé ----------------
    if is_color(648, 262, (114, 91, 58), 10):
        print("Activated achievement auto")
        tap(648, 262)
        time.sleep(0.5)

    # ---------------- Cliquer sur le les demons 1 etoile ----------------
    tap(241, 363)
    time.sleep(1)

    # ---------------- Check les 6 villages si il y a l'achevement multiple activé dessus ----------------
    # Village 1
    if not is_color(200, 414, (235, 204, 49), 10):
        print("Activated achievement auto")
        tap(200, 414)
        time.sleep(0.5)
    else:
        time.sleep(0.5)

    # Village 2
    if not is_color(395, 414, (233, 200, 45), 10):
        print("Activated achievement auto")
        tap(395, 414)
        time.sleep(0.5)
    else:
        time.sleep(0.5)

    # Village 3
    if not is_color(588, 414, (236, 205, 51), 10):
        print("Activated achievement auto")
        tap(588, 414)
        time.sleep(0.5)
    else:
        time.sleep(0.5)

    # Village 4
    if not is_color(201, 578, (251, 239, 79), 10):
        print("Activated achievement auto")
        tap(201, 578)
        time.sleep(0.5)
    else:
        time.sleep(0.5)

    # Village 5
    if not is_color(395, 579, (241, 215, 58), 10):
        print("Activated achievement auto")
        tap(395, 579)
        time.sleep(0.5)
    else:
        time.sleep(0.5)

    # Village 6
    if not is_color(590, 579, (241, 217, 61), 10):
        print("Activated achievement auto")
        tap(590, 579)
        time.sleep(0.5)
    else:
        time.sleep(0.5)

    # ---------------- Faire l'achevement auto ----------------
    print("Clear all 6 villages")
    tap(402, 894)
    time.sleep(2)

    # ---------------- Savoir si on a plus de potions  ----------------
    if compare_image(home_image_path, region_home, 0.9):
        stop("No more ACT and no more potions")

    # ---------------- Attendre la fin du clear ----------------
    wait_for_color(455, 959, (46, 167, 113), 10)
    print("Clear finished")
    tap(455, 959)
    time.sleep(0.5)
