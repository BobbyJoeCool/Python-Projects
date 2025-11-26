import classes

def newDeck():
    while True:
        decks = input("How many decks would you like to play with (enter a number 1-6?): ")
        if decks in ["1", "2", "3", "4", "5", "6"]:
            break
        else:
            print("Please enter a valid number of decks for the shoe.")
    
    deck = classes.Deck(int(decks))
    return deck

def newGame(deck):
    playerName = input("What is your Name?: ")
    player = classes.Player(playerName.strip())
    dealer = classes.Player("Dealer")
    player.hand = classes.Hand(player)
    dealer.hand = classes.Hand(dealer)
    player.chips = 50
    return player, dealer

def newHand(dealer, player, deck):
    player.hand.clearHand()
    dealer.hand.clearHand()
    player.handSplit = None
    # player.hand.addCard(deck.dealOne())
    dealer.hand.addCard(deck.dealOne())
    # player.hand.addCard(deck.dealOne())
    dealer.hand.addCard(deck.dealOne())
    # dealer.hand.dealBlackjack() # Testing Dealer Blackjack
    # player.hand.dealBlackjack() # Testing Player Blackjack
    player.hand.dealSplit()


    print("---------------------------------")
    print("")

def printHand(player, hand = None, dealer=False):
    if hand is None:
        hand = player.hand
    if not dealer:
        print(hand.showHand())
        playerValue, playerValueSoft = hand.getValue()
        playerName = player.name
        if playerValueSoft is not None:
            valueString = f"{playerValue}/{playerValueSoft}"
        else:
            valueString = str(playerValue)
        print(f"{playerName}'s hand value: {valueString}")
    else:
        print(hand.showHand(True))

def getBet(player, chips):
    playerName = player.name
    while True:
        print(f"\n{playerName} has {chips} chips remaining.")
        bet = input(f"Please place your bet.  Minimum bet is 5 chips: ")
        if not bet.isdigit():
            print("Please enter a valid number.")
            continue

        bet = int(bet)

        if bet < 5:
            print("Bet must be at least 5 chips.")
            continue
        if bet > chips:
            print("You do not have that many chips.")
            continue
        
        return bet
    
def insurance(player):
    result = False
    bet = player.hand.bet
    insurancePrice = int(bet/2)
    if player.chips > insurancePrice + bet:
        print(f"""The dealer is showing an Ace!
          Would you like to purchase insurance?
          It costs {insurancePrice} chips.
          You get to keep your bet if the dealer has Blackjack.
          You lose the insurance cost either way.
          """
          )
        insurance = input("(y/n): ")
        insurance = insurance[0].strip().lower()
        if insurance == "y":
            player.chips -= insurancePrice
            result = True
    else:
        print("Sorry, you don't have enough chips for insurance.")

    return result

def split(player, deck):
    player.handSplit = classes.Hand(player)
    player.handSplit.addCard(player.hand.split())
    player.handSplit.bet = player.hand.bet
    player.hand.addCard(deck.dealOne())
    player.handSplit.addCard(deck.dealOne())

def double(player, deck):
    player.hand.bet *= 2
    player.hand.addCard(deck.dealOne())

def whoWon(player, dealer, insurance):
    if not insurance:
        bet = player.hand.bet
        playerScore = player.hand.value
        dealerScore = dealer.hand.value
        playerName = player.name
        dealerName = dealer.name
        print("")
        if player.handSplit:
            print("First Hand:")

        if playerScore > 21:
            print(f"{playerName} Busted")
            player.chips -= bet
        elif dealerScore > 21:
            print(f"{dealerName} Busted")
            player.chips += bet
        elif playerScore == dealerScore:
            print("It's a push!")
        elif playerScore > dealerScore:
            print(f"{playerName} Wins!")
            player.chips += bet
        else:
            print(f"{dealerName} Wins!")
            player.chips -= bet
        
        if player.handSplit:
            bet = player.handSplit.bet
            playerScore = player.handSplit.value
            print("")
            print("Second Hand:")
            if playerScore > 21:
                print(f"{playerName} Busted")
                player.chips -= bet
            elif dealerScore > 21:
                print(f"{dealerName} Busted")
                player.chips += bet
            elif playerScore == dealerScore:
                print("It's a push!")
            elif playerScore > dealerScore:
                print(f"{playerName} Wins!")
                player.chips += bet
            else:
                print(f"{dealerName} Wins!")
                player.chips -= bet
    else:
        print("Thanks for buying Insurance!")
