import json
import os
import shutil
from collections import Counter
from dataclasses import dataclass

from .. import config as config_module
from .. import console
from ..paths import resolve
from ..prompts import ask_choice
from .defaults import (
    BOOLEAN,
    BOOLEAN_LABELS,
    DEFAULT_DEMON_DIFFICULTY,
    DEFAULTS,
    DEMONS,
    DIFFICULTY_OPTIONS,
    EXPEDITION_ITEMS,
    SALON_DESIGNS,
    STAR_OPTIONS,
    YGGDRASIL_LEVELS,
    YGGDRASIL_MEMORIES,
)

CONFIG_PATH = resolve("config.json")

DIFFICULTIES_KEY = "demon_difficulties"


@dataclass(frozen=True)
class Question:
    key: str
    prompt: str
    options: tuple
    labels: tuple = None

    def ask(self, current):
        default = current if current in self.options else DEFAULTS[self.key]
        return ask_choice(self.prompt, list(self.options), default, self.labels)


QUESTIONS = [
    Question(
        "salon_design",
        "Which tavern style are you using?",
        tuple(SALON_DESIGNS),
        tuple(SALON_DESIGNS.values()),
    ),
    Question("daily_demon_stars", "Star tier for the daily demons?", STAR_OPTIONS),
    Question(
        "daily_demon_ticket",
        "Clear the daily demon villages with auto-clear tickets?",
        BOOLEAN,
        BOOLEAN_LABELS,
    ),
    Question(
        "daily_use_ticket",
        "Spend tickets on the special dungeon and Yggdrasil?",
        BOOLEAN,
        BOOLEAN_LABELS,
    ),
    Question("yggdrasil_level", "Which Yggdrasil level?", YGGDRASIL_LEVELS),
    Question("yggdrasil_memory", "Which Yggdrasil memory floor?", YGGDRASIL_MEMORIES),
    Question("expedition_items", "Which expedition bonus item?", EXPEDITION_ITEMS),
    Question(
        "only_reward_3v3",
        "Claim the 3v3 reward without playing any 3v3 match?",
        BOOLEAN,
        BOOLEAN_LABELS,
    ),
    Question(
        "pvp_stuff",
        "Enter 1v1 PvP with your equipment?",
        BOOLEAN,
        BOOLEAN_LABELS,
    ),
]


def ensure_config():
    existing = _read()

    if existing is None:
        _run(dict(DEFAULTS), QUESTIONS, list(DEMONS), fresh=True)
        return

    config = dict(existing)
    pending = [q for q in QUESTIONS if _value_of(config, q) is None]
    demons = _unset_demons(config)

    if not pending and not demons:
        return

    _run(config, pending, demons, fresh=False)


def _value_of(config, question):
    value = config.get(question.key)
    return value if value in question.options else None


def _unset_demons(config):
    difficulties = config.get(DIFFICULTIES_KEY)
    if not isinstance(difficulties, dict):
        return list(DEMONS)
    return [d for d in DEMONS if difficulties.get(d) not in DIFFICULTY_OPTIONS]


def _run(config, questions, demons, fresh):
    if fresh:
        console.banner(
            "First run: let's create your config.json",
            "Press Enter to keep the value shown in brackets.",
        )
    else:
        console.banner(
            "Your config.json needs a few answers",
            "Press Enter to keep the value shown in brackets.",
        )
        _report(config, questions, demons)

    for question in questions:
        config[question.key] = question.ask(config.get(question.key))

    if demons:
        config.setdefault(DIFFICULTIES_KEY, {})
        _ask_difficulties(config, demons)

    for key, value in DEFAULTS.items():
        config.setdefault(key, value)

    _save(config)
    config_module.reload()
    print(f"\nSaved {CONFIG_PATH}\n")
    input("Press Enter to continue...")


def _report(config, questions, demons):
    for question in questions:
        stored = config.get(question.key)
        if question.key not in config:
            print(f"  {question.key}: missing")
        else:
            print(f"  {question.key}: '{stored}' is not a valid value")
    for demon in demons:
        stored = (config.get(DIFFICULTIES_KEY) or {}).get(demon)
        state = "missing" if stored is None else f"'{stored}' is not a valid difficulty"
        print(f"  {DIFFICULTIES_KEY}.{demon}: {state}")


def _ask_difficulties(config, demons):
    listed = ", ".join(demons)
    difficulty = ask_choice(
        f"Difficulty to fight these demons at ({listed})?",
        list(DIFFICULTY_OPTIONS),
        _usual_difficulty(config),
    )
    for demon in demons:
        config[DIFFICULTIES_KEY][demon] = difficulty


def _usual_difficulty(config):
    settled = [
        value
        for value in (config.get(DIFFICULTIES_KEY) or {}).values()
        if value in DIFFICULTY_OPTIONS
    ]
    if not settled:
        return DEFAULT_DEMON_DIFFICULTY
    return Counter(settled).most_common(1)[0][0]


def _read():
    if not os.path.exists(CONFIG_PATH):
        return None
    try:
        with open(CONFIG_PATH, encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, ValueError):
        backup = f"{CONFIG_PATH}.bak"
        shutil.copyfile(CONFIG_PATH, backup)
        console.warn(f"config.json could not be read, kept a copy as {backup}")
        return None
    return data if isinstance(data, dict) else None


def _save(config):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
        f.write("\n")
