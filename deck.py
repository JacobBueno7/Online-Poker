from card import Card
import random

class Deck:
    deck = []
    def __init__(self):
        self.flopped_cards = ""     
        self.flopped = False
        suit = ''
        for x in range(4):
            for y in range(1, 14):
                if x == 0:
                    suit = "Hearts"
                elif x == 1:
                    suit = "Spades"
                elif x == 2:
                    suit = "Diamonds"
                elif x == 3:
                    suit = "Clubs"
                if y == 1:
                    y = "Ace"
                elif y == 11:
                    y = "Jack"
                elif y == 12:
                    y = "Queen"
                elif y == 13:
                    y = "King"
                self.deck.append(Card(suit, y))

    def shuffle(self):
        random.shuffle(self.deck)
        


            

                