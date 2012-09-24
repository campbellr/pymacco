""" This module contains the logic for a card game
"""
import random

from player.player import Player
import rules

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

    def __cmp__(self, card):
        if not isinstance(card, Card):
            raise TypeError("Cannot compare a %s to a Card." % type(card))

        # 2 of Clubs < 3 of Clubs from the values.
        # 2 of Clubs < 2 of Spades from the suits.
        # Arbitrarly decide that suits are more important, making the default sort by suit of
        # increasing values.
        thisCard = (self.suits.index(self.suit), self.values.index(self.value))
        otherCard = (self.suits.index(card.suit), self.values.index(card.value))

        return cmp(thisCard, otherCard)

    def __hash__(self):
        return hash((self.suit, self.value))

class TomaccoCard(Card):
    """ A card specifically for use in tomacco
    """
    clear_cards = ['10', 'Ace']
    reset_cards = ['2']
    wild_cards = ['2', '10']

    def is_reset(self):
        """ Return whether or not the card is a 'reset card'.

            A 'reset card' is a card that resets the count of the cards on
            the table.
        """
        return self.value in self.reset_cards

    def is_clear(self):
        """ Return whether or not the card is a 'clear card'.

            A 'clear card' will clear existing cards on the table.
        """
        return self.value in self.clear_cards

    def is_wild(self):
        """ Return whether or not the card is a 'wild card'.

            A 'wild card' can be played at any time.
        """
        return self.value in self.wild_cards

    def __cmp__(self, other):
        """ Arbitrarly, say that a return > 0 = card is a valid play.

            Also say 'self' is being played on the 'other' card.

            Example - get valid cards in hand:
                validCards = [card for card in myHand if card > pile.topCard]
        """
        if not isinstance(other, TomaccoCard):
            raise TypeError("Cannot compare a %s to a TomaccoCard." % type(other))

        if self.is_wild():
            return 1

        thisCard = self.values.index(self.value)
        otherCard = self.values.index(other.value)
        return cmp(thisCard, otherCard)

    def beats(self, card):
        """ Returns whether or not this card beats the given card.

            :param card: The card to compare this card to.
            :type card: :py:class:`logic.TomaccoCard`

            :return: True if this card can be played on the given card,
            otherwise False.
        """
        return self > card

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

    def removeTopCard(self):
        if len(self.cards) > 0:
            return self.cards.pop()
        return None

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

    def __contains__(self, card):
        allCards = self.cardsInHand + self.cardsFaceUp + self.cardsFaceDown
        return card in allCards

    def __getitem__(self, card):
        for cards in [self.cardsInHand, self.cardsFaceUp, self.cardsFaceDown]:
            if card in cards:
                return cards.remove(card)
        raise Exception("%s not in this hand!" % card)

    def pickUp(self, cards):
        """ Pick up one or more cards.

            :param cards: One or more cards to pick up.
            :type cards: :py:class:`logic.TomaccoCard` or
            :py:func:`list` of :py:class:`logic.TomaccoCard`
        """
        if not cards:
            print "no cards to pickup"
            return
        if isinstance(cards, list):
            self.cardsInHand.extend(cards)
        else:
            self.cardsInHand.append(cards)

class TomaccoPile(object):
    def __init__(self):
        self._pile = []

    def getTopCard(self):
        if len(self._pile) > 0:
            return self._pile[len(self._pile)-1]
        return None

    def canPlay(self, card):
        """ Validate whether the given card can be played on the pile.

            :param card: The card to check for playability.
            :type card: :py:class:`logic.TomaccoCard`

            :return: :py:func:`bool` True if the card can be played on this pile,
            otherwise False.
        """
        if not self.getTopCard():
            return True
        return card.beats(self.getTopCard())

    def play(self, card):
        """ Play a card on the top of the pile.

            :param card: The card to play.
            :type card: :py:class:`logic.TomaccoCard`
        """
        self._pile.append(card)

    def pickUp(self):
        cards =  self._pile[:]
        self._pile = []
        return cards

class TomaccoGame(object):
    """ Represents a game of tomacco.
    """
    def __init__(self, players, decks=None):
        players, decks = self._validateArgs(players, decks)
        self.deck = Deck(card_cls=TomaccoCard)
        for i in range(decks - 1):
            self.deck += Deck(card_cls=TomaccoCard)
        self.deck.shuffle()

        self.activePile = TomaccoPile()
        self.players = players
        for player in players:
            player.game = self
        # TODO: choose the starting player as the player to the right of the dealer.
        self.currentPlayer = random.choice(self.players)

    def start(self):
        self.deal()

    def _validateArgs(self, players, decks):
        """ Validates the args
        """
        if not isinstance(players, list) and not \
               isinstance(players, basestring) and getattr(players, '__iter__', False):
            # iterable that isn't a string or list, convert directly.
            players = list(players)
        elif not isinstance(players, list):
            players = [players]

        if len(players) < 2:
            raise ValueError("A Minimum of two players are required to play Tomacco")

        if decks is None:
            # 1 deck for every 5 players
            decks = rules.getNumDecks(len(players))

        return players, decks

    def deal(self):
        # TODO: pick a dealer randomly, deal starting to the right of the dealer.
        numInHand = 6
        numFaceDown = 3

        hands = [TomaccoHand() for i in range(len(self.players))]

        for i in range(numInHand):
            for hand in hands:
                card = self.deck.removeTopCard()
                print card.value
                hand.cardsInHand.append(card)

        for i in range(numFaceDown):
            for hand in hands:
                hand.cardsFaceDown.append(self.deck.removeTopCard())

        for player, hand in zip(self.players, hands):
            player.hand = hand

    def getNextPlayer(self):
        return self.currentPlayer

    def pickUp(self):
        """ Remove and return the top card off the deck.

            :return: (:py:class:`TomaccoCard`) The top card off the deck.
        """
        return self.deck.removeTopCard()

    def pickUpPile(self):
        self._incrementPlayer()
        return self.activePile.pickUp()

    def playCard(self, player, card):
        if not self.canPlay(card):
            raise Exception("Player attempted to play a card that cannot be played.")
        self.activePile.play(card)
        self._incrementPlayer()

    def _incrementPlayer(self):
        nextIndex = (self.players.index(self.currentPlayer)+1) % len(self.players)
        self.currentPlayer = self.players[nextIndex]

    def canPlay(self, card):
        """ Validate whether the given card can be played.

            :param card: The card to check for playability.
            :type card: :py:class:`logic.TomaccoCard`

            :return: :py:func:`bool` True if the card can be played,
            otherwise False.
        """
        return self.activePile.canPlay(card)
