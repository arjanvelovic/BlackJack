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
            handvalue: int of total hand value
            blackjack: boolean
            notbusted: boolean
            handsplit: list of cards in second hand if user splits
            handvaluesplit: into of total split hand value
            notbustedsplit: boolean for split hand
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
                player = dict.fromkeys(['money', 'bet', 'hand', 'handvalue', 'blackjack', 'notbusted', 'handsplit', 'handvaluesplit', 'notbustedsplit']), 
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

    # checks if bet or insurance is valid based on minimum bet, default set to 2
    def checkBet(self, input, maximum, minimum = 2, insurance = False):
        if input.lower() in ['', 'no', 'n', '0']:
            return 0
        elif input.isnumeric():
            intnum = int(input)
            if intnum >= minimum and intnum <= maximum:
                if insurance == False:
                    os.system('cls')
                return intnum
            elif intnum < minimum:
                print(f'That is less than the minimum bet of ${minimum}\nSubmit another bet')
                breakline()
            else:
                print(f'That is above the maximum bet of ${maximum}\nSubmit another bet')
                breakline()
        else:
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
    
    # prints hand, converts 1,J,Q,K,A to word, has condition for dealer hidden hand
    def printHand(self, hand, hide = False):
        if hand == self.dealer['hand']:
            print('Dealer hand:')
        else:
            print('Your current hand:')
        if hide == False:
            for i in range(len(hand)):
                if hand[i][0] == '1':
                    print(f'card {i+1}: 10 of {hand[i][1:]}')
                elif hand[i][0] == 'J':
                    print(f'card {i+1}: Jack of {hand[i][1:]}')
                elif hand[i][0] == 'Q':
                    print(f'card {i+1}: Queen of {hand[i][1:]}')
                elif hand[i][0] == 'K':
                    print(f'card {i+1}: King of {hand[i][1:]}')
                elif hand[i][0] == 'A':
                    print(f'card {i+1}: Ace of {hand[i][1:]}')
                else:
                    print(f'card {i+1}: {hand[i][0]} of {hand[i][1:]}')
        else:
            if hand[0][0] == '1':
                print(f'card 1: 10 of {hand[0][1:]}\ncard 2: Hidden')
            elif hand[0][0] == 'J':
                print(f'card 1: Jack of {hand[0][1:]}\ncard 2: Hidden')
            elif hand[0][0] == 'Q':
                print(f'card 1: Queen of {hand[0][1:]}\ncard 2: Hidden')
            elif hand[0][0] == 'K':
                print(f'card 1: King of {hand[0][1:]}\ncard 2: Hidden')
            elif hand[0][0] == 'A':
                print(f'card 1: Ace of {hand[0][1:]}\ncard 2: Hidden')
            else:
                print(f'card 1: {hand[0][0]} of {hand[0][1:]}\ncard 2: Hidden')

    # handles logic to ask questions for hand, recusive function for split
    def playerTurn(self, hand, notbusted, handvalue):
        while self.player[notbusted]:
            # restricts users to options based on if they already split
            if self.player[hand][0][0] == self.player[hand][1][0] and self.player[handvalue] in [9, 10, 11] and self.player['handsplit'] == None:
                decision = input('1) Hit     2) Stand     3) Split     4) Double Down\n')
            elif self.player[hand][0][0] == self.player[hand][1][0] and self.player[handvalue] not in [9, 10, 11] and self.player['handsplit'] == None:
                decision = input('1) Hit     2) Stand     3) Split\n')
            elif self.player[handvalue] in [9, 10, 11] and self.player[hand][0][0] != self.player[hand][1][0] and self.player['handsplit'] == None:
                decision = input('1) Hit     2) Stand     4) Double Down\n')
            else:
                decision = input('1) Hit     2) Stand\n')

            # if player hits
            if decision.lower() in ['hit', 'h', '1', 'one', 'hit me', '']:
                os.system('cls')
                self.player[hand].append(self.drawCard())
                self.player[handvalue] = self.calcHandValue(self.player[hand])
                self.printHand(self.player[hand])
                breakline()
                if self.player[handvalue] > 21:
                    print('You have busted')
                    breakline()
                    self.player[notbusted] = False
                    break

            # if player stands
            elif decision.lower() in ['stand', 's', '2', 'two']:
                breakline()
                break

            # if player splits, only allows split if user truly has pair and hasn't already split
            elif decision.lower() in ['split', '3', 'three'] and self.player[hand][0][0] == self.player[hand][1][0] and self.player['handsplit'] == None:
                os.system('cls')
                self.player['handsplit'] = [self.player['hand'][1],self.drawCard()]
                self.player['handvaluesplit'] = self.calcHandValue(self.player['handsplit'])

                self.player['hand'] = [self.player['hand'][0],self.drawCard()]
                self.player['handvalue'] = self.calcHandValue(self.player['hand'])

                # if user is dealt a pair of Aces
                if self.player['hand'][0][0] == 'A':
                    print('Hand 1:')
                    self.printHand(self.player['hand'])
                    breakline()
                    print('Hand 2:')
                    self.printHand(self.player['handsplit'])
                    breakline()
                    break

                self.printHand(self.player['hand'])
                self.printHand(self.dealer['hand'],True)
                breakline()
                # recussivly calls playerTurn()
                self.playerTurn('hand', 'notbusted', 'handvalue')

                print('Your Second Hand')
                self.printHand(self.player['handsplit'])
                self.printHand(self.dealer['hand'],True)
                breakline()
                # recussivly calls playerTurn()
                self.playerTurn('handsplit', 'notbustedsplit', 'handvaluesplit')
                break

            # if player doubles down, only allows if user truly has a handvalue of 9,10, or 11 and hasnt already split
            elif decision.lower() in ['double down', 'dd', 'double', 'down', '4', 'four'] and self.player[handvalue] in [9, 10, 11] and self.player['handsplit'] == None:
                os.system('cls')
                self.player['bet'] += self.player['bet']
                self.player[hand].append(self.drawCard())
                self.player[handvalue] = self.calcHandValue(self.player[hand])
                self.printHand(self.player[hand])
                breakline()
                break
            else:
                os.system('cls')
                print('That was not a valid input\nTry another input')
                breakline()

    # handles logic to determine the winner
    def determinWinner(self):
        # if dealer has busted and player hasn't = win, if player hand > dealer hand = win
        if (self.player['notbusted'] and self.dealer['notbusted'] == False) or (self.player['notbusted'] and self.player['handvalue'] > self.dealer["handvalue"]):
            print('Your Hand Won!')
            self.player['money'] += self.player['bet']
        # if player busted = lose, if dealer hand > player hand = win
        elif (self.player['notbusted'] == False and self.dealer['notbusted']) or (self.player['handvalue'] < self.dealer['handvalue'] and self.dealer['notbusted']):
            print('Your Hand Lost :(')
            self.player['money'] -= self.player['bet']
        # if player and dealer have the same hand value = draw
        elif (self.dealer['handvalue'] == self.player['handvalue']) or (self.player['notbusted'] == False and self.dealer['notbusted'] == False):
            print('It is a draw')
        breakline()

        # determines winner if player split
        if self.player['handsplit'] != None:
            if (self.player['notbustedsplit'] and self.dealer['notbusted'] == False) or (self.player['notbustedsplit'] and self.player["handvaluesplit"] > self.dealer["handvalue"]):
                print('Your Second Hand Won!')
                self.player['money'] += self.player['bet']
            elif (self.player['notbustedsplit'] == False and self.dealer['notbusted']) or (self.player["handvaluesplit"] < self.dealer["handvalue"] and self.dealer['notbusted']):
                print('Your Second Hand Lost :(')
                self.player['money'] -= self.player['bet']
            elif self.dealer["handvalue"] == self.player["handvaluesplit"] or (self.player['notbustedsplit'] == False and self.dealer['notbusted'] == False):
                print('Your Second Hand Drawed')
            breakline()

    # handles all logic for a round
    def round(self):
        os.system('cls')
        # resets defaults for each round
        self.player['bet'] = None
        self.player['notbusted'] = True
        self.player['notbustedsplit'] = True
        self.player['handsplit'] = None
        self.player['blackjack'] = False

        self.dealer['notbusted'] = True
        self.dealer['blackjack'] = False

        insurance = None
        
        # holds user until a proper bet is placed
        while self.player['bet'] == None:
            self.player['bet'] = self.checkBet(input(f'You currently have ${self.player["money"]}\nHow much would you like to bet?\n$'), self.player['money'])
        
        # draws cards for both player and dealer
        self.player['hand'] = [self.drawCard(), self.drawCard()]
        self.dealer['hand'] = [self.drawCard(), self.drawCard()]

        # sets player and dealer handvalues
        self.player["handvalue"] = self.calcHandValue(self.player["hand"])
        self.dealer["handvalue"] = self.calcHandValue(self.dealer["hand"])

        # prints players hand
        self.printHand(self.player['hand'])

        # checks if player and dealer has blackjack
        if self.player["handvalue"] == 21:
            self.player['blackjack'] = True
        if self.dealer["handvalue"] == 21:
            self.dealer['blackjack'] = True

        # if player has blackjack and dealer doesnt, player wins and is awarded 1.5x bet
        if self.player['blackjack'] and self.dealer['blackjack'] == False:
            self.printHand(self.dealer['hand'])
            breakline()
            print('BlackJack! - You Won!')
            breakline()
            self.player['money'] += self.player['bet']*1.5
            return self.player['money']
        # if player and dealer both have blackjack it is a draw
        elif self.player['blackjack'] and self.dealer['blackjack']:
            self.printHand(self.dealer['hand'])
            breakline()
            print('Both you and the dealer got BlackJack')
            breakline()
            return self.player['money']
        
        # prints dealer hand with hidden card
        self.printHand(self.dealer['hand'],True)
        
        # ask for insurance after printing dealer hidden hand
        if self.dealer['hand'][0][0] == 'A':
            breakline()
            while insurance == None:
                insurance = self.checkBet(input('The dealer has drawn an Ace\nDo you want to place insurance?\nIf so place your value here:\n$'),self.player['bet']/2, 0, True)
        breakline()

        # use of playerTurn function
        self.playerTurn('hand', 'notbusted', 'handvalue')
        
        # handles logic for dealer, will hit only if player has larger handvalue and hasnt busted
        while self.dealer["handvalue"] < self.player["handvalue"] and self.player['notbusted']:
            self.dealer["hand"].append(self.drawCard())
            self.dealer["handvalue"] = self.calcHandValue(self.dealer["hand"])
            if self.dealer["handvalue"] > 21:
                print('The dealer has busted!')
                breakline()
                self.dealer['notbusted'] = False
        
        # prints dealer revealed hand
        self.printHand(self.dealer['hand'])
        # settles insurance condition after revealing dealers hand
        if insurance != None and insurance != 0:
            if self.dealer['blackjack']:
                print(f'The dealer has BlackJack, your insurance covered ${insurance*2}')
                self.player['money'] += insurance*2
            else:
                print('You have lost your insurance')
                self.player['money'] -= insurance
        breakline()
        
        # determines winner
        self.determinWinner()
    
    # All the rules of BlackJack
    def rules(self):
        print(' Rules of Black Jack '.center(35, '*'))
        print(' Version 2.0 '.center(35, '*'))
        print(
'''- Object of the Game: Attempt to beat the dealer by getting a count as close to 21 as possible, without going over 21 (bust).
- The Play: The player and dealer are dealt two cards, both the players cards are shown and one of the dealers cards are hidden. The player has the option to 'hit'(ask for another card) or 'stand'(not ask for another card). All the dealer's cards are revealed only when the player stands or goes bust.
- Card Values: An ace is worth 1 or 11. Face cards are 10 and any other card is its pip value.
- Betting: A bet is placed before the deal begins and has a minimum of $2.
- The Pack: This is a six-deck game(312 cards) consisting of standard 52-card decks.
- The Cut: A plastic card is randonly placed between the last 60-75 cards, determing when to reshuffle.
- BlackJack: If the player is dealt 21, the player has struck BlackJack and is awarded 1.5x their bet, unless the dealer also recieves BlackJack in which the game is a draw.

Added Features to Version 2.0
- Splitting Pairs: If the player is dealt a pair they are able to split and treat them as two separate hands. The amount of the original bet then goes on one of the cards, and an equal amount must be placed as a bet on the other card. The two hands are treated separately, and the dealer settles with each on its own merits. With a pair of aces, the player is given one card for each ace and may not draw again. Also, if a ten-card is dealt to one of these aces, the payoff is equal to the bet (not one and one-half to one, as with a blackjack at any other time).
- Doubling Down: The player is able to double their bet if their hand totals 9, 10, or 11. The dealer gives the player just one card which ends the players turn. Note that the dealer does not have the option of splitting or doubling down.
- Insurance: When the dealer's face-up card is an ace, the player may make a side bet of up to half the original bet that the dealer's face-down card is a ten-card. If it is a ten-card, the player insurance bet is paid double the amount.
''')
        
    def mainMenu(self):
        os.system('cls')
        self.deckAttributes()
        self.playerAttributes()
        # holds user in mainmenu until exists
        while True:
            print(' Welcome to BlackJack! '.center(35, '*'))
            print(f' You currently have ${self.player["money"]} '.center(35, '*'))
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
    print('------------------------------------')      

Play = BlackJack()
Play.mainMenu()
print(Play.__dir__())