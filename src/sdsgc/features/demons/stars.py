from ... import screen

STAR_BUTTONS = {
    "1": "demon_stars_1",
    "2": "demon_stars_2",
    "3": "demon_stars_3",
}


def select_stars(stars):
    name = STAR_BUTTONS.get(str(stars))
    if name:
        screen.tap(name)


def star_mode(stars):
    return "one_star" if str(stars) == "1" else "multi_star"
