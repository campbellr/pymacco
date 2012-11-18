""" This module contains the any util functions or classes
"""


class GameOverException(Exception):
    pass


def iterable(l):
    """ Return an iterable
    """
    if not hasattr(l, '__iter__') or isinstance(l, basestring):
        l = [l]

    return l
