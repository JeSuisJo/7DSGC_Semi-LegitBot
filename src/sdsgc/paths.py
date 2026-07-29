"""Filesystem paths anchored at the project root."""

import os

# src/sdsgc/paths.py -> sdsgc -> src -> project root
PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)


def resolve(relative_path):
    """Return an absolute path, resolving relative paths from the project root."""
    if os.path.isabs(relative_path):
        return relative_path
    return os.path.join(PROJECT_ROOT, relative_path)
