""" This module contains the logic the artificial opponents
"""
import random
from pymacco.player.player import Player

from pymacco.util import GameOverException

class AIPlayer(object):
    def __init__(self, name):
        self.name = name
        self.hand = None
        
    def __str__(self):
        return "Player(%s)" % self.name
    def __repr__(self):
        return str(self)
    
    def playCard(self, card):
        if card not in self.hand:
            raise Exception("%s not in %s's hand!" % (card, self.name))
        return self.hand[card]
    
    def chooseFaceUpCards(self):
        return random.sample(self.hand.cardsInHand, 3)

    def chooseCardToPlay(self):
        playableCards = self.getPlayableCards()
        if playableCards():
            return random.choice(playableCards)
        else:
            raise GameOverException("%s has won!" % self)
