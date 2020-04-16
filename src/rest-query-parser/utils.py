from constants import EMPTY_VALUES


def coalesce(*args):
    for arg in args:
        if arg not in EMPTY_VALUES:
            return arg

    return None
