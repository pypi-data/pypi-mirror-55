# -*- coding: utf-8 -*-
from functools import cmp_to_key
from operator import itemgetter, methodcaller


def filter_or(item, filter):
    """Return True if matching fields two dictionaries have any same values."""
    if not item or not filter:
        return False
    # Convert both to sets: See if there is an intersection of anything.
    return set(item.items()).intersection(set(filter.items()))


def filter_and(item, filter):
    """Return True if matching fields two dictionaries have the same values."""
    if not item or not filter:
        return False
    # Convert both to sets: See if the intersection is the same as the filter.
    return set(item.items()).intersection(set(filter.items())) == set(
        filter.items()
    )


def _cmp(a, b):
    try:
        return (a > b) - (a < b)
    except TypeError:
        return -1


def multikeysort(items, columns, functions={}, getter=itemgetter):
    """Sort a list of dictionary objects or objects by multiple keys bidirectionally.

    Keyword Arguments:
    items -- A list of dictionary objects or objects
    columns -- A list of column names to sort by. Use -column to sort in descending order
    functions -- A Dictionary of Column Names -> Functions to normalize or process each column value
    getter -- Default "getter" if column function does not exist
              operator.itemgetter for Dictionaries
              operator.attrgetter for Objects
    """
    comparers = []
    for col in columns:
        column = col[1:] if col.startswith("-") else col
        if not column in functions:
            functions[column] = getter(column)
        comparers.append((functions[column], 1 if column == col else -1))

    def comparer(left, right):
        for func, polarity in comparers:
            result = _cmp(func(left), func(right))
            if result:
                return polarity * result
        else:
            return 0

    return sorted(items, key=cmp_to_key(comparer))
