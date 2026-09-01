import time

from ... import screen
from ...battle import (
    battle_preparation_auto,
    fight_pve,
    run_battle_preparation_equipment,
)
from ...coords import equipment_images

STATS = {
    "atk": ("Attack", "equipment_stat_atk"),
    "def": ("Defence", "equipment_stat_def"),
    "hp": ("HP", "equipment_stat_hp"),
    "crit_chance": ("Crit Chance", "equipment_stat_crit_chance"),
    "crit_res": ("Crit Resistance", "equipment_stat_crit_res"),
    "recovery": ("Recovery Rate", "equipment_stat_recovery"),
}

STORY_SCROLLS = 4

REWARD_SCALES = (1.0,)


def mission_on_screen(stat):
    images = equipment_images(stat)
    if not images:
        screen.stop(f"No reference image in img/equipement/{stat}/")
    return screen.see_any_at(images, "mission_equipement", scales=REWARD_SCALES)


def open_mission_list(stat):
    screen.wait_home()

    print("Quest Menu")
    screen.tap("menu_quest")
    time.sleep(3)

    print("7DS Quest")
    screen.tap("main_story")
    time.sleep(3)

    for _ in range(STORY_SCROLLS):
        screen.swipe_to("story_scroll_up")
        time.sleep(1)

    label, coord = STATS[stat]
    print(label)
    screen.tap(coord)
    time.sleep(1.5)

    screen.tap("filter_equipement")
    time.sleep(1.5)

    screen.tap("filter_equipement_in_progress")
    time.sleep(3)


def claim_reward():
    screen.tap("mission_equipement")
    time.sleep(2)
    screen.wait("quest_reward")
    time.sleep(1)
    print("Claim Reward")
    screen.tap("unblock")
    screen.wait_template("new_quest_equipement")
    time.sleep(1)
    print("New Quest")
    screen.tap("new_quest_equipement")
    time.sleep(1.5)


def claim_last_reward(stat):
    open_mission_list(stat)

    if not mission_on_screen(stat) or screen.see("not_finish"):
        print("No reward left to claim")
    else:
        claim_reward()

    print("Return to the tavern")
    screen.tap("tavern_return")
    time.sleep(1)


def farm_equipment(stat, configure):
    open_mission_list(stat)

    if mission_on_screen(stat):
        if screen.see("not_finish"):
            screen.tap("mission_equipement")
            time.sleep(1)
        else:
            claim_reward()
            if not mission_on_screen(stat):
                screen.stop("Equipment mission not found after claiming the reward")
            screen.tap("mission_equipement")
    else:
        print("Not found, go to new quest")
        screen.tap("filter_equipement")
        time.sleep(1)
        screen.tap("filter_equipement_start")
        time.sleep(2)

        screen.tap("mission_equipement")
        time.sleep(1)
        screen.tap("filter_equipement")
        time.sleep(1)
        screen.tap("filter_equipement_in_progress")
        time.sleep(2)
        if not mission_on_screen(stat):
            screen.stop("Equipment mission not found after starting it")
        screen.tap("mission_equipement")

    screen.wait("equipment_difficulty_screen")

    print("Last difficulty")
    screen.tap("equipment_last_difficulty")
    time.sleep(1)

    if configure:
        run_battle_preparation_equipment()
    else:
        battle_preparation_auto()
    time.sleep(1)

    fight_pve()
    time.sleep(1)

    screen.tap_until("unblock", "equipment_difficulty_screen")

    print("Return to the tavern")
    screen.tap("tavern_return")
    time.sleep(1)
