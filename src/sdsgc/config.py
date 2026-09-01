import json

from .paths import resolve


class Config:
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
        self._data[key] = value

    def is_true(self, key):
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
    global _cache
    if _cache is None:
        _cache = _load()
    return _cache


def reload():
    global _cache
    _cache = None
    return get_config()


def save(key, value):
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
