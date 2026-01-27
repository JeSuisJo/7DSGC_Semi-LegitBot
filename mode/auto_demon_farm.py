from utils.adb_helper import auto_setup_adb
import time
import os
from utils.villageDemonOneStar import village_demon_one_star
from utils.villageDemonOneStarTicket import village_demon_one_star_ticket
from utils.goToBossMenu import go_to_boss_menu
from utils.clearDemon import clear_demons

def run_auto_demon_farm():
    # Configuration automatique de ADB
    adb = auto_setup_adb(verbose=True)
    os.system('cls')
    print("=" * 50)
    print(" Auto demon farm mode")
    print("=" * 50)
    
    # ---------------- Choix entre farm avec ou sans ticket ----------------
    print("Do you want to farm with ticket?")
    print("1 : Yes")
    print("2 : No")
    while True:
        try:
            ticket_choice = input("Your choice (1-2): ").strip()
            ticket_choice = int(ticket_choice)
            if ticket_choice == 1 or ticket_choice == 2:
                break
            else:
                print("Please enter 1 or 2")
        except ValueError:
            print("Please enter a valid number")
    

    # ---------------- Choix du nombre de fois à farmer ----------------
    while True:
        try:
            num_times = int(input("How many times do you want to farm? ").strip())
            if num_times >= 1:
                break
            else:
                print("Please enter a number greater or equal to 1")
        except ValueError:
            print("Please enter a valid number")

    # ---------------- Aller au menu des démons ----------------
    go_to_boss_menu()
    time.sleep(0.5)
    
    # ---------------- Boucle de farm ----------------
    for i in range(1, num_times + 1):
        os.system('cls')
        print("=" * 50)
        print(" Auto demon farm mode")
        print("=" * 50)
        if ticket_choice == 1:
            village_demon_one_star_ticket()
            time.sleep(0.5)
            clear_demons()
        else:
            village_demon_one_star()   
            time.sleep(0.5)
            clear_demons()

