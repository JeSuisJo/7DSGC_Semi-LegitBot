"""Single source of truth for user configuration (config.json)."""

import json

from .paths import resolve


class Config:
    """Read-only view over config.json with attribute and ``.get()`` access."""

    def __init__(self, data):
        self._data = data

    def __getattr__(self, name):
        try:
            return self._data[name]
        except KeyError as exc:
            raise AttributeError(name) from exc

    def get(self, key, default=None):
        return self._data.get(key, default)

    def set(self, key, value):
        """Update a value in the live config (in memory only)."""
        self._data[key] = value

    def is_true(self, key):
        """Return True for a flag stored as the string ``"true"``.

        config.json stores booleans as strings; real JSON booleans are accepted
        too, so the file can be cleaned up later without breaking callers.
        """
        value = self._data.get(key)
        if isinstance(value, bool):
            return value
        return str(value).strip().lower() == "true"


_cache = None


def _load():
    path = resolve("config.json")
    try:
        with open(path, encoding="utf-8") as f:
            return Config(json.load(f))
    except FileNotFoundError:
        print(f"Warning: config.json not found at {path}")
        return Config({})
    except json.JSONDecodeError:
        print("Warning: invalid JSON in config.json")
        return Config({})


def get_config():
    """Return the cached config, loading it on first use."""
    global _cache
    if _cache is None:
        _cache = _load()
    return _cache


def reload():
    """Drop the cache so the next :func:`get_config` re-reads the file.

    Called by the setup wizard: importing it already loaded whatever was on
    disk (or nothing at all) before it wrote the answers.
    """
    global _cache
    _cache = None
    return get_config()


def save(key, value):
    """Persist one key to config.json and to the live config.

    A write failure is not fatal: the value still applies to this session.
    """
    get_config().set(key, value)

    path = resolve("config.json")
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        data[key] = value
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write("\n")
    except (OSError, ValueError) as exc:
        print(f"Warning: could not save '{key}' to config.json ({exc})")
