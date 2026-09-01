from ..features.demons.clear import DEMON_NAMES
from ..features.demons.fight import DEFAULT_DIFFICULTY, DIFFICULTIES
from ..features.demons.stars import STAR_BUTTONS
from ..features.dungeons.yggdrasil import LEVELS, MEMORIES
from ..features.tavern.expeditions import DEFAULT_ITEM, ITEMS

YES, NO = "true", "false"
BOOLEAN = (YES, NO)
BOOLEAN_LABELS = ("Yes", "No")

SALON_DESIGNS = {
    "1": "Season 1",
    "2": "Season 3",
    "3": "4KOA (anime)",
}

DEMONS = tuple(DEMON_NAMES)
DIFFICULTY_OPTIONS = tuple(DIFFICULTIES)
STAR_OPTIONS = tuple(STAR_BUTTONS)
YGGDRASIL_LEVELS = tuple(LEVELS)
YGGDRASIL_MEMORIES = tuple(MEMORIES)
EXPEDITION_ITEMS = tuple(ITEMS)

DEFAULT_DEMON_DIFFICULTY = DEFAULT_DIFFICULTY

DEFAULTS = {
    "device_id": "",
    "salon_design": "1",
    "daily_demon_stars": "1",
    "daily_demon_ticket": NO,
    "daily_use_ticket": NO,
    "yggdrasil_level": "yellow",
    "yggdrasil_memory": "5",
    "expedition_items": DEFAULT_ITEM,
    "only_reward_3v3": NO,
    "pvp_stuff": NO,
}
