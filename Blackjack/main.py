import game
import classes

print(""""
Welcome to BlackJack!
Programmed by Robert Breutzmann
as part of continued learning of Python.
      
Dealer hits until they have 17.
Dealer hits on soft 17
""")

playing = True
deck = game.newDeck()
player, dealer = game.newGame(deck)
while playing == True:
    game.newHand(dealer, player, deck)
    game.printHand(dealer, True)
    game.printHand(player)
    

    if dealer.hand.blackjack():  # Check for Dealer Blackjack
        game.printHand(dealer)
        print("Sorry, Dealer has Blackjack!")
        playerTurn = False
        dealerTurn = False
    else:
        playerTurn = True
        dealerTurn = True

    while playerTurn:
        if player.hand.blackjack(): # Check for Player Blackjack
            print("BlackJack!")
            playerTurn = False
            dealerTurn = False
        else:
            action = input("Hit or Stand?")
            if action.lower() == "hit":
                player.hand.addCard(deck.dealOne())
                game.printHand(player)
                if player.hand.value > 21:
                    playerTurn = False
                    dealerTurn = False
            else:
                playerTurn = False

    print("")

    while dealerTurn:
        game.printHand(dealer)
        if dealer.hand.valueSoft is not None:
            if dealer.hand.value <= 17:
                dealer.hand.addCard(deck.dealOne())
            else:
                dealerTurn = False
        elif dealer.hand.value < 17:
            dealer.hand.addCard(deck.dealOne())
        elif dealer.hand.value > 21:
            dealerTurn = False
        else:
            dealerTurn = False

    game.whoWon(player, dealer)

    nextRound = input("Would you like to play again? (y/n): ")
    if nextRound.lower() == "y":
        continue
    else:
        print("\nThanks for playing!  Goodbye!\n")
        break