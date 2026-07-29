"""Central registry of automation modes shown in the menu."""

from dataclasses import dataclass
from typing import Callable, Optional

from . import daily, demons, equipment, legendary_boss


@dataclass
class Feature:
    label: str
    run: Callable
    # Runs before `run`, after the menu choice; returns the args passed to `run`.
    prepare: Optional[Callable] = None


# Keys are the strings typed at the menu; insertion order defines menu order.
FEATURES = {
    "1": Feature("Daily", daily.run, prepare=daily.prepare),
    "2": Feature("Auto Demon Farm", demons.run, prepare=demons.prepare),
    "3": Feature("Legendary Boss", legendary_boss.run, prepare=legendary_boss.prepare),
    "4": Feature("Equipment Farm", equipment.run, prepare=equipment.prepare),
}
