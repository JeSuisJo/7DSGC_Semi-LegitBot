from . import tap, path, wait_for_image, wait_for_color, is_color, compare_image
import time
import os

def run_expeditions():
    os.system('cls')
    print("=" * 50)
    print(" Daily mode : Expeditions 6/8")
    print("=" * 50)

    region_home = (615, 1005, 662, 1041)
    home_image_path = path("img/home.png")
    region_hub = (562, 345, 617, 402)
    hub_image_path = path("img/hub.png")
    expedition_in = (649, 102, 689, 194)
    expedition_in_image_path = path("img/expedition.png")
    reward_expedition_daily = (304, 368, 497, 412)
    reward_expedition_daily_image_path = path("img/reward-expedition-daily.png")
    reward_claim_2_bonus = (308, 195, 494, 234)
    reward_claim_2_bonus_image_path = path("img/reward-claim-2.png")
    reward_claim_1_bonus = (306, 281, 495, 325)
    reward_claim_1_bonus_image_path = path("img/reward-claim-1-bonus.png")
    reward_claim_no_bonus = (306, 395, 499, 437)
    reward_claim_no_bonus_image_path = path("img/reward-claim-no-bonus.png")
    hawk_region = (326, 434, 378, 469)
    hawk_image_path = path("img/hawk.png")

    # ---------------- Savoir si on est dans la taverne ----------------
    wait_for_image(home_image_path, region_home, 0.9)

    # ---------------- Clique sur le bouton menu combat ----------------
    print("Menu")
    tap(738, 745)
    time.sleep(0.5)

    # ---------------- Savoir si on est dans le menu ----------------
    wait_for_image(hub_image_path, region_hub, 0.9)

    # ---------------- Cliquer sur le menu expeditions ----------------
    print("Expeditions")
    tap(563, 351)
    time.sleep(0.5)

    # ---------------- Savoir si on est dans le menu expeditions ----------------
    wait_for_image(expedition_in_image_path, expedition_in, 0.9)

# ---------------- Cliquer si le bouton la recompense est prete- ----------------
    time.sleep(1)
    if is_color(613, 330, (43, 159, 104), 10):
        print("Reward ready")
        tap(614, 331)
        time.sleep(0.5)
        # ---------------- ATTENDRE QUE LE REWARD APPARAISSE (daily) ----------------
        wait_for_image(reward_expedition_daily_image_path, reward_expedition_daily, 0.9)
        time.sleep(1)
        tap(614, 331)

    time.sleep(0.5)

# ---------------- Cliquer si le bouton tous terminier est prete ----------------
    if is_color(586, 915, (43, 163, 106), 10):
        print("All finished")
        tap(586, 915)
        time.sleep(1)
        # ---------------- ATTENDRE QUE LE REWARD APPARAISSE ----------------
        while True:
            # ---------------- SI 2 REWARD SPECIAL MISSON ----------------
            if compare_image(reward_claim_2_bonus_image_path, reward_claim_2_bonus, 0.9):
                time.sleep(1)
                tap(586, 915)
                break

            # ---------------- SI 1 REWARD  SPECIAL MISSON ----------------
            if compare_image(reward_claim_1_bonus_image_path, reward_claim_1_bonus, 0.9):
                time.sleep(1)
                tap(586, 915)
                break

            # ---------------- SI REWARD BASIQUE ----------------
            if compare_image(reward_claim_no_bonus_image_path, reward_claim_no_bonus, 0.9):
                time.sleep(1)
                tap(586, 915)
                break

        time.sleep(0.5)

# ---------------- Cliquer si l'équipe peut etre definie ----------------
    if is_color(358, 912, (3, 111, 121), 10):
        print("Sending team")
        tap(358, 912)
        time.sleep(0.5)
        # ---------------- Confirmer l'envoi de l'équipe ----------------
        wait_for_color(469, 909, (43, 160, 103), 10)
        print("Team sent")
        tap(469, 909)
        # ---------------- Attendre que le hawk apparaisse ----------------
        wait_for_image(hawk_image_path, hawk_region, 0.9)
        tap(469, 909)

    # ---------------- Savoir si tous fini ----------------
    wait_for_image(home_image_path, region_home, 0.9)

    # ---------------- Retoure a la taverne ----------------
    time.sleep(0.5)
    tap(162, 1014)
