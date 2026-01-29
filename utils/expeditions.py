from utils.adb_helper import auto_setup_adb
import time
import os
from utils.adb_helper import get_project_path

def run_expeditions():
    # Configuration automatique de ADB
    adb = auto_setup_adb(verbose=True)
    os.system('cls')
    print("=" * 50)
    print(" Daily mode : Expeditions 6/8")
    print("=" * 50)

    region_home = (615, 1005, 662, 1041)
    home_image_path = get_project_path("img/home.png")
    region_hub = (562, 345, 617, 402)
    hub_image_path = get_project_path("img/hub.png")
    expedition_in = (649, 102, 689, 194)
    expedition_in_image_path = get_project_path("img/expedition.png")
    reward_expedition_daily = (304, 368, 497, 412)
    reward_expedition_daily_image_path = get_project_path("img/reward-expedition-daily.png")
    reward_claim_2_bonus = (308, 195, 494, 234)
    reward_claim_2_bonus_image_path = get_project_path("img/reward-claim-2.png")
    reward_claim_1_bonus = (306, 281, 495, 325)
    reward_claim_1_bonus_image_path = get_project_path("img/reward-claim-1-bonus.png")
    reward_claim_no_bonus = (306, 395, 499, 437)
    reward_claim_no_bonus_image_path = get_project_path("img/reward-claim-no-bonus.png")
    hawk_region = (326, 434, 378, 469)
    hawk_image_path = get_project_path("img/hawk.png")


    # ---------------- Savoir si on est dans la taverne ----------------
    while True:
        at_tavern = adb.compare_region_with_image(
            reference_image_path=home_image_path,
            region=region_home,
            threshold=0.9,
        )
        if at_tavern:
            break
        time.sleep(0.5)

    # ---------------- Clique sur le bouton menu combat ----------------
    print("Menu")
    adb.tap(738, 745)
    time.sleep(0.5)

    # ---------------- Savoir si on est dans le menu ----------------
    while True:
        in_hub = adb.compare_region_with_image(
            reference_image_path=hub_image_path,
            region=region_hub,
            threshold=0.9,
        )
        if in_hub:
            break
        time.sleep(0.5)

    # ---------------- Cliquer sur le menu expeditions ----------------
    print("Expeditions")
    adb.tap(563, 351)
    time.sleep(0.5)

    # ---------------- Savoir si on est dans le menu expeditions ----------------
    while True:
        in_expedition_menu = adb.compare_region_with_image(
            reference_image_path=expedition_in_image_path,
            region=expedition_in,
            threshold=0.9,
        )
        if in_expedition_menu:
            break
        time.sleep(0.5)

# ---------------- Cliquer si le bouton la recompense est prete- ----------------
    time.sleep(1)
    reward_color = adb.get_color_at(613, 330, target_color=(43, 159, 104), tolerance=10)
    if reward_color:
        print("Reward ready")
        adb.tap(614, 331)
        time.sleep(0.5)
        while True:
            reward_expedition_ready = adb.compare_region_with_image(
                reference_image_path=reward_expedition_daily_image_path,
                region=reward_expedition_daily,
                threshold=0.9,
            )
            if reward_expedition_ready:
                time.sleep(1)
                adb.tap(614, 331)
                break

            time.sleep(0.5)

    time.sleep(0.5)

# ---------------- Cliquer si le bouton tous terminier est prete ----------------
    color_all_finished = adb.get_color_at(
        586, 915,
        target_color=(43, 163, 106),
        tolerance=10,
    )
    if color_all_finished:
        print("All finished")
        adb.tap(586, 915)
        time.sleep(1)
        # ---------------- ATTENDRE QUE LE REWARD APPARAISSE ----------------
        while True:
            # ---------------- SI 2 REWARD SPECIAL MISSON ----------------
            reward_2_bonus = adb.compare_region_with_image(
                reference_image_path=reward_claim_2_bonus_image_path,
                region=reward_claim_2_bonus,
                threshold=0.9,
            )
            if reward_2_bonus:
                time.sleep(1)
                adb.tap(586, 915)
                break

            # ---------------- SI 1 REWARD  SPECIAL MISSON ----------------
            reward_1_bonus = adb.compare_region_with_image(
                reference_image_path=reward_claim_1_bonus_image_path,
                region=reward_claim_1_bonus,
                threshold=0.9,
            )
            if reward_1_bonus:
                time.sleep(1)
                adb.tap(586, 915)
                break

            # ---------------- SI REWARD BASIQUE ----------------
            reward_no_bonus = adb.compare_region_with_image(
                reference_image_path=reward_claim_no_bonus_image_path,
                region=reward_claim_no_bonus,
                threshold=0.9,
            )
            if reward_no_bonus:
                time.sleep(1)
                adb.tap(586, 915)
                break

        time.sleep(0.5)

# ---------------- Cliquer si l'équipe peut etre definie ----------------
    color_defined_team = adb.get_color_at(
        358, 912,
        target_color=(3, 111, 121),
        tolerance=10,
    )
    if color_defined_team:
        print("Sending team")
        adb.tap(358, 912)
        time.sleep(0.5)
        # ---------------- Confirmer l'envoi de l'équipe ----------------
        while not adb.get_color_at(469, 909, target_color=(43, 160, 103), tolerance=10):
            time.sleep(0.5)
        print("Team sent")
        adb.tap(469, 909)
        # ---------------- Attendre que le hawk apparaisse ----------------
        while True:
            hawk_visible = adb.compare_region_with_image(
                reference_image_path=hawk_image_path,
                region=hawk_region,
                threshold=0.9,
            )
            if hawk_visible:
                adb.tap(469, 909)
                break
            time.sleep(0.5)

    # ---------------- Savoir si tous fini ----------------
    while True:
        at_tavern = adb.compare_region_with_image(
            reference_image_path=home_image_path,
            region=region_home,
            threshold=0.9,
        )
        if at_tavern:
            break
        time.sleep(0.5)
        
    # ---------------- Retoure a la taverne ----------------
    time.sleep(0.5)
    adb.tap(162, 1014)
