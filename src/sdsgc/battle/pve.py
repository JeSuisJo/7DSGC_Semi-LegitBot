import time

from .. import screen


def fight_pve():
    screen.wait_any("pve_end", "pve_end_alt", poll=1)

    print("Repeat end")
    screen.tap("pve_repeat_ok")
    time.sleep(1.5)

    print("Level finished")
    screen.tap("pve_level_ok")
