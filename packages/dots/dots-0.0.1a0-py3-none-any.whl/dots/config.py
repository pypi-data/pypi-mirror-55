import os

HOME_DIR = os.path.expanduser("~")

DEFAULT_SOURCE_DIR = os.path.join(HOME_DIR, "dotfiles")
ACTION_COLOR_DICT = {
    "backup": "magenta",
    "create": "cyan",
    "remove": "red",
    "skip": "magenta",
    "up to date": "green",
    "update": "blue",
    "outdated": "red",
    # For SystemChecker
    "topic": "magenta",
    "pass": "green",
    "fail": "red",
    "warn": "yellow",
}
