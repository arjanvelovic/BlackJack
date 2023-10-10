import os
import random
os.system('cls')
# Full Rule Set of Black Jack

# pack consist of 6 deck of cards, 312 cards total
# last 60-75 cards arent used, do this randomly
# player starts with $500, bet range $2 to $500
# player dealt with two cards face up
# dealer dealt with one card face down which is revealed when its his turn
# if player is dealt with 21, it is considered blackjack and they are awarded 1.5x their bet
# if dealer also dealt blackjack, then the player is given back his chips
# dealer must stop after recieving 17 or higher even if have an Ace
# if player is dealt a pair or cards they can split the pair,
    # the original bet that is placed has to be equalled to the 
# once the player goes bust they lose their bet, even if the dealer goes bust
# if player and dealter tie then player gets money back 

# player - dict of current hand attributes
    # money: int total money
    # bet: int betted value
    # cards: dict of cards in hand
        # card1: int cardvalue
        # card2: int cardvalue
        # etc.
    # handvalue: int of total card value
    # blackjack: boolean
    # bust: boolean
# dealer hand - dict of current hand attributes
    # cards: dict of cards in hand
        # card1: int cardvalue hidden card
        # card2: int cardvalue showed card
        # etc.
    # handvalue: int of total card value
    # blackjack: boolean
    # bust: boolean
# deck - dict of deck attributes
    # total cards: int, 312
    # cut: int, 60-75
    # playable cards: int, total cards - cut - cards played
    # all cards: [list of all cards, 4 suits, 13 cards * 6]

