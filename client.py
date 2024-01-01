from card import Card
from deck import Deck
from player import Player
import os
import random


def bet(player):
    bet = input("\nhow much would you like to bet?")
    print(f'{player.name} has raised the bet by {bet}! {player.name} now has ${player.money} left.')
    player.totalBet += int(bet)

def call1(player1, player2):
    player1.turnEnded = True
    player1.myTurn = False
    player2.myTurn = True
    h = player2.totalBet - player1.totalBet
    player1.money -= h
    player1.totalBet = player2.totalBet
    print(f"{player1} has called for {h}!")

def call2(player2, player1):
    player2.turnEnded = True
    player2.myTurn = False
    player1.myTurn = True
    h = player1.totalBet - player2.totalBet
    player2.money -= h
    player2.totalBet = player1.totalBet
    print(f"{player2} has called for {h}!")

def flop(d):
    d.flopped = True
    d.deck.pop()
    d.flopped_cards = f"The public cards are: | {d.deck.pop()} | {d.deck.pop()} | {d.deck.pop()} |"

def add_card(d):
    d.flopped_cards = d.flopped_cards+f"{d.deck.pop()} |"

class Poker:

    def __init__(self):
        self.d = Deck()

    def run(self):
        allCardsDown = False
        run = True
        for x in range(3):
            self.d.shuffle()
        player1 = input("\nWhat is the name of player 1?")
        player1money = int(input("\nHow much would you like to spend on chips?($)"))
        player2 = input("\nWhat is the name of player 2?")
        player2money = int(input("\nHow much would you like to spend on chips?($)"))
        p1 = Player(player1, self.d.deck.pop(), self.d.deck.pop(), player1money, True, 0, False)
        p2 = Player(player2, self.d.deck.pop(), self.d.deck.pop(), player2money, False, 0, False)

        while run:
            os.system("cls")
            if p1.turnEnded and p2.turnEnded and not allCardsDown:
                if self.d.flopped:
                    add_card(self.d)
                    p1.turnEnded = False
                    p2.turnEnded = False
                    p1.total_bet = 0
                    p2.total_bet = 0
                    p1.myTurn = True
                    p2.myTurn = False
                else:
                    flop(self.d)
                    p1.turnEnded = False
                    p2.turnEnded = False
                    p1.total_bet = 0
                    p2.total_bet = 0
                    p1.myTurn = True
                    p2.myTurn = False
            print(self.d.flopped_cards)
            if allCardsDown:
                End()
            if p1.myTurn == True:
                print(p1)
                turn = input("Would you like to Bet(b), Call/Check(c), or Fold(f)?")
                if turn == "b":
                    bet(p1)
                    p1.myTurn = False
                    p2.myTurn = True
                elif turn == "c":
                    call1(p1, p2)
                elif turn == "f":
                    pass
            elif p2.myTurn == True:
                print(p2)
                turn = input("Would you like to Bet(b), Call/Check(c), or Fold(f)?")
                if turn == "b":
                    bet(p2)
                    p2.myTurn = False
                    p1.myTurn = True
                elif turn == "c":
                    call2(p2, p1)
                elif turn == "f":
                    pass

