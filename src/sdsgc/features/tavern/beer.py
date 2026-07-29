"""Collect the tavern beer.

The beer sits in a different spot in each salon design, so the walk there is
per-design; everything after it is shared.
"""

import time

from ... import console, screen
from ...config import get_config

TITLE = "Collect Beer"


def collect_beer(title=TITLE):
    console.banner(title)
    design = str(get_config().get("salon_design"))

    walk = {
        "1": _season_1,
        "2": _season_3,
        "3": _anime,
    }.get(design)

    if walk is None:
        print(f"Unknown salon_design '{design}', skipping beer")
        return

    screen.wait_home()
    print("Going to the beer")
    screen.tap("beer_side_menu")
    time.sleep(1.5)

    walk()
    _dismiss()


def _season_1():
    screen.tap("beer_menu_season_1")
    time.sleep(1)
    screen.wait("in_menu")
    time.sleep(1.5)
    screen.tap("beer_back")
    time.sleep(1.5)
    screen.tap("beer_collect_season_1")
    time.sleep(1.5)


def _season_3():
    screen.tap("beer_menu_season_3")
    time.sleep(1)
    screen.wait("in_menu")
    time.sleep(2)
    screen.tap("beer_back")
    time.sleep(1)
    screen.swipe_to("beer_scroll_season_3")
    time.sleep(1)
    screen.tap("beer_collect_season_3")
    time.sleep(0.5)
    screen.tap("beer_collect_season_3_confirm")
    time.sleep(1)


def _anime():
    screen.tap("beer_menu_anime")
    time.sleep(1)
    screen.wait("in_menu")
    time.sleep(1.5)
    screen.tap("beer_back")
    time.sleep(1)
    screen.swipe_to("beer_scroll_anime")
    time.sleep(1.5)
    print("Collecting beer")
    screen.tap("beer_collect_anime")
    time.sleep(1.5)


def _dismiss():
    screen.tap_until("beer_dismiss", "home")
    print("Beer collected")
