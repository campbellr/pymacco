""" Contains code that represents game rules,
    Without being part of specific logic or a class.
"""

def getNumDecks(playerCount):
    """ 1 deck for every 5 players.
    """
    return (playerCount / 5) + 1
