"""Full daily routine: the eight chores, in order."""

import time

from ... import console, prompts, screen
from .. import demons, dungeons, equipment, pvp, tavern

TITLE = "Daily mode"

PAUSE = 0.5


def _step_demons(title):
    demons.run_daily(title)
    print("Return to the tavern")
    screen.tap("tavern_return")


def _step_pvp(title):
    pvp.daily_3v3(title)
    time.sleep(PAUSE)
    pvp.daily_pvp()


# (label, action) in run order. Step numbers are computed from this list, never
# hardcoded in the actions.
STEPS = [
    ("Collect beer", tavern.collect_beer),
    ("Food preparation", tavern.food_preparation),
    ("Demon villages", _step_demons),
    ("Special dungeon", dungeons.run_special_dungeon),
    ("Yggdrasil", dungeons.run_yggdrasil),
    ("Expeditions", tavern.run_expeditions),
    ("PvP (3v3 + 1v1)", _step_pvp),
    ("Friend points", tavern.send_friends_points),
]


def prepare():
    """Ask which chores to skip; returns the set of done step indices (1-based)."""
    console.banner(TITLE)

    if not prompts.ask_yes_no("Have some daily tasks already been done today?"):
        return (set(),)

    labels = [label for label, _ in STEPS]
    done = prompts.ask_many_from_list("Select the tasks already done (they will be skipped):", labels)
    return (done,)


def run(done=None):
    done = done or set()
    console.banner(TITLE)

    # Always run at every start, never a skippable daily.
    equipment.recycle_equipement()
    time.sleep(PAUSE)

    for index, (label, step) in enumerate(STEPS, 1):
        if index in done:
            print(f"Skipping (already done): {label}")
            continue
        step(f"{TITLE} : {label} {index}/{len(STEPS)}")
        time.sleep(PAUSE)
