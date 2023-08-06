"""Utilities"""


def sec2unit(value, force=None):
    """Convert a value in seconds in the most appropriate unit
        or in the required unit
        force:   unit required"""
    unit = 'sec'
    if value is None:
        return value, ''
    if force == unit:
        return value, unit
    if value >= 60 and value % 60. == 0:
        value /= 60
        unit = 'min'
        if force == unit:
            return value, unit
    if value >= 60 and value % 60. == 0:
        value /= 60
        unit = 'hour'
        if force == unit:
            return value, unit
    if value >= 24 and value % 24. == 0:
        value /= 24
        unit = 'day'
    return value, unit


def format2sec(value):
    """Convert format [value,unit] in seconds"""

    if value is None:
        return 0
    elif isinstance(value, (int, float)):
        return value
    else:
        i = ['sec', 'min', 'hour', 'day'].index(value[1])
        t = int(value[0]) * [1, 60, 3600, 86400][i]
        return t
