"""Utilities module."""
#  Copyright (c) 2018-present RDIL.
#  You should have received a copy of the
#  MIT License with this program/distribution.
# ---------------------------------------------------
# ~ area4 ~
# ---------------------------------------------------
import os
import random
from functools import lru_cache


@lru_cache(maxsize=None)
def get_raw_file():
    """
    Get the raw divider file in a string array.

    :return: the array
    :rtype: str
    """
    with open("{0}/dividers.txt".format(
        os.path.abspath(os.path.dirname(__file__))
    ), mode="r") as file_handler:
        lines = file_handler.readlines()
        stringbuilder = ""
        for i in range(6):
            stringbuilder += "<>"
        # we need to manually inject this, GitHub thinks its
        # a conflict marker
        lines[32] = stringbuilder
        lines[35] = str(
            random.randint(0, 999999999999)
        )
        return lines


def reduce_to_unit(divider):
    """
    Reduce a repeating divider to the smallest repeating unit possible.

    Note: this function is used by make-div
    :param divider: the divider
    :return: smallest repeating unit possible
    :rtype: str

    :Example:
    'XxXxXxX' -> 'Xx'
    """
    for unit_size in range(1, len(divider) // 2 + 1):
        length = len(divider)
        unit = divider[:unit_size]

        # Ignores mismatches in final characters:
        divider_item = divider[:unit_size * (length // unit_size)]
        if unit * (length // unit_size) == divider_item:
            return unit
    return divider  # Return original if no smaller unit


def get_divider_character(divider_id):
    """
    Get the character the divider is made of.

    :param divider_id: the divider's number
    :return: the character
    :rtype: str
    :Example:
    # Get what divider 7 is made of
    get_divider_character(7)
    # will return '='
    """
    blacklisted = [18, 19, 22, 33, 34, 35, 222, 223, 224, 226, 233, 234, 242]
    if divider_id in blacklisted:
        return None
    try:
        return get_raw_file()[divider_id][0]
    except IndexError:
        raise ValueError("That divider doesn't exist!")


def reddit_horizontal():
    """
    Get Reddit horizontal divider.

    :return: the divider
    :rtype: str
    """
    return "*****"


def markdown_horizontal():
    """
    Get Markdown horizontal divider.

    :return: the divider
    :rtype: str
    """
    return "---"
