import os
import random
os.system('cls')

class BlackJack():
    '''
    BlackJack class has the following attributes:
        player - dict of current hand attributes
            money: int total money
            bet: int of money bet per round
            hand: list of cards in hand
            handvalue: int of total card value
            blackjack: boolean
            notbusted: boolean
        dealer - dict of current hand attributes
            hand: list of cards in hand
            handvalue: int of total card value
            blackjack: boolean
            notbusted: boolean
        deck - dict of deck attributes
            cut: int of when to reshuffle
            pack: list of all cards, 4 suits, 13 cards * number of decks
    '''
    # initializes global class attributes
    def __init__(self,
                player = dict.fromkeys(['money', 'bet', 'hand', 'handvalue', 'blackjack', 'notbusted']), 
                dealer = dict.fromkeys(['hand', 'handvalue', 'blackjack', 'notbust']),
                deck = dict.fromkeys(['cut', 'pack'])):
        self.player = player
        self.dealer = dealer
        self.deck = deck

    # initializes deck attributes, default is set to a 6 deck pack
    def deckAttributes(self, decks = 6):
        self.deck['cut'] = random.randint(60,75) #cut is randomly between 60-75 cards
        onedeck = []
        # 1 is actually 10, converted later
        for i in ['2', '3', '4', '5', '6', '7', '8', '9', '1', 'J', 'Q', 'K', 'A']:
            for j in ['Clubs', 'Spades', 'Diamonds', 'Hearts']:
                onedeck.append(i+j)
        self.deck['pack']= decks*onedeck

        # reshuffled if the cut is reached by adding deck-1 decks
        if len(self.deck['pack']) <= self.deck['cut']:
            self.deck['pack'] += (decks-1)*onedeck
    
    # sets palyers money
    def playerAttributes(self, money = 500):
        self.player['money'] = money

    # checks if bet is valid based on minimum bet, default set to 2
    def checkBet(self, input, minimum = 2):
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

    # draws card by randomly chosing from pack and removing card from pack
    def drawCard(self):
        card = random.choice(self.deck['pack'])
        self.deck['pack'].remove(card)
        return card
    
    # calculates handvalue, Ace can be considered a 1 or 11
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
    
    # prints players hand, converts 1,J,Q,K,A to word
    def printPlayerHand(self):
        print('Your current hand:')
        for i in range(len(self.player['hand'])):
            if self.player["hand"][i][0] == '1':
                print(f'card {i+1}: 10 of {self.player["hand"][i][1:]}')
            elif self.player["hand"][i][0] == 'J':
                print(f'card {i+1}: Jack of {self.player["hand"][i][1:]}')
            elif self.player["hand"][i][0] == 'Q':
                print(f'card {i+1}: Queen of {self.player["hand"][i][1:]}')
            elif self.player["hand"][i][0] == 'K':
                print(f'card {i+1}: King of {self.player["hand"][i][1:]}')
            elif self.player["hand"][i][0] == 'A':
                print(f'card {i+1}: Ace of {self.player["hand"][i][1:]}')
            else:
                print(f'card {i+1}: {self.player["hand"][i][0]} of {self.player["hand"][i][1:]}')

    # prints dealers hand, has conditional for hiding the dealers second card
    def printDealerHand(self, hide = False):
        print('Dealer hand:')
        if hide == True:
            if self.dealer["hand"][0][0] == '1':
                print(f'card 1: 10 of {self.dealer["hand"][0][1:]}\ncard 2: hidden')
            elif self.dealer["hand"][0][0] == 'J':
                print(f'card 1: Jack of {self.dealer["hand"][0][1:]}\ncard 2: hidden')
            elif self.dealer["hand"][0][0] == 'Q':
                print(f'card 1: Queen of {self.dealer["hand"][0][1:]}\ncard 2: hidden')
            elif self.dealer["hand"][0][0] == 'K':
                print(f'card 1: King of {self.dealer["hand"][0][1:]}\ncard 2: hidden')
            elif self.dealer["hand"][0][0] == 'A':
                print(f'card 1: Ace of {self.dealer["hand"][0][1:]}\ncard 2: hidden')
            else:
                print(f'card 1: {self.dealer["hand"][0][0]} of {self.dealer["hand"][0][1:]}\ncard 2: hidden')
        else:
            for i in range(len(self.dealer['hand'])):
                if self.dealer["hand"][i][0] == '1':
                    print(f'card {i+1}: 10 of {self.dealer["hand"][i][1:]}')
                elif self.dealer["hand"][i][0] == 'J':
                    print(f'card {i+1}: Jack of {self.dealer["hand"][i][1:]}')
                elif self.dealer["hand"][i][0] == 'Q':
                    print(f'card {i+1}: Queen of {self.dealer["hand"][i][1:]}')
                elif self.dealer["hand"][i][0] == 'K':
                    print(f'card {i+1}: King of {self.dealer["hand"][i][1:]}')
                elif self.dealer["hand"][i][0] == 'A':
                    print(f'card {i+1}: Ace of {self.dealer["hand"][i][1:]}')
                else:
                    print(f'card {i+1}: {self.dealer["hand"][i][0]} of {self.dealer["hand"][i][1:]}')

    # handles all logic for a round
    def round(self):
        os.system('cls')
        # resets defaults for reach round
        self.player['notbusted'] = True
        self.dealer['notbusted'] = True
        self.player['blackjack'] = False
        self.dealer['blackjack'] = False
        self.player['bet'] = None
        
        # holds user until a proper bet is placed
        while self.player['bet'] == None:
            self.player['bet'] = self.checkBet(input(f'You currently have ${self.player["money"]}\nHow much would you like to bet?\n$'), 2)
        
        # draws cards for both player and dealer
        self.player['hand'] = [self.drawCard(), self.drawCard()]
        self.dealer['hand'] = [self.drawCard(), self.drawCard()]

        # sets player and dealer handvalues
        self.player["handvalue"] = self.calcHandValue(self.player["hand"])
        self.dealer["handvalue"] = self.calcHandValue(self.dealer["hand"])

        # prints players hand
        self.printPlayerHand()
        print()

        # checks if player and dealer has blackjack
        if self.player["handvalue"] == 21:
            self.player['blackjack'] = True
        if self.dealer["handvalue"] == 21:
            self.dealer['blackjack'] = True

        # if player has blackjack and dealer doesnt, player wins and is awarded 1.5x bet
        if self.player['blackjack'] and self.dealer['blackjack'] == False:
            self.printDealerHand()
            breakline()
            print('BlackJack! - You Won!')
            breakline()
            self.player['money'] += self.player['bet']*1.5
            return self.player['money']
        # if player and dealer both have blackjack it is a draw
        elif self.player['blackjack'] and self.dealer['blackjack']:
            self.printDealerHand()
            breakline()
            print('Both you and the dealer got BlackJack')
            breakline()
            return self.player['money']
        
        # prints dealer hand with hidden card
        self.printDealerHand(True)
        breakline()

        # allows player to hit as long as they arent busted and stores handvalue
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
        
        # handles logic for dealer, will hit only if player has larger handvalue and hasnt busted
        while self.dealer["handvalue"] < self.player["handvalue"] and self.player['notbusted']:
            self.dealer["hand"].append(self.drawCard())
            self.dealer["handvalue"] = self.calcHandValue(self.dealer["hand"])
            if self.dealer["handvalue"] > 21:
                print('The dealer has busted!')
                breakline()
                self.dealer['notbusted'] = False
        
        # prints dealer hand
        self.printDealerHand()
        breakline()
        
        # handles logic to determine the winner
        # if dealer has busted and player hasn't = win, if player hand > dealer hand = win
        if (self.player['notbusted'] == True and self.dealer['notbusted'] == False) or (self.player['notbusted'] == True and self.dealer["handvalue"] < self.player["handvalue"]):
            print('You Won!')
            breakline()
            self.player['money'] += self.player['bet']
            return self.player['money']
        # if player busted = lose, if dealer hand > player hand = win
        elif self.player['notbusted'] == False or (self.dealer["handvalue"] > self.player["handvalue"] and self.dealer['notbusted']):
            print('You Lost :(')
            breakline()
            self.player['money'] -= self.player['bet']
            return self.player['money']
        # if player and dealer have the same hand value = draw
        elif self.dealer["handvalue"] == self.player["handvalue"]:
            print('It is a draw')
            breakline()
            return self.player['money']
    
    # All the rules of BlackJack
    def rules(self):
        print(' Rules of Black Jack '.center(41, '*'))
        print(' Version 1.0 '.center(41, '*'))
        print(
'''- Object of the Game: Attempt to beat the dealer by getting a count as close to 21 as possible, without going over 21 (bust).
- The Play: The player and dealer are dealt two cards, both the players cards are shown and one of the dealers cards are hidden. The player has the option to 'hit'(ask for another card) or 'stand'(not ask for another card). All the dealer's cards are revealed only when the player stands or goes bust.
- Card Values: An ace is worth 1 or 11. Face cards are 10 and any other card is its pip value.
- Betting: A bet is placed before the deal begins and has a minimum of $2.
- The Pack: This is a six-deck game(312 cards) consisting of standard 52-card decks.
- The Cut: A plastic card is randonly placed between the last 60-75 cards, determing when to reshuffle.
- BlackJack: If the player is dealt 21, the player has struck BlackJack and is awarded 1.5x their bet, unless the dealer also recieves BlackJack in which the game is a draw.

Version 2.0 Pending Release:
-Addition of splitting pairs, doubling down, insurance, and settlement''')
        
    def mainMenu(self):
        os.system('cls')
        self.deckAttributes()
        self.playerAttributes()
        # holds user in mainmenu until exists
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
                self.rules()
                input('')
                os.system('cls')
            elif maininput.lower() in ['3', 'three', 'quit', 'q', 'esc', 'exit']:
                os.system('cls')
                print('See you later aligator!')
                break
            else:
                os.system('cls')
                print('That was not a valid input\nTry another input')
                breakline()

# breakline to make display cleaner
def breakline():
    print('----------------------------------------------------')      

Play = BlackJack()
Play.mainMenu()