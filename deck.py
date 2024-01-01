from card import Card
import random

class Deck:
    deck = []
    def __init__(self):
        self.flopped_cards = ""     
        self.flopped = False
        suit = ''
        value = ''
        for x in range(4):
            for y in range(13):
                if x == 0:
                    suit = "Hearts"
                elif x == 1:
                    suit = "Spades"
                elif x == 2:
                    suit = "Diamonds"
                elif x == 3:
                    suit = "Clubs"
                if y == 0:
                    value = "2"
                elif y == 1:
                    value = "3"
                elif y == 2:
                    value = "4"
                elif y == 3:
                    value = "5"
                elif y == 4:
                    value = "6"
                elif y == 5:
                    value = "7"
                elif y == 6:
                    value = "8"
                elif y == 7:
                    value = "9"
                elif y == 8:
                    value = "10"
                elif y == 9:
                    value = "Jack"
                elif y == 10:
                    value = "Queen"
                elif y == 11:
                    value = "King"
                elif y == 12:
                    value = "Ace"
                self.deck.append(Card(suit, value))

    def shuffle(self):
        random.shuffle(self.deck)
        

            

                