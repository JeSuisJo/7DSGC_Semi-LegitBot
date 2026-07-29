"""Star-difficulty selection on the village list."""

from ... import screen

STAR_BUTTONS = {
    "1": "demon_stars_1",
    "2": "demon_stars_2",
    "3": "demon_stars_3",
}


def select_stars(stars):
    """Tap the star filter. Unknown values are left alone."""
    name = STAR_BUTTONS.get(str(stars))
    if name:
        screen.tap(name)


def star_mode(stars):
    """One-star villages put the last difficulty lower on screen than the
    two/three-star ones, so the two layouts are named rather than compared."""
    return "one_star" if str(stars) == "1" else "multi_star"
