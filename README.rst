=======
Pymacco
=======

``Pymacco`` is a Python implementation the card game Tomacco (a variation
of `shithead <http://en.wikipedia.org/wiki/Shithead_(card_game)>`_).

Installation
============

In the future ``Pymacco`` will be installable using ``pip install``.

Usage
=====

TODO

Official Tomacco Rules
======================
 
Preparation:
------------

- 1 deck for every 5 players
- Every player is dealt 9 cards.  6 cards go to their hand; 3 cards are placed
  face down in front of the player without being previewed.
- The rest of the deck are put in a pick-up pile
- Each player then selects 3 cards from their hand. Once all players have 
  selected their 3 cards, the cards are placed face up above their 3 face down cards.
 
The Deck:
---------

- 1 deck should be used for every 5 people added to the game. There is no
  theoretical maximum to the number of people who can play.
- Ace is high
- Once Ace is played the active pile is cleared and removed from play
- 3 or more of a kind: Clears the active pile and it is removed from play.
  When there is more than 1 deck in play, this moves to 4 of a kind to clear.
- Multiples of the same card can be played at any time.  This is an optional strategy.
 
Wild Cards:
-----------

- Can be played on any turn, and do not have to be played sequentially.
- 2:  Resets the active pile back down to 2. 
- 10: Clears the active pile
 
Play:
-----

- The person to the left of the dealer begins
- Each player must draw 1 card at each turn until no more cards remain in the pick-up pile
- The first player plays any card they wish from their hand. 
- Each subsequent player must then play a card higher than the one laid down
  by the previous player.  Any higher card can be played. This pile is called
  the ‘active pile’
- If a player cannot play a card higher than the last one played on the active pile,
  they must pick up the active pile.
- Once a player no longer has any cards in their hand, they may then play the face up cards.
 
Playing the Face Up Cards:
--------------------------

- When a player has no cards left in their hand, they then play the 3 face
  up cards following the same rules of play. 
- The player may choose any of the face up cards to play.  There is no order
  in which to play the face up cards.
- If multiples are in the face up cards, a player may, at their option, play the multiples.
- Once the face-up cards have been played, players are then permitted to play the face down cards.
 
Playing the Face Down Cards:
----------------------------

- Players can randomly choose any card from their 3 face down cards. 
- The Player selects a cards and looks to see what it is without showing any 
  other players. 
- If the card is playable (higher than the last card played on the active
  pile), the Player may play the card.
- If the card is not playable, the Player must place the card face down again
  and pick-up the active pile.  The Player must play out the cards in their
  hand before returning to the face down cards.
- If/when a player returns to the face down cards, they may select any face
  down card, whether is has been previously revealed or not.
- Peeking at the face-down cards is not permitted at any time.
- Multiples cannot be played from the face-down cards, even if 2 or more are known to be multiples.
