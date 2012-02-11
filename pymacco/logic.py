""" This module contains the logic for a card game
"""
import random


class Card(object):
    """ Representation of a single card.
    """
    suits = ['Clubs', 'Spades', 'Diamonds', 'Hearts']
    values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack',
            'Queen', 'King', 'Ace']

    def __init__(self, suit, value):
        if suit not in self.suits:
            raise ValueError("'suit' must be one of %s" % self.suits)
        if value not in self.values:
            raise ValueError("'value' must be one of %s" % self.suits)

        self.suit = suit
        self.value = value

    def __str__(self):
        return "Card(%s, %s)" % (self.suit, self.value)
    def __repr__(self):
        return str(self)


class TomaccoCard(Card):
    """ A card specfically for use in tomacco
    """
    clear_cards = ['10', 'Ace']
    reset_cards = ['2']

    def is_reset(self):
        """ Return whether or not the card is a 'reset card'.

            A 'reset card' is a card that resets the count of the cards on
            the table.
        """
        if self.value in self.reset_cards:
            return True

        return False

    def is_clear(self):
        """ Return whether or not the card is a 'clear card'.

            A 'clear card' will clear existing cards on the table.
        """
        if self.value in self.clear_cards:
            return True

        return False

    def __cmp__(self, other):
        # TODO: implement this!
        pass


class Deck(object):
    """ Representation of a single deck of cards.
    """
    def __init__(self, card_cls=Card, cards=None):
        self.card_cls = card_cls
        if cards:
            # TODO: should I be validating this?
            self.cards = cards
        else:
            self.cards = []
            for suit in self.card_cls.suits:
                for value in self.card_cls.values:
                    self.cards.append(self.card_cls(suit, value))

    def shuffle(self):
        """ Shuffle the deck.
        """
        random.shuffle(self.cards)

    def __getitem__(self, key):
        if isinstance(key, slice):
            return Deck(cards=self.cards[key])

        return self.cards[key]

    def __add__(self, other):
        return self.cards + other.cards

    def __sub__(self, other):
        return self.cards - other.cards

    def __iadd__(self, other):
        self.cards += other.cards
        return self

    def __isub__(self, other):
        self.cards += other.cards
        return self


class TomaccoHand(object):
    def __init__(self):
        self.cardsInHand = []
        self.cardsFaceUp = []
        self.cardsFaceDown = []
    def __str__(self):
        return "Hand(InHand: %s, FaceUp: %s, FaceDown: %s)" % \
               (self.cardsInHand, self.cardsFaceUp, self.cardsFaceDown)
    def __repr__(self):
        return str(self) 
        
        
class Player(object):
    def __init__(self, name):
        self.name = name
        self.hand = TomaccoHand()
    def __str__(self):
        return "Player(%s)" % self.name
    def __repr__(self):
        return str(self)


class TomaccoGame(object):
    """ Represents a game of tomacco.
    """
    def __init__(self, players, decks=1):
        self.deck = Deck(card_cls=TomaccoCard)
        for i in range(decks - 1):
            self.deck += Deck(card_cls=TomaccoCard)
            
        if not isinstance(players, list):
            players = [players]
        self.players = players

    def deal(self):
        numInHand = 6*len(self.players)
        numFaceDown = 3*len(self.players)
        
        for card in self.deck[:numInHand]:
            for player in self.players:
                player.hand.cardsInHand.append(card)
                
        for card in self.deck[numInHand:numInHand+numFaceDown]:
            for player in self.players:
                player.hand.cardsFaceDown.append(card)        


