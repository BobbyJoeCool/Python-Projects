import game
import classes

print("")
print("Welcome to BlackJack!")
print("Programmed by Robert Breutzmann")
print("as part of continued learning of Python.")

playing = True
deck = game.newDeck()
player, dealer = game.newGame(deck)
while playing == True:
    game.newHand(dealer, player, deck)
    game.printHand(dealer, True)
    game.printHand(player)
    
    playerTurn = True
    dealerTurn = True
    while playerTurn:
        action = input("Hit or Stand?")
        if action.lower() == "hit":
            player.hand.addCard(deck.dealOne())
            game.printHand(player)
            if player.hand.value > 21:
                print("You Busted!")
                playerTurn = False
                dealerTurn = False
        else:
            playerTurn = False

    game.printHand(dealer)
    while dealerTurn:
        if dealer.hand.valueSoft is not None:
            if dealer.hand.value <= 17:
                dealer.hand.addCard(deck.dealOne())
                game.printHand(dealer)
        elif dealer.hand.value < 17:
            dealer.hand.addCard(deck.dealOne())
            game.printHand(dealer)
        elif dealer.hand.value > 21:
            print("Dealer Busts!")
            dealerTurn = False
        else:
            dealerTurn = False

    nextRound = input("Would you like to play again? (y/n): ")
    if nextRound.lower() == "y":
        deck = game.newDeck()
        game.newHand(dealer, player, deck)
        continue
    else:
        print("\nThanks for playing!  Goodbye!\n")
        break