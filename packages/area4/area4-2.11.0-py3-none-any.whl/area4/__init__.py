"""Main class."""
#  Copyright (c) 2018-present RDIL.
#  You should have received a copy of the
#  MIT License with this program/distribution.
# ---------------------------------------------------
# ~ area4 ~
# ---------------------------------------------------

from . import util as utils

# Info variables:
name = "area4"
__author__ = "RDIL"
author_email = "me@rdil.rocks"
description = "Dividers in Python, the easy way!"


def divider(number):
    """
    Get the divider you requested.

    :param number: the divider number (NOT 0)
    :return: requested divider
    :rtype: str
    :Example:
    area4.divider(3)
    will return ............
    """
    if number == 0 or type(number) != int:
        raise ValueError('Please use a number bigger then 0!')
    else:
        try:
            return utils.get_raw_file()[number].replace("\n", "")
        except IndexError:
            raise ValueError('That divider doesn\'t exist!')


def splitter(div, *args):
    """
    Split text with dividers easily.

    :return: newly made value
    :rtype: str
    :param div: the divider
    """
    retstr = ""
    if type(div) is int:
        div = utils.get_raw_file()[div]
    if len(args) == 1:
        return args[0]
    for s in args:
        retstr += s
        retstr += "\n"
        retstr += div
        retstr += "\n"
    return retstr


def area4info():
    """
    Get some info about the package.

    :return: Package info
    :rtype: str
    """
    return "Name: {0}\nAuthor: {1}\nAuthor Email: {2}\nDescription: {3}".format(
        name,
        __author__,
        author_email,
        description
    )


def make_div(unit, length=24,
             start='', end='',
             literal_unit=False):
    """
    Generate a custom divider.

    :param unit: str containing a repeating unit
    :param length: The maximum length (won't be exceeded) (default: 24)
    :param start: optional starting string
    :param end: optional ending string
    :param literal_unit: if True will not try to break
    unit down into smaller repeating subunits
    :return: a new, custom divider
    :rtype: str

    :Example:
    custom_div = make_div(unit='=-', length=40, start='<', end='=>')
    note:: The generated string will be terminated
    at the specified length regardless
    of if all the input strings have been fully replicated.
    A unit > 1 length may
    not be able to be replicated to extend to the full length.
    In this situation, the
    string will be shorter than the specified length.
    Example: unit of 10 characters and a specified length of
    25 will contain 2 units for
    a total length of 20 characters.
    """
    # Reduce the size if possible to extend closer to full length:
    if not literal_unit:
        unit = utils.reduce_to_unit(unit)
    repeats = (length - len(start + end)) // len(unit)
    return (start + unit * repeats + end)[0:length]
