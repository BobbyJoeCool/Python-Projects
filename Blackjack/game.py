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

def whoWon(player, dealer):
    playerScore = player.hand.value
    dealerScore = dealer.hand.value
    playerName = player.name
    dealerName = dealer.name
    print("")
    if playerScore > 21:
        print(f"{playerName} Busted")
    elif dealerScore > 21:
        print(f"{dealerName} Busted")
    elif playerScore == dealerScore:
        print("It's a push!")
    elif playerScore > dealerScore:
        print(f"{playerName} Wins!")
    else:
        print(f"{dealerName} Wins!")