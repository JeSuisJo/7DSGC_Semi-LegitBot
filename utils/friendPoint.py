from . import tap, path, wait_for_image, is_color
import time
import os

def send_friends_points():
    os.system('cls')
    print("=" * 50)
    print(" Daily mode : Friends Points 8/8")
    print("=" * 50)
    region_home = (615, 1005, 662, 1041)
    home_image_path = path("img/home.png")
    region_option = (496, 205, 582, 265)
    option_image_path = path("img/friends.png")

    # ---------------- Savoir si on est dans la taverne ----------------
    wait_for_image(home_image_path, region_home, 0.9)

    # ---------------- Aller dans le menu option ----------------
    print("Option")
    tap(644, 1011)
    time.sleep(0.5)

    # ---------------- Savoir si on est dans le menu option ----------------
    wait_for_image(option_image_path, region_option, 0.9)

    # ---------------- Cliquer sur les amis ----------------
    print("Friends list")
    tap(563, 234)
    time.sleep(0.5)

    # ---------------- Que l'ont peux plus envoyé les points ----------------
    while not is_color(392, 916, (114, 114, 114), 10):
        tap(253, 921)
        time.sleep(0.5)

    tap(253, 921)
    print("Friend points sent")

    # ---------------- Retour a la taverne ----------------
    time.sleep(0.5)
    tap(265, 1005)
