from dataclasses import dataclass
from typing import Callable, Optional

from . import daily, demons, equipment, legendary_boss


@dataclass
class Feature:
    label: str
    run: Callable
    prepare: Optional[Callable] = None


FEATURES = {
    "1": Feature("Daily", daily.run, prepare=daily.prepare),
    "2": Feature("Auto Demon Farm", demons.run, prepare=demons.prepare),
    "3": Feature("Legendary Boss", legendary_boss.run, prepare=legendary_boss.prepare),
    "4": Feature("Equipment Farm", equipment.run, prepare=equipment.prepare),
}
