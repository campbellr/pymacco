""" This module provides a base implementation for UI's that all UI's
    should extend.
"""
from pymacco.util import GameOverException
from pymacco.logic import TomaccoGame

class BaseUi(object):
    """ Provides a base implementation of a UI that all UI's must follow.
    """

    def __init__(self):
        self.players = None
        self.game = None

    def createPlayers(self):
        raise NotImplementedError("This method must be overridden by the subclass.")

    def createGame(self):
        if not self.players:
            raise Exception("The players must exist before the game can be created.")
        self.game = TomaccoGame(self.players)

    def startGame(self):
        try:
            self.game.start()
            while True:
                player = self.game.getNextPlayer()
                self.playTurn(player)
        except GameOverException:
            print "Game Over, something else needs to go here!"

    def playTurn(self, player):
        """ Handle the turn for the given player.
        """
        player.pickUp()
        self._displayCards(player)
        card = self._getPlayersPlay(player)
        if not card:
            player.pickUpPile()
        else:
            player.playCard(card)

    def _displayCards(self, player):
        """ Display the cards for the given player.
        """
        raise NotImplementedError("This method must be overridden by the subclass.")

    def _getPlayersPlay(self, player):
        """ Get the given players play.

            :param player: The player who's play it is.
            :type player: :py:class:`player.player.Player`

            :return: (:py:class:`logic.TomaccoCard`)
        """
        raise NotImplementedError("This method must be overridden by the subclass.")

def start(ui_cls):
    ui = ui_cls()
    ui.createPlayers()
    ui.createGame()
    ui.startGame()
