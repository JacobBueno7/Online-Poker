from card import Card
from deck import Deck
from player import Player
import os, random, time


class Poker:

    def __init__(self):
        self.d = Deck()
        self.allCardsDown = False
        self.timer = 0
        self.pot = 0
        self.cards = []
        self.betsEven = False

    # Game Functions
    def bet(self, player):
        while True:  
            try:
                bet = int(input("\nhow much would you like to bet?"))
                if bet > player.money:
                    print("\nInvalid Amount!")
                else:
                    break
            except ValueError:
                print("\nMust be a Number!")
        player.totalBet += bet
        self.pot += bet
        player.money -= bet
        print(f'\n{player.name} has raised the bet by {bet}! {player.name} now has ${player.money} left.')
        time.sleep(2)

    def call(self, player, opponent):
        player.turnEnded = True
        player.myTurn = False
        opponent.myTurn = True
        h = opponent.totalBet - player.totalBet
        player.money -= h
        player.totalBet = opponent.totalBet
        print(f"\n\n{player.name} has called for {h}!")
        time.sleep(2)

    def flop(self):
        self.d.flopped = True
        self.d.deck.pop(0)
        first, second, third = self.d.deck.pop(0), self.d.deck.pop(0), self.d.deck.pop(0)
        self.cards.extend([first, second, third])
        self.d.flopped_cards = f"The public cards are: | {first} | {second} | {third} | "

    def add_card(self):
        self.d.deck.pop(0)
        card = self.d.deck.pop(0)
        self.cards.append(card)
        self.d.flopped_cards = self.d.flopped_cards+f"{card} | "
    
    def End(self, p1, p2):
        p1EndCards, p2EndCards = list(self.cards), list(self.cards)
        p1EndCards.extend([p1.card1, p1.card2])
        p2EndCards.extend([p2.card1, p2.card2])
        p1EndCards.sort(key=self.cardValue)
        p2EndCards.sort(key=self.cardValue)
        p1HighCard = self.handEval(p1EndCards, p1)
        p2HighCard = self.handEval(p2EndCards, p2)
        if p1.score > p2.score:
            print(f'{p1.name} wins the pot of ${self.pot}')
            time.sleep(5)
            p1.money += self.pot
            self.restart(p1, p2)

        elif p1.score < p2.score:
            print(f'{p2.name} wins the pot of ${self.pot} with a {p2.hand}')
            time.sleep(5)
            self.restart(p1, p2)    

        else:
            if p1HighCard > p2HighCard:
                print(f'{p1.name} wins the pot of ${self.pot}')
                time.sleep(5)
                self.restart(p1, p2)
            elif p2HighCard > p1HighCard:
                print(f'{p2.name} wins the pot of ${self.pot}')
                time.sleep(5)
                self.restart(p1, p2)
            else:
                print(f"It's a tie! The pot will be split among the players who won!")
                h = self.pot // 2
                p1.money += h
                p2.money += h
                time.sleep(5)
                self.restart(p1, p2)

    def restart(self, p1, p2):
        self.pot = 0
        self.allCardsDown = False
        self.timer = 0
        self.cards = []
        self.d = Deck()
        p1.myTurn = True
        p2.myTurn = False
        p1.turnEnded = False
        p2.turnEnded = False
        p1.totalBet = 0
        p2.totalBet = 0


    # Hand Functions
        
    def cardValue(self, card):
        if card.value == "Ace":
            return 14
        elif card.value == "King":
            return 13 
        elif card.value == "Queen":
            return 12
        elif card.value == "Jack":
            return 11
        else:
            return int(card.value)

    def isRoyal(self, cards):
        values = ["Ace", "King", "Queen", "Jack", "10"]
        for card in cards:
            if card.value in values:
                values.remove(card.value)
        if len(values) == 0:
            return True
        return False
    
    def isFlush(self, cards):
        test = cards.pop(0)
        counter = 0
        hand = []
        for card in cards:
            if card.suit != test.suit:
                counter += 1
            else:
                hand.append(card)
        if counter > 2:
            return False, None
        return True, self.highCard(hand)

    def hasStraight(self, cards):
        counter = 0
        hand = [cards[0]]
        for x in range(1, 5):
            if self.cardValue(cards[0]) + x == cards[x]:
                counter += 1
                hand.append(cards[x])
        if counter == 4 or (counter == 3 and self.hasAce(cards)):
            if counter == 3:
                hand.append(Card("Spades", "Ace"))
            return True, self.highCard(hand)
        counter = 0
        hand = [cards[0]]
        for x in range(2, 6):
            if self.cardValue(cards[1]) + x == cards[x]:
                counter += 1
                hand.append(cards[x])
        if counter == 4:
            return True, self.highCard(hand)
        counter = 0
        hand = [cards[0]]
        for x in range(3, 7):
            if self.cardValue(cards[2]) + x == cards[x]:
                counter += 1
                hand.append(cards[x])
        if counter == 4:
            return True, self.highCard(hand)
        return False, None

    def hasAce(self, cards):
        for card in cards:
            if card.value == "Ace":
                return True
        return False
    
    def hasFullHouse(self, cards):
        total, cardVal = self.xOfAKind(cards)
        blank, highCardPair = self.totalPairs(cards)
        if total == 3 and self.totalPairs(cards) >= 1:
            return True, max(highCardPair, cardVal)
        return False, None

    def xOfAKind(self, cards):
        total = 1
        temp = 1
        cardValue = 0
        for x in range(len(cards)-1):
            for y in range(x+1, len(cards)):
                if y == len(cards):
                    break
                elif cards[x].value == cards[y].value:
                    temp += 1
            if temp > total:
                total = temp
                cardValue = self.cardValue(cards[x])
        return total, cardValue
    
    def totalPairs(self, cards):
        pairs = 0
        burner = cards
        highCard = 0
        while True:
            if len(burner) <= 1:
                break
            elif burner[0].value == burner[1].value:
                pairs += 1
                if self.cardValue(burner[0]) > highCard:
                    highCard = self.cardValue(burner[0])
            burner.pop(0)
            burner.pop(0)
        return pairs, highCard
    
    def highCard(self, cards):
        value = 0
        for card in cards: 
            if self.cardValue(card) > value:
                value = self.cardValue(card)
        return value

    def handEval(self, cards, player):
        hasStraight, straightHighCard = self.hasStraight(cards)
        hasFlush, flushHighCard = self.isFlush(cards)
        if hasStraight:
            if self.isRoyal(cards):
                player.score = 23
                return
            elif hasFlush:
                player.score = 22
                return flushHighCard
            player.score = 18
            return straightHighCard

        elif hasFlush:
            player.score = 19
            return flushHighCard

        total, cardValue = self.xOfAKind(cards)
        hasFullHouse, fullHouseHighCard = self.hasFullHouse(cards)
        if total == 4:
            player.score = 21
            return cardValue
        elif total == 3:
            if hasFullHouse:
                player.score = 20
                return fullHouseHighCard
            else:
                player.score = 17
                return cardValue
        pairs, pairHighCard = self.totalPairs(cards)
        if pairs >= 2:
            player.score = 16
            return pairHighCard
        elif pairs == 1:
            player.score = 15
            return pairHighCard
        else:
            player.score = self.highCard(cards)
            return self.highCard(cards)





    # Game function
    def run(self):
        run = True
        for _ in range(3):
            random.shuffle(self.d.deck)

        player1 = input("\nWhat is the name of player 1?")
        while True:
            try:
                player1money = int(input("\nHow much would you like to spend on chips?($)"))
                break
            except ValueError:
                print("Must be a number!")

        player2 = input("\nWhat is the name of player 2?")
        while True:
            try:
                player2money = int(input("\nHow much would you like to spend on chips?($)"))
                break
            except ValueError:
                print("Must be a number!")

        p1 = Player(player1, self.d.deck.pop(0), self.d.deck.pop(0), player1money, True, 0, False, 0, '')
        p2 = Player(player2, self.d.deck.pop(0), self.d.deck.pop(0), player2money, False, 0, False, 0, '')

        while run:
            os.system("cls")
            if p1.turnEnded and p2.turnEnded and not self.allCardsDown:
                if self.d.flopped:
                    self.add_card()
                    self.timer += 1
                    p1.turnEnded = False
                    p2.turnEnded = False
                    p1.totalBet = 0
                    p2.totalBet = 0
                    p1.myTurn = True
                    p2.myTurn = False
                    if self.timer == 2:
                        self.allCardsDown = True
                else:
                    self.flop()
                    p1.turnEnded = False
                    p2.turnEnded = False
                    p1.totalBet = 0
                    p2.totalBet = 0
                    p1.myTurn = True
                    p2.myTurn = False
            print(self.d.flopped_cards)
            if p1.myTurn == True:
                print(p1)
                turn = input(f"\nWould you like to Bet(b), Call/Check(c), or Fold(f)? You have ${p1.money} left.")
                if turn == "b":
                    self.bet(p1)
                    p1.myTurn = False
                    p2.myTurn = True
                elif turn == "c":
                    self.call(p1, p2)
                elif turn == "f":
                    pass
            elif p2.myTurn == True:
                print(p2)
                turn = input(f"\nWould you like to Bet(b), Call/Check(c), or Fold(f)? You have ${p2.money} left.")
                if turn == "b":
                    self.bet(p2)
                    p2.myTurn = False
                    p1.myTurn = True
                elif turn == "c":
                    self.call(p2, p1)
                elif turn == "f":
                    pass
            if self.allCardsDown and p1.turnEnded and p2.turnEnded:
                self.End(p1, p2)

