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

## `card.py`

**Purpose:**  
Represents a single playing card.

**Responsibilities:**

- Store the card’s rank and suit.
- Provide the card’s Blackjack value.
- Format the card nicely (e.g., `"A♠"`).

**Typical contents:**

- `class Card`
  - `rank`
  - `suit`
  - `value`
  - `__str__()` for printing

---

## `deck.py`

**Purpose:**  
Handles all deck operations.

**Responsibilities:**

- Create a standard 52-card deck.
- Shuffle the deck.
- Deal cards by removing them from the deck.

**Typical functions:**

- `create_deck()`
- `shuffle_deck(deck)`
- `deal_card(deck)`

---

## `hand.py`

**Purpose:**  
Manages a player's or dealer's hand.

**Responsibilities:**

- Store the cards a player/dealer has.
- Add new cards to the hand.
- Calculate total value (including Ace soft/hard logic).
- Display hand content when needed.

**Typical contents:**

- `class Hand`
  - `add_card()`
  - `calculate_value()`
  - `show_hand(hide_second=False)`

---

## `game.py`

**Purpose:**  
Implements the core Blackjack gameplay logic.

**Responsibilities:**

- Controls a full round of Blackjack.
- Manages turn flow:
  - Initial dealing
  - Player turn (hit/stand loop)
  - Dealer turn (draw until 17)
- Determines round outcomes.
- Keeps logic separate from user interface.

**Typical functions:**

- `play_round()`
- `player_turn(deck, player_hand)`
- `dealer_turn(deck, dealer_hand)`
- `determine_winner(player_hand, dealer_hand)`

---

## `ui.py`

**Purpose:**  
Handles user interaction and output formatting.

**Responsibilities:**

- Get user input (hit/stand).
- Display hands and statuses.
- Show round results.
- Ask whether to play again.

**Typical functions:**

- `get_player_choice()`
- `show_player_hand()`
- `show_dealer_hand()`
- `show_result()`
- `ask_play_again()`

---

## `main.py`

**Purpose:**  
Entry point of the program.

**Responsibilities:**

- Start the game.
- Run rounds in a loop.
- Handle the "play again" option.
