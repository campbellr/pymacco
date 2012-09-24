""" This module contains the base Player representation.

    Player can be extended to create any AI players.
"""
class Player(object):
    def __init__(self, name):
        self.name = name

        self.game = None
        self.hand = None
        
    def __str__(self):
        return "Player(%s)" % self.name

    def __repr__(self):
        return str(self)

    def pickUp(self):
        card = self.game.pickUp()
        self.hand.pickUp(card)

    def pickUpPile(self):
        cards = self.game.pickUpPile()
        self.hand.pickUp(cards)
    
    def playCard(self, card):
        if card not in self.hand:
            raise Exception("%s not in %s's hand!" % (card, self.name))
        self.game.playCard(self, card)
    
    def shouldPickUpPile(self):
        """ Auto-detect that the player needs to pick-up.
        """
        return not getPlayableCards()

    def getPlayableCards(self):
        """ Return a list of cards currently playable by this player.

            A card is considered playable if it is in the set of cards
            the player is currently player, and if it can beat the top
            card on the pile.

            :return: :py:func:`list` of :py:class:`logic.TomaccoCard`
        """
        playable = lambda cards: [card for card in cards if self.game.canPlay(card)]

        if self.hand.cardsInHand:
            return playable(self.hand.cardsInHand)
        if self.hand.cardsFaceUp:
            return playable(self.hand.cardsFaceUp)
        if self.hand.cardsFaceDown:
            return playable(self.hand.cardsFaceDown)
