"""Named screen coordinates and reference images (the ``coords/`` folder).

One JSON file per feature plus ``common.json``, merged into a single flat
namespace at import time, so callers look names up globally: ``coords("home")``.
"""

import glob
import json
import os
from functools import lru_cache

from .paths import resolve

_COORDS_DIR = resolve("coords")


def _load():
    """Merge every ``coords/*.json`` file, rejecting duplicate names.

    A flat namespace means a name defined twice would silently shadow the
    other, so the clash fails loudly with both filenames.
    """
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
    """Return every reward thumbnail identifying a ``stat`` equipment quest.

    The art changes with the stat farmed, so the references are a folder rather
    than a named entry: ``img/equipement/<stat>/*.png``.
    """
    folder = f"{_EQUIPMENT_IMAGES}/{stat}"
    found = sorted(glob.glob(os.path.join(resolve(folder), "*.png")))
    return [f"{folder}/{os.path.basename(path)}" for path in found]


def demon_image(village, demon_name):
    """Return the reference image of ``demon_name`` as seen in ``village``.

    The same demon is drawn at a slightly different angle in each village, so
    the path is built rather than named: 6 x 6 would be 36 near-identical entries.
    """
    return f"img/village-demon/village-{village}/{demon_name}.png"
