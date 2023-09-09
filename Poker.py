from itertools import combinations
import random


class PokerGame:

    def __init__ (self, players = 2):
        if players == 1:
            self.players = 2
        else:
            self.players = players
        self.cardsPlayer = []
        for i in range(self.players):
            self.cardsPlayer.append([])
        self.cardsTable = []
        d = ['2D', '3D', '4D', '5D', '6D', '7D','8D', '9D', 'TD', 'JD', 'QD', 'KD', 'AD', '2S', '3S', '4S', '5S'
        , '6S', '7S', '8S', '9S', 'TS', 'JS', 'QS', 'KS', 'AS','2C', '3C', '4C', '5C', '6C', '7C', '8C', '9C',
         'TC', 'JC', 'QC', 'KC', 'AC','2H', '3H', '4H', '5H', '6H', '7H', '8H', '9H', 'TH', 'JH','QH', 'KH','AH']
        random.shuffle(d)
        self.deck = d

    # adds a card to a specified player's hand
    def add_card(self, n):
        self.cardsPlayer[n].append(self.deck[0])
        self.deck.pop(0)

    # adds a card to the table
    def add_to_table(self):
        self.cardsTable.append(self.deck[0])
        self.deck.pop(0)

    def IsStraightFlush(self, cards): #checks if list has straightflush
        if self.IsStraight(cards) and self.IsFlush(cards):
            return True
        return False

    def IsFourofaKind(self, cards): #checks if list has four of one kind
        copy1 = cards
        for i in cards:
            counter = 0
            for j in copy1:
                if i[0] == j[0]:
                    counter = counter + 1
            if counter == 4:
                return True
        return False

    def IsFullHouse(self, cards): # checks if list has 3 of same rank and 2 of same rank
        copy1 = list(cards)
        copy2 = list(cards)
        triply = []
        for i in copy1:
            counter = 0
            for j in copy2:
                if i[0] == j[0]:
                    counter += 1
                if counter == 3:
                    triply.append(i)
        triply = set(triply)
        for i in triply:
            copy1.remove(i)
        if len(triply) == 3:
            if copy1[0][0] == copy1[1][0]:
                return True
        return False

    def IsFlush(self, cards): #checks if all 5 have same suit
        copy1 = cards
        for i in copy1:
            counter = 0
            for j in copy1:
                if i[1] == j[1]:
                    counter += 1
            if counter == 5:
                return True
        return False

    def IsStraight(self, cards): #checks if they are in order
        if self.orderchecker(cards):
            return True
        return False

    # checks if a group of five cards contains 3 of the same rank
    def IsThreeofaKind(self, cards):
        numOccurances = 0
        rank = cards[0][0]
        for i in range(len(cards)):
            rank = cards[i][0]
            numOccurances = 0
            for j in range(len(cards)):
                if cards[j][0] == rank:
                    numOccurances+=1
            if numOccurances == 3:
                return True
        return False

    # checks if there are two pairs of cards of the same rank
    def IsTwoPairs(self, cards):
        pairs = 0
        valuesChecked = []
        rank = cards[0][0]
        checked = False
        for i in range(len(cards)):
            checked = False
            rank = cards[i][0]
            for k in range(len(valuesChecked)):
                if rank == valuesChecked[k]:
                    checked = True
                    break
            if checked == False:
                for j in range(len(cards)):
                    if cards[j][0] == rank and j != i:
                        pairs+=1
                        valuesChecked.append(rank)
                        break
        if pairs == 2:
            return True
        return False

    # checks if there is one pair of cards of the same rank (does not count if more than one pair)
    def IsOnePair(self, cards):
        pairs = 0
        valuesChecked = []
        rank = cards[0][0]
        checked = False
        for i in range(len(cards)):
            checked = False
            rank = cards[i][0]
            for k in range(len(valuesChecked)):
                if rank == valuesChecked[k]:
                    checked = True
                    break
            if checked == False:
                for j in range(len(cards)):
                    if cards[j][0] == rank and j != i:
                        pairs+=1
                        valuesChecked.append(rank)
                        break
        if pairs == 1:
            return True
        return False
    def orderchecker(self,cards): #checks the order of the list
        copy1 = list(cards)
        numsA = []
        for i in copy1:
            if i[0] == 'A':
                numsA.append('A')
            elif i[0] == 'T':
                numsA.append(10)
            elif i[0] == 'J':
                numsA.append(11)
            elif i[0] == 'Q':
                numsA.append(12)
            elif i[0] == 'K':
                numsA.append(13)
            else:
                numsA.append(int(i[0]))
        while 'A' in numsA:
            if 2 in numsA and 3 in numsA and 4 in numsA and 5 in numsA:
                numsA.remove('A')
                numsA.append(1)
            else:
                for i in numsA:
                    if i == 'A':
                        numsA.remove('A')
                        numsA.append(14)
        numsA.sort()
        for i in range(len(numsA) - 1):
            if numsA[i] + 1 != numsA[i + 1]:
                return False
        return True
