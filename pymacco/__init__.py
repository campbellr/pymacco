__version__ = (0, 1, 0)


def getVersionString():
    return "pymacco" + ".".join(str(v) for v in __version__)
