from base import BaseUi, start
from player.player import Player

class SimpleCli(BaseUi):
    
    def createPlayers(self):
        numPlayers = int(input("How many players?"))
        self.players = [Player("Player " + str(i+1)) for i in range(numPlayers)]

    def _displayCards(self, player):
        self._printDownCards(player.hand)
        self._printUpCards(player.hand)
        self._printHand(player.hand)

    def _printDownCards(self, hand):
        self._printCards(hand.cardsFaceDown, mask="*")

    def _printUpCards(self, hand):
        self._printCards(hand.cardsFaceUp)

    def _printHand(self, hand):
        self._printCards(hand.cardsInHand)

    def _printCards(self, cards, mask=None):
        # TODO: make this a nicer print out.
        # TODO: identify the cards with numbers (up, down, and hand cards must be unique)
        if mask:
            output = " ".join([mask for card in cards])
        else:
            output = " ".join([card.value for card in cards])
        print output

    def _getPlayersPlay(self, player):
        print str(player) + "'s turn"
        # TODO: support multiple cards
        cardNum = input("Which card would you like to play?")
        # TODO: get the card based on all the cards (not just their hand)
        card = player.hand.cardsInHand[cardNum]
        print str(player) + " played " + str(card)
        return card

if __name__ == "__main__":
    start(SimpleCli)
