from . import tap, path, wait_for_image, swipe, compare_image
from .fightDemon import load_config
import time
import os

def collect_beer():
    config = load_config()
    salon_design = config.get("salon_design")
    region_in_menu = (4, 9, 60, 62)
    in_menu_image_path = path("img/return.png")
    region_home = (615, 1005, 662, 1041)
    home_image_path = path("img/home.png")

    os.system('cls')
    print("=" * 50)
    print(" Daily mode : Collect Beer 1/8")
    print("=" * 50)

    # ---------------- Si on est dans le salon de la saison 1 ----------------
    if salon_design == "1":
        wait_for_image(home_image_path, region_home, 0.9)

        print("Going to the beer")
        tap(54, 894)
        time.sleep(1)

        tap(60, 558)
        time.sleep(0.5)

        wait_for_image(in_menu_image_path, region_in_menu, 0.9)

        time.sleep(1)
        tap(37, 29)
        time.sleep(1)

        tap(110, 392)
        time.sleep(1)

        while True:
            if compare_image(home_image_path, region_home, 0.9):
                print("Beer collected")
                break
            tap(387, 120)
            time.sleep(0.5)

    # ---------------- Si on est dans le salon de la saison 3 ----------------
    elif salon_design == "2":
        wait_for_image(home_image_path, region_home, 0.9)

        print("Going to the beer")
        tap(54, 894)
        time.sleep(1)

        tap(54, 731)
        time.sleep(0.5)

        wait_for_image(in_menu_image_path, region_in_menu, 0.9)

        time.sleep(2)
        tap(37, 29)
        time.sleep(0.5)

        swipe(408, 693, 43, 693, 800)
        time.sleep(0.5)

        tap(276, 336)
        time.sleep(0.2)
        tap(335, 336)
        time.sleep(0.5)

        while True:
            if compare_image(home_image_path, region_home, 0.9):
                print("Beer collected")
                break
            tap(387, 120)
            time.sleep(0.5)

    # ---------------- Si on est dans le salon de l'anime 4KOA ----------------
    elif salon_design == "3":
        wait_for_image(home_image_path, region_home, 0.9)

        print("Going to the beer")
        tap(54, 894)
        time.sleep(1)

        tap(57, 322)
        time.sleep(0.5)

        wait_for_image(in_menu_image_path, region_in_menu, 0.9)

        time.sleep(1)
        tap(37, 29)
        time.sleep(0.5)

        swipe(422, 652, 16, 652, 1000)
        time.sleep(1)

        print("Collecting beer")
        tap(212, 503)
        time.sleep(1)

        while True:
            if compare_image(home_image_path, region_home, 0.9):
                print("Beer collected")
                break
            tap(387, 120)
            time.sleep(0.5)
