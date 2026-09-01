import time

from ... import console, screen

TITLE = "Recycling"

RECYCLED_GRADES = [
    ("recycle_grade_c", "C"),
    ("recycle_grade_uc", "UC"),
    ("recycle_grade_r", "R"),
    ("recycle_grade_sr", "SR"),
]


def recycle_equipement():
    console.banner(TITLE)

    screen.wait_home()

    screen.tap("side_menu")
    time.sleep(1.5)

    print("Recycling")
    screen.tap("recycle_menu")
    time.sleep(1)

    screen.wait("in_menu")

    time.sleep(2)
    print("Configuration recycling")
    screen.tap("recycle_config")

    time.sleep(1.5)
    _configure_grades()
    _configure_options()

    time.sleep(1)
    screen.tap("recycle_save")
    time.sleep(1)

    screen.wait("in_menu", poll=1)

    time.sleep(1.5)
    print("Recycling all items")
    screen.tap("recycle_all")
    time.sleep(1.5)

    if screen.tap_if_color("recycle_high_grade_ok"):
        print("High Grade Items for recycling accepted")
        time.sleep(1)

    _dismiss_results()

    time.sleep(1.5)
    screen.tap("recycle_back")
    time.sleep(1)

    screen.wait("home", poll=1)


def _tap_unless_color(name, tapped_msg, already_msg):
    if screen.is_color(name):
        print(already_msg)
    else:
        print(tapped_msg)
        screen.tap(name)


def _configure_grades():
    for name, label in RECYCLED_GRADES:
        if screen.tap_if_color(name):
            print(f"Grade {label} activated")
        else:
            print(f"Grade {label} already activated")
        time.sleep(1)

    _tap_unless_color("recycle_grade_ssr", "Grade SSR deactivated", "Grade SSR already deactivated")
    time.sleep(1)


def _configure_options():
    _tap_unless_color(
        "recycle_upgrade_items", "Activated upgrade items", "Upgrade items already activated"
    )
    time.sleep(1)

    _tap_unless_color(
        "recycle_select_all", "Activated select all items", "All items already activated"
    )


def _dismiss_results():
    time.sleep(2.5)
    while True:
        with screen.frame():
            if screen.see("in_menu"):
                break
            confirming = screen.is_color("recycle_confirm")
        if confirming:
            screen.tap("recycle_confirm")
            time.sleep(1)
        screen.tap("recycle_dismiss")
        time.sleep(1)
    print("All items are recycled")
