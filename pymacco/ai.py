""" This module contains the logic the artificial opponents
"""
import random

from util import GameOverException

class Player(object):
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
        if self.hand.cardsInHand:
            return random.choice(self.hand.cardsInHand)
        if self.hand.cardsFaceUp:
            return random.choice(self.hand.cardsFaceUp)
        if self.hand.cardsFaceUp:
            return random.choice(self.hand.cardsFaceDown)
        raise GameOverException("%s has won!" % self)
    
    def shouldPickUpPile(self):
        return random.choice([False, False, True, False])