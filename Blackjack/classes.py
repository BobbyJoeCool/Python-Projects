import random

class Card:
    def __init__(self, rank, suit, value):
        self.rank = rank
        self.suit = suit
        self.value = value

    def __str__(self):
        return f"{self.rank}{self.suit}"
    
class Deck:
    def __init__(self):
        suits = ["♠", "♥", "♦", "♣"]
        ranks = {
            "A": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6,
            "7": 7, "8": 8, "9": 9, "10": 10,
            "J": 10, "Q": 10, "K": 10
        }

        self.cards = [Card(rank, suit, ranks[rank]) for rank in ranks for suit in suits]
        
        random.shuffle(self.cards)

    def dealOne(self):
         return self.cards.pop(0)
    
class Hand:
    def __init__(self, owner):
        self.owner = owner
        self.cards = []
        self.value = 0
        self.valueSoft = None

    def addCard(self, card):
        self.cards.append(card)
        self.updateValue()

    def addCards(self, cards=[]):
        self.cards.append(cards)
        self.updateValue()

    def removeCard(self, card):
        if card in self.cards:
            self.cards.remove(card)
        self.updateValue()

    def sortHand(self):
        self.cards.sort(key=lambda c: (c.value))

    def clearHand(self):
        self.cards = []
        self.updateValue()

    def showHand(self, hide_first=False):
        ownerName = self.owner.name
        cardStrings = []
        for index, card in enumerate(self.cards):
            if hide_first and index == 0:
                cardStrings.append("[Hidden]")
            else:
                cardStrings.append(str(card))

        return f"{ownerName}'s hand: " + ", ".join(cardStrings)
    
    def updateValue(self):
        value = 0
        aces = 0
        for card in self.cards:
            value += card.value
            if card.rank == "A":
                aces += 1

        if aces > 0 and value <= 11:
            self.valueSoft = value
            value += 10
        else:
            self.valueSoft = None

        self.value = value

    def getValue(self):
        return self.value, self.valueSoft
    
class Player:
    def __init__(self, name="Player"):
        self.name = name
        self.hand = None

    def newHand(self, hand):
        self.hand = hand
    

if __name__== "__main__":
    deck = Deck()
    for card in deck:
            print(card)