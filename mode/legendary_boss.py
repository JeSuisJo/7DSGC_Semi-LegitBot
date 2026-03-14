from utils import tap, path, stop, compare_image
import time
import os

def run_legendary_boss():
    region_potion = (365, 333, 429, 411)
    potion_image_path = path("img/act.png")
    region_auto = (644, 17, 674, 47)
    auto_image_path = path("img/auto.png")
    region_in_battle = (753, 15, 783, 46)
    in_battle_image_path = path("img/in-battle.png")
    region_finish = (637, 1006, 666, 1026)
    finish_image_path = path("img/end.png")
    region_loss = (639, 993,668, 1015)
    loss_image_path = path("img/loss.png")

    os.system('cls')
    print("=" * 50)
    print(" Legendary boss farming")
    print("=" * 50)

    # ---------------- Demande combien de fois il veut farm ----------------
    while True:
        try:
            num_times = int(input("How many times do you want to farm? ").strip())
            if num_times >= 1:
                break
            else:
                print("Please enter a number greater or equal to 1")
        except ValueError:
            print("Please enter a valid number")

    # ---------------- Lancer le boss ----------------
    time.sleep(0.5)
    print("Launching the boss")
    tap(402, 1017)
    time.sleep(0.8)

    # ---------------- Si il y a plus de stam ----------------
    time.sleep(1.5)
    no_more_act = compare_image(potion_image_path, region_potion, 0.9)
    if no_more_act:
        print("No stamina, refill potions")
        tap(399, 805)
        time.sleep(1)
        print("Restarting the boss")
        tap(402, 1017)
        time.sleep(1.7)

    # ---------------- Boucle de farm ----------------
    for i in range(1, num_times + 1):
        while True:
            os.system('cls')
            print("=" * 50)
            print(f" Farming the boss {num_times} times")
            print("=" * 50)
            print(f"Run {i}/{num_times}")

            time.sleep(1)
            # ---------------- Savoir si on a plus d'act ----------------
            no_more_act = compare_image(potion_image_path, region_potion, 0.9)
            if no_more_act:
                print("No stamina, refill potions")
                tap(399, 805)
                time.sleep(1)

            # ---------------- Savoir si ont est dans le combat ----------------
            in_battle = compare_image(in_battle_image_path, region_in_battle, 0.9)
            if in_battle:
                break
            tap(402, 1055)
            time.sleep(0.5)
        
        while True:
            # ---------------- Savoir si le bouton relancer est la ----------------
            in_battle = compare_image(finish_image_path, region_finish, 0.9)
            if in_battle:
                if i == num_times:
                    print("Finished farming the boss")
                    time.sleep(0.5)
                    tap(507, 1011)
                    break

                print("Restarting the boss")
                tap(288, 1002)
                time.sleep(0.8)
                break

            auto = compare_image(auto_image_path, region_auto, 0.98)
            if auto:
                tap(659, 24)
                time.sleep(0.8)
        
            tap(402, 1055)

            # ---------------- Savoir si on a perdue ----------------
            loss = compare_image(loss_image_path, region_loss, 0.9)
            if loss:
                stop("Defeat")
            time.sleep(0.5)
