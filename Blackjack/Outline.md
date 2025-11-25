# Blackjack

This program will be a blackjack game created as Python coding practice.

Initial Goals:
1) Basic Blackjack game with result logic
2) 1 Deck game (with option to add more later)
3) Dealer Logic (hit on <17 and Soft 17s>)
4) Original Program to start with fresh deck every hand.

Expansion Goals:
1) Add betting (with a pot)
2) Add Split and Doubles
3) Add Insurance if Dealers showing an Ace (pay 1/4 bet, don't lose if dealer Blackjack)
4) Add multiple decks for the shoe.
5) Expand to allow for a Discard Pile and to reshuffle when the deck gets low


---

Module Responsibilties

## main.py

Main Game Flow:

- Start a new game
- Make a new hand
- Ask for Bet
- Player Turn Logic
- Dealer Turn Logic
- Play Again?

## classes.py

Holds all Class definitions:

- Player Class
  - name: Player Name
  - hand: Holds Hand object
  - chips: Holds player's money

- Card Class
  - rank: A-K face of the card
  - suit: Holds the suit of the card
  - value: Holds the value of the card (A=1)

- Hand Class
  - owner: Who owns the hand
  - cards: List of cards in the hand
  - value: Combined Value of the cards in the hand
  - valueSoft: None - Hold the value if a card is an Ace and the hand holds 2 possible values.
  - Various functions to handle most of the fucntions for the game. (add card, remove card, updateValue, etc)

- Deck Class:
  - Creates 1 of each of the 52 cards in the deck, then shuffles them, creating a list of cards.
  - dealOne: "pops" the top card off the deck to give to a player.

  ## game.py

  Holds all the game functions such as "newDeck" "newGame", "newHand".

  ## ui.py

  Will hold all the UI information for the tkinter UI (in a GUI Class)