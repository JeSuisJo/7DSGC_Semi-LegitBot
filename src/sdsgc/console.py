import os

WIDTH = 50
SEP = "=" * WIDTH


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def banner(title, *lines):
    clear()
    print(SEP)
    print(title)
    for line in lines:
        print(str(line))
    print(SEP)


def error(message):
    print(f"Error: {message}")


def warn(message):
    print(f"Warning: {message}")


def info(message):
    print(message)