class BlackJack():
    '''
    '''
    def __init__(self,
                player = dict.fromkeys(['money', 'bet', 'hand', 'handvalue', 'blackjack', 'notbusted']), 
                dealer = dict.fromkeys(['hand', 'handvalue', 'blackjack', 'notbust']),
                deck = dict.fromkeys(['totalcards', 'cut', 'playable', 'allcards'])):
        self.player = player
        self.dealer = dealer
        self.deck = deck

    def deckAttributes(self):
        self.deck['totalcards'] = 312
        self.deck['cut'] = random.randint(60,75)
        self.deck['playable'] = self.deck['totalcards'] - self.deck['cut']
        onedeck = []
        for i in ['2', '3', '4', '5', '6', '7', '8', '9', '1', 'J', 'Q', 'K', 'A']:
            for j in ['Clubs', 'Spades', 'Diamonds', 'Hearts']:
                onedeck.append(i+j)
        self.deck['allcards']= 6*onedeck
    
    def playerAttributes(self):
        self.player['money'] = 500

    def checkBet(self, input, minimum):
        if input.isnumeric():
            intnum = int(input)
            if intnum >= minimum and intnum <= self.player['money']:
                os.system('cls')
                return intnum
            elif intnum < minimum:
                os.system('cls')
                print('That is less than the minimum bet of $2\nSubmit another bet')
                breakline()
            else:
                os.system('cls')
                print('You do not have that much cash\nSubmit another bet')
                breakline()
        else:
            os.system('cls')
            print('That was not a valid input\nSubmit another bet')
            breakline()

    def drawCard(self):
        card = random.choice(self.deck['allcards'])
        self.deck['allcards'].remove(card)
        return card
    
    def calcHandValue(self, handlist):
        handvalue = 0
        for card in handlist:
            if card[0] in ['2', '3', '4', '5', '6', '7', '8', '9']:
                handvalue += int(card[0])
            elif card[0] in ['1', 'J', 'Q', 'K']:
                handvalue += 10
            elif card[0] in ['A']:
                handvalue += 11
                if handvalue > 21:
                    handvalue -= 10
        return handvalue
    
    def printPlayerHand(self):
        print('Your current hand:')
        for i in range(len(self.player['hand'])):
            print(f'card {i+1} = {self.player["hand"][i][0]} of {self.player["hand"][i][1:]}')
        print(f'your current hand value: {self.calcHandValue(self.player["hand"])}')

    def printDealerHand(self):
        print('Dealer hand:')
        for i in range(len(self.dealer['hand'])):
            print(f'card {i+1} = {self.dealer["hand"][i][0]} of {self.dealer["hand"][i][1:]}')
        print(f'dealer hand value: {self.calcHandValue(self.dealer["hand"])}')

    def round(self):
        os.system('cls')
        self.player['notbusted'] = True
        self.dealer['notbusted'] = True
        self.player['blackjack'] = False
        self.dealer['blackjack'] = False
        self.player['bet'] = None

        while self.player['bet'] == None:
            self.player['bet'] = self.checkBet(input(f'You currently have ${self.player["money"]}\nHow much would you like to bet?\n$'), 2)
        
        self.player['hand'] = [self.drawCard(), self.drawCard()]
        self.dealer['hand'] = [self.drawCard(), self.drawCard()]

        self.player["handvalue"] = self.calcHandValue(self.player["hand"])
        self.dealer["handvalue"] = self.calcHandValue(self.dealer["hand"])

        self.printPlayerHand()
        print()

        if self.calcHandValue(self.player["hand"]) == 21:
            self.player['blackjack'] = True
        if self.calcHandValue(self.dealer["hand"]) == 21:
            self.dealer['blackjack'] = True

        if self.player['blackjack'] and self.dealer['blackjack'] == False:
            self.printDealerHand()
            breakline()
            print('BlackJack! - You Won!')
            breakline()
            self.player['money'] += self.player['bet']*1.5
            return self.player['money']
        elif self.player['blackjack'] and self.dealer['blackjack']:
            self.printDealerHand()
            breakline()
            print('Both you and the dealer got BlackJack')
            breakline()
            return self.player['money']

        print(f'Dealer hand:\ncard 1: {self.dealer["hand"][0][0]} of {self.dealer["hand"][0][1:]}\ncard 2: hidden')
        breakline()

        while self.player['notbusted']:
            decision = input('1) Hit     2) Stand\n')
            if decision.lower() in ['hit', 'h', '1', 'one', 'hit me', '']:
                os.system('cls')
                self.player["hand"].append(self.drawCard())
                self.player["handvalue"] = self.calcHandValue(self.player["hand"])
                self.printPlayerHand()
                breakline()
                if self.player["handvalue"] > 21:
                    print('You have busted')
                    breakline()
                    self.player['notbusted'] = False
                    break
                
            elif decision.lower() in ['stand', 's', '2', 'two']:
                breakline()
                break
            else:
                os.system('cls')
                print('That was not a valid input\nTry another input')
                breakline()
        
        while (self.dealer["handvalue"] < 17 and self.player['notbusted']) or (self.dealer["handvalue"] < self.player["handvalue"] and self.player['notbusted']):
            self.dealer["hand"].append(self.drawCard())
            self.dealer["handvalue"] = self.calcHandValue(self.dealer["hand"])
            if self.dealer["handvalue"] > 21:
                print('The dealer has busted!')
                breakline()
                self.dealer['notbusted'] = False
        
        self.printDealerHand()
        breakline()
        
        if self.player['notbusted'] == True and self.dealer['notbusted'] == False:
            print('You Won!')
            breakline()
            self.player['money'] += self.player['bet']
            return self.player['money']
        elif self.player['notbusted'] == True and self.dealer["handvalue"] < self.player["handvalue"]:
            print('You Won!')
            breakline()
            self.player['money'] += self.player['bet']
            return self.player['money']
        
        elif self.player['notbusted'] == False:
            print('You Lost :(')
            breakline()
            self.player['money'] -= self.player['bet']
            return self.player['money']
        
        elif self.dealer["handvalue"] > self.player["handvalue"] and self.dealer['notbusted']:
            print('You Lost :(')
            breakline()
            self.player['money'] -= self.player['bet']
            return self.player['money']
        
        elif (self.dealer['notbusted'] == False and self.player['notbusted'] == False) or (self.dealer["handvalue"] == self.player["handvalue"]):
            print('It is a draw')
            breakline()
            return self.player['money']

    def mainMenu(self):
        os.system('cls')
        while True:
            print(' Welcome to BlackJack! '.center(41, '*'))
            print(f' You currently have ${self.player["money"]} '.center(41, '*'))
            print('Please select a following option:')
            breakline()
            maininput = input('1) Play a Round     2) Read the Rules      3) Quit\n')
            if maininput.lower() in ['1', 'one', 'play', 'p', 'play a round', 'blackjack', '21', '']:
                os.system('cls')
                self.round()
            elif maininput.lower() in ['2', 'two', 'read', 'rules', 'read the rules', 'r']:
                os.system('cls')
                print('These are the rules')
                input('')
                os.system('cls')
            elif maininput.lower() in ['3', 'three', 'quit', 'q']:
                os.system('cls')
                print('See you later aligator')
                break
            else:
                os.system('cls')
                print('That was not a valid input\nTry another input')
                breakline()

def breakline():
    print('----------------------------------------------------')      

Play = BlackJack()
Play.deckAttributes()
Play.playerAttributes()

Play.mainMenu()
