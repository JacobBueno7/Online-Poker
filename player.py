from card import Card
class Player:
    def __init__(self, name, card1, card2, money, myTurn, totalBet, turnEnded, score, hand):
        self.name = name
        self.card1 = card1
        self.card2 = card2
        self.money = money
        self.myTurn = myTurn
        self.totalBet = totalBet
        self.turnEnded = turnEnded
        self.score = score
        self.hand = hand
    
    def __repr__(self):
        return str(f'\n{self.name} has | {self.card1} | {self.card2} |')
    
        