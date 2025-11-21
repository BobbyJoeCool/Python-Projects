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
    