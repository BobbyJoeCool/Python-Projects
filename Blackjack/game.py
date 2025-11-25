import classes

def newDeck():
    deck = classes.Deck()
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
    player.hand.addCard(deck.dealOne())
    dealer.hand.addCard(deck.dealOne())
    player.hand.addCard(deck.dealOne())
    dealer.hand.addCard(deck.dealOne())


    print("---------------------------------")
    print("")

def printHand(player, dealer=False):
    if not dealer:
        print(player.hand.showHand())
        playerValue, playerValueSoft = player.hand.getValue()
        playerName = player.name
        if playerValueSoft is not None:
            valueString = f"{playerValue}/{playerValueSoft}"
        else:
            valueString = str(playerValue)
        print(f"{playerName}'s hand value: {valueString}")
    else:
        print(player.hand.showHand(True))

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

def whoWon(player, dealer, bet):
    playerScore = player.hand.value
    dealerScore = dealer.hand.value
    playerName = player.name
    dealerName = dealer.name
    print("")
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