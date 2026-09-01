from ... import console, prompts
from .farm import STATS, claim_last_reward, farm_equipment
from .recycle import recycle_equipement

TITLE = "Equipment Farm"

PIECES_PER_SET = 5

RECYCLE_EVERY = 5


def prepare():
    console.banner(TITLE)

    by_set = prompts.ask_from_list("What do you want to farm?", ["Equipment", "Set"]) == 2

    if by_set:
        sets = prompts.ask_int("How many sets do you want to farm? ")
        levels = sets * PIECES_PER_SET
        print(f" {sets} set(s) to farm, {levels} levels")
    else:
        levels = prompts.ask_int("How many equipments do you want to farm? ")

    labels = [label for label, _ in STATS.values()]
    choice = prompts.ask_from_list("Choice of the equipment to farm:", labels)
    stat = list(STATS)[choice - 1]
    print(f" Selected equipment: {labels[choice - 1]}\n")

    return stat, levels


def run(stat, levels):
    for level in range(1, levels + 1):
        console.banner(TITLE, f"Equipment farm {level} of {levels}")
        farm_equipment(stat, configure=(level == 1))

        if level != levels and level % RECYCLE_EVERY == 0:
            recycle_equipement()

    console.banner(TITLE, "Claiming the last equipment")
    claim_last_reward(stat)

    recycle_equipement()

    print("\nEquipment farm mode completed")