class TexasHoldem(PokerGame):
    def __init__ (self, players = 2):
        super().__init__(players)

    # adds two cards to each player's hand and five cards to the table
    def deal(self):
        for i in range(self.players):
            self.add_card(i)
            self.add_card(i)
        for i in range(5):
            self.add_to_table()

    # receives cards from each player's hand and the table and returns best outcome
    def hands(self):
        possibleCards = self.cardsTable
        handCombos = ['Straight Flush', 'Four of a Kind', 'Full House', 'Flush', 'Straight', 'Three of a Kind', 'Two Pair', 'Pair', 'High Card']
        possibleCombinations = []
        handPossibilities = []
        bestHand = []
        test = []
        minValue = -1
        for i in range(self.players):
            handPossibilities = []
            possibleCards.extend(self.cardsPlayer[i])  # adding player cards
            print(possibleCards)
            possibleCombinations = list(combinations(possibleCards, 5))
            for x in possibleCombinations:
                if super().IsStraightFlush(x):
                    handPossibilities.append(0)
                elif super().IsFourofaKind(x):
                    handPossibilities.append(1)
                elif super().IsFullHouse(x):
                    handPossibilities.append(2)
                elif super().IsFlush(x):
                    handPossibilities.append(3)
                elif super().IsStraight(x):
                    handPossibilities.append(4)
                elif super().IsThreeofaKind(x):
                    handPossibilities.append(5)
                elif super().IsTwoPairs(x):
                    handPossibilities.append(6)
                elif super().IsOnePair(x):
                    handPossibilities.append(7)
                else:
                    handPossibilities.append(8)
            minValue = min(handPossibilities)
            bestHand.append(handCombos[minValue])
            # removing player cards
            for j in range(len(self.cardsPlayer)):
                possibleCards.pop(len(possibleCards)-1)
        return bestHand
class OmahaHoldem(PokerGame):
    def __init__ (self, players = 2):
        super().__init__(players)

    # adds four cards to each player's hand and five cards to the table
    def deal(self):
        for i in range(self.players):
            for j in range(4):
                self.add_card(i)
        for i in range(5):
            self.add_to_table()
    def hands(self):
        possibleCards = self.cardsTable
        handCombos = ['Straight Flush', 'Four of a Kind', 'Full House', 'Flush', 'Straight', 'Three of a Kind', 'Two Pair', 'Pair', 'High Card']
        possibleCombinationsCards = []
        possibleCombinationsHand = []
        handPossibilities = []
        bestHand = []
        test = []
        minValue = -1
        for i in range(self.players):
            handPossibilities = []
            possibleCombinations = []
            playerhand = self.cardsPlayer[i]
            playerodds = playerhand
            #combinations of possible cards
            possibleCombinationsCards = list(combinations(possibleCards, 3))
            possibleCombinationsHand = list(combinations(playerhand, 2))
            for j in possibleCards:
                playerodds.append(j)
            print(playerodds)
            for j in possibleCombinationsCards:
                for k in possibleCombinationsHand:
                    l = list(j)
                    l.extend(k)
                    possibleCombinations.append(l)
            for x in possibleCombinations:
                if super().IsStraightFlush(x):
                    handPossibilities.append(0)
                elif super().IsFourofaKind(x):
                    handPossibilities.append(1)
                elif super().IsFullHouse(x):
                    handPossibilities.append(2)
                elif super().IsFlush(x):
                    handPossibilities.append(3)
                elif super().IsStraight(x):
                    handPossibilities.append(4)
                elif super().IsThreeofaKind(x):
                    handPossibilities.append(5)
                elif super().IsTwoPairs(x):
                    handPossibilities.append(6)
                elif super().IsOnePair(x):
                    handPossibilities.append(7)
                else:
                    handPossibilities.append(8)
            minValue = min(handPossibilities)
            bestHand.append(handCombos[minValue])
        return bestHand


print('Texas Holdem')
game2 = TexasHoldem(2)
game2.deal()
print(game2.hands())
print('--------------------------------------------------------------------------------')
print('Omaha Holdem')
game3 = OmahaHoldem(2)
game3.deal()
print(game3.hands())
