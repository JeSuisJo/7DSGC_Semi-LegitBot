import time

from ... import console, screen
from .clear import villages_to_farm
from .cycle import cycle_village, skip_village
from .stars import select_stars, star_mode


def run_villages(stars, title, skip_done=False):
    console.banner(title)

    select_stars(stars)
    time.sleep(1.5)

    if screen.is_color("auto_achievement_enabled"):
        print("Deactivated achievement auto")
        screen.tap("auto_achievement_enabled")
        time.sleep(1)

    free = villages_to_farm(skip_done)
    if free is None:
        print("Every village is already finished, nothing to farm")
        return False
    if not free:
        print("Every village already holds a demon, nothing to farm")
        return True

    mode = star_mode(stars)
    first, last = free[0], free[-1]

    print(f"Village {first}")
    screen.tap(f"village_{first}_enter")
    time.sleep(1)
    cycle_village(mode, configure=True)
    time.sleep(1)

    for village in range(first + 1, last + 1):
        console.banner(title)
        print(f"Village {village}")
        screen.tap("village_next")
        time.sleep(1)
        if village in free:
            cycle_village(mode, configure=False)
        else:
            skip_village()

    print("Return to the boss menu")
    screen.tap("boss_menu_return")
    time.sleep(1)
    return True
