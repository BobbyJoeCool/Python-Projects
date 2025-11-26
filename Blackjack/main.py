import game
import classes

print(""""
Welcome to BlackJack!
Programmed by Robert Breutzmann
as part of continued learning of Python.
      
Dealer hits until they have 17.
Dealer hits on soft 17
      
Blackjack pays 1.5x the bet (Rounded Down).
""")

playing = True
deck = game.newDeck()
player, dealer = game.newGame(deck)
while playing == True:
    insurance = False
    if len(deck.cards) < 15:
        deck = game.newDeck()
    chips = int(player.chips)
    player.hand.bet = int(game.getBet(player, chips))
    game.newHand(dealer, player, deck)
    game.printHand(dealer, None, True)
    game.printHand(player)
    
    if dealer.hand.cards[1].rank == "A" and not player.hand.blackjack():
        insurance = game.insurance(player)
    if dealer.hand.blackjack():  # Check for Dealer Blackjack
        game.printHand(dealer)
        print("Sorry, Dealer has Blackjack!")
        playerTurn = False
        dealerTurn = False
    else:
        playerTurn = True
        dealerTurn = True
        playerSplitTurn = True

    while playerTurn:
        if player.hand.blackjack(): # Check for Player Blackjack
            print("BlackJack!")
            player.hand.bet += int(player.hand.bet/2)
            playerTurn = False
            dealerTurn = False
        else:
            if player.chips >= player.hand.bet*2:
                if player.hand.cards[0].rank == player.hand.cards[1].rank and len(player.hand.cards) == 2:
                    split = input("WOuld you like to Split you hand and place an equal bet on the second hand? (y/n): ")
                    if split[0].lower().strip() == "y":
                        game.split(player, deck)
                        print("")
                        print("First Hand:")
                        game.printHand(player)
                if len(player.hand.cards) == 2 and split != "y":
                    double = input("Would you like to double down, double your bet, hit one time, and be done? (y/n): ")
                    if double[0].lower().strip() == "y":
                        game.double(player, deck)
                        print("")
                        game.printHand(player)
                        playerTurn = False
                        break
            else:
                print("You do not have enough chips to double down or split.")

            action = input("Hit or Stand?")
            if action.lower() == "hit":
                player.hand.addCard(deck.dealOne())
                game.printHand(player)
                if player.hand.value > 21:
                    playerTurn = False
            else:
                playerTurn = False

    if player.handSplit:
        while playerSplitTurn:
            print("")
            game.printHand(dealer, None, True)
            print("Second Hand:")
            game.printHand(player, player.handSplit)
            action = input("Hit or Stand?")
            if action.lower() == "hit":
                player.handSplit.addCard(deck.dealOne())
                game.printHand(player, player.handSplit)
                if player.handSplit.value > 21:
                    playerSplitTurn = False
            else:
                playerSplitTurn = False
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

    game.whoWon(player, dealer, insurance)

    if player.chips < 5:
        print("Sorry, you do not have enough chips to continue playing.  Thanks for playing!")
        break

    nextRound = input("Would you like to play again? (y/n): ")
    if nextRound.lower() == "y":
        continue
    else:
        print("\nThanks for playing!  Goodbye!\n")
        break