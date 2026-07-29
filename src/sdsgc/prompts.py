"""Interactive prompt helpers, one per answer shape."""

from . import console


def ask_int(prompt, minimum=1):
    while True:
        answer = input(f"{prompt}").strip()
        try:
            value = int(answer)
        except ValueError:
            console.error("Please enter a valid number")
            continue
        if value < minimum:
            console.error(f"Please enter a number greater or equal to {minimum}")
            continue
        return value


def ask_from_list(prompt, options):
    """Ask the user to pick one entry from ``options``; returns its 1-based index."""
    print(f"\n{prompt}")
    for i, option in enumerate(options, 1):
        print(f"  [{i}] {option}")
    while True:
        answer = input(f"Choice (1-{len(options)}): ").strip()
        if answer.isdigit() and 1 <= int(answer) <= len(options):
            return int(answer)
        console.error(f"Please enter a number between 1 and {len(options)}")


def ask_choice(prompt, options, default, labels=None):
    """Pick one value from ``options``; an empty answer keeps ``default``.

    ``labels`` renders each option for the user when the stored value is not
    self-explanatory (``"1"`` -> ``"Season 1"``). Returns the option itself.
    """
    shown = labels or options
    print(f"\n{prompt}")
    for i, label in enumerate(shown, 1):
        mark = "  <- default" if options[i - 1] == default else ""
        print(f"  [{i}] {label}{mark}")
    hint = shown[options.index(default)] if default in options else default
    while True:
        answer = input(f"Choice (1-{len(options)}) [{hint}]: ").strip()
        if not answer:
            return default
        if answer.isdigit() and 1 <= int(answer) <= len(options):
            return options[int(answer) - 1]
        console.error(f"Please enter a number between 1 and {len(options)}")


def ask_yes_no(prompt):
    return ask_from_list(prompt, ["Yes", "No"]) == 1


def ask_many_from_list(prompt, options):
    """Ask for several entries, space- or comma-separated; returns a set of indices."""
    print(f"\n{prompt}")
    for i, option in enumerate(options, 1):
        print(f"  [{i}] {option}")
    while True:
        answer = input(f"Choices (1-{len(options)}, e.g. 1,3,5) []: ").strip()
        if not answer:
            return set()
        tokens = answer.replace(",", " ").split()
        if all(t.isdigit() and 1 <= int(t) <= len(options) for t in tokens):
            return {int(t) for t in tokens}
        console.error(f"Please enter numbers between 1 and {len(options)}, separated by spaces")
