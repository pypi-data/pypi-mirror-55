from collections.abc import Iterable


def reverse(val):
    if isinstance(val, Iterable):
        return val[::-1]
    return val


def strip(val):
    if isinstance(val, str):
        return val.strip()
    return val


filters = {"reverse": reverse, "strip": strip}
