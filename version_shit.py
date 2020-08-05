"""
Sorts the versions in a human way so that for example 1.15 is newer than 1.2
"""
import re
from distutils.version import LooseVersion


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

    Args:
        version1: First version to compare e.g 2.1.7
        version2: Second version to compare e.g 2.1.8 or 2.2

    Returns:
        A boolean whether or not version1 is smaller then version two

    """
    return LooseVersion(version1) < LooseVersion(version2)
