import glob
import json
import os
from functools import lru_cache

from .paths import resolve

_COORDS_DIR = resolve("coords")


def _load():
    merged = {}
    origin = {}
    for path in sorted(glob.glob(os.path.join(_COORDS_DIR, "*.json"))):
        filename = os.path.basename(path)
        with open(path, encoding="utf-8") as f:
            entries = json.load(f)
        for name, block in entries.items():
            if name in merged:
                raise ValueError(
                    f"Duplicate coord '{name}' defined in both "
                    f"'{origin[name]}' and '{filename}'"
                )
            merged[name] = block
            origin[name] = filename
    return merged


_COORDS = _load()


def coords(name):
    try:
        return _COORDS[name]
    except KeyError as exc:
        raise KeyError(f"Unknown coord '{name}' (not defined in coords/*.json)") from exc


_EQUIPMENT_IMAGES = "img/equipement"


@lru_cache(maxsize=None)
def equipment_images(stat):
    folder = f"{_EQUIPMENT_IMAGES}/{stat}"
    found = sorted(glob.glob(os.path.join(resolve(folder), "*.png")))
    return [f"{folder}/{os.path.basename(path)}" for path in found]


def demon_image(village, demon_name):
    return f"img/village-demon/village-{village}/{demon_name}.png"
