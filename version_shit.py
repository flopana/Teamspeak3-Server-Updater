import re
from distutils.version import LooseVersion

"""
Sorts the versions in a human way so that for example 1.15 is newer than 1.2
"""


def tryint(s):
    try:
        return int(s)
    except ValueError:
        return s


def alphanum_key(s):
    """ Turn a string into a list of string and number chunks.
        "z23a" -> ["z", 23, "a"]
    """
    return [tryint(c) for c in re.split('([0-9]+)', s)]


def sort(l):
    """ Sort the given list in the way that humans expect.
    """
    l.sort(key=alphanum_key)


def vcmp(version1, version2):
    """
    Compares the two versions and returns true if version1 is smaller than version2

    :param version1:
    :param version2:
    :return boolean:
    """
    return LooseVersion(version1) < LooseVersion(version2)
