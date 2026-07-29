"""Cook the first available recipe."""

import time

from ... import console, screen

TITLE = "Food preparation"


def food_preparation(title=TITLE):
    console.banner(title)

    screen.wait_home()

    screen.tap("side_menu")
    time.sleep(1.5)

    screen.tap("food_menu")
    time.sleep(1.5)

    screen.wait("in_menu")

    print("Recipe menu")
    time.sleep(2)
    screen.tap("food_recipe_menu")

    screen.wait_color("food_first_recipe")
    print("First recipe")
    screen.tap("food_first_recipe")
    time.sleep(1)

    time.sleep(1.5)
    screen.tap("food_cook")

    # The cook button settles on one of two colours once the batch is done,
    # depending on whether another recipe is still available.
    while True:
        with screen.frame():
            if screen.is_color("food_done_disabled") or screen.is_color("food_done_enabled"):
                break
        time.sleep(1)
    print("Food cook finished")
    time.sleep(1)

    time.sleep(1.5)
    screen.tap("food_back")
    time.sleep(3)
    screen.tap("food_back")

    screen.wait("in_menu")
