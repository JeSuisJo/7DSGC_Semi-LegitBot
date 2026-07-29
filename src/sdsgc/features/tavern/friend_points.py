"""Send friendship points to every friend."""

import time

from ... import console, screen

TITLE = "Friends Points"


def send_friends_points(title=TITLE):
    console.banner(title)

    screen.wait_home()

    print("Option")
    screen.tap("friends_option_button")
    time.sleep(1)

    screen.wait("friends_option")

    print("Friends list")
    screen.tap("friends_list")
    time.sleep(1.5)

    # The send button greys out once every friend has been given points.
    screen.tap_until_color("friends_send", "friends_send_exhausted", poll=1)

    screen.tap("friends_send")
    print("Friend points sent")

    time.sleep(1.5)
    screen.tap("friends_return")
