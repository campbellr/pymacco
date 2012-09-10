from base import BaseUi, start
from player.player import Player

class SimpleCli(BaseUi):
    
    def createPlayers(self):
        numPlayers = int(raw_input("How many players?"))
        self.players = [Player("Player " + str(i+1)) for i in range(numPlayers)]

    def _displayCards(self, player):
        startingNumber = 1
        self._printDownCards(player.hand, startingNumber)
        startingNumber += len(player.hand.cardsFaceDown)
        self._printUpCards(player.hand, startingNumber)
        startingNumber += len(player.hand.cardsFaceUp)
        self._printHand(player.hand, startingNumber)

    def _printDownCards(self, hand, startingNumber):
        self._printCards(hand.cardsFaceDown, startingNumber, mask="*")

    def _printUpCards(self, hand, startingNumber):
        self._printCards(hand.cardsFaceUp, startingNumber)

    def _printHand(self, hand, startingNumber):
        self._printCards(hand.cardsInHand, startingNumber)

    def _printCards(self, cards, startingNumber, mask=None):
        # TODO: make this a nicer print out.
        # TODO: identify the cards with numbers (up, down, and hand cards must be unique)
        numbers = " ".join([str(i) for i in range(startingNumber, startingNumber+len(cards))])
        if mask:
            output = " ".join([mask for card in cards])
        else:
            output = " ".join([card.value for card in cards])
        print numbers
        print output

    def _getPlayersPlay(self, player):
        """ Get the card that the given player will play.

            :param player: The player to get the play of.
            :type player: :py:class:`player.player.Player`

            :return: The card that the player will play, or None
            if they will pick up.
        """
        print str(player) + "'s turn"
        topCard = self.game.activePile.getTopCard()
        if not topCard:
            print str(player) + " can play anything!"
        else:
            print str(player) + " must play on a " + str(topCard) + "!"
        # TODO: support multiple cards
        cardNum = raw_input("Which card would you like to play (p to pick the pile up)?")
        # TODO: get the card based on all the cards (not just their hand cards)
        if cardNum == "p":
            print str(player) + " picked up the pile!"
            return None
        else:
            cardNum = int(cardNum)
        if player.hand.cardsFaceDown and cardNum <= len(player.hand.cardsFaceDown):
            card = player.hand.cardsFaceDown[cardNum-1]
        else:
            if player.hand.cardsFaceDown:
                cardNum -= len(player.hand.cardsFaceDown)
            if player.hand.cardsFaceUp and cardNum > len(player.hand.cardsFaceUp):
                card = player.hand.cardsFaceUp[cardNum-1]
            else:
                if player.hand.cardsFaceUp:
                    cardNum -= len(player.hand.cardsFaceUp)
                card = player.hand.cardsInHand[cardNum-1]

        print str(player) + " played " + str(card)
        return card
