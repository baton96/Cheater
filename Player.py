#Time limit per decision 0.01s !!!
class YourPlayer(Player): 
    def __init__(self, name):        
        self.name = name
        self.cards = None
        self.winOption = 3 #wartosc ustalona empirycznie podczas testow
        
    def startGame(self, cards):        
        self.cards = sorted(cards)
        self.nOpponentCards = len(cards) #8?Not 9?
        self.actualPile = []
        self.opCouldDraw = True
        
    def takeCards(self, cards_to_take):
        self.cards = sorted(self.cards + cards_to_take)
        
    def simple(self, declared_card): 
        #extended SimplePlayer strategy
        declaredColor = np.random.choice([i for i in range(4) if i!=declared_card[1]])
        self.actualPile.append(self.cards[0])
        return self.cards[0], (declared_card[0], declaredColor)

    def putCard(self, declared_card):
        self.opCouldDraw = False        
        if declared_card is None: 
            #nothing declared, give worst card
            self.actualPile.append(self.cards[0])
            return self.cards[0], self.cards[0]
        if len(self.cards) == 1 and self.cards[0][0] < declared_card[0]:
            #cant lie on last card
            self.actualPile = self.actualPile[:-1]
            return "draw"
        for card in self.cards: #try not to lie
            if card[0]>=declared_card[0]:
                #WinningPutter
                winning = len(self.cards)<self.nOpponentCards+self.winOption
                if winning: 
                    #play Honest
                    self.actualPile.append(card)
                    return card, card
                else: 
                    #play Sneaky
                    self.actualPile.append(self.cards[0])
                    return self.cards[0], card
        #I have to lie, use extended SimplePlayer strategy
        return self.simple(declared_card)
    
    def checkCard(self, opponent_declaration):
        self.nOpponentCards -= 1
        self.opCouldDraw = False        
        if opponent_declaration in self.cards:
            #this card is in my hand
            return True
        if opponent_declaration in self.actualPile:
            #this card is in the pile
            return True
        #DesperateCheckery
        for card in self.cards: # do i have to lie in next step?
            if card[0]>=opponent_declaration[0]:
                #I dont have to lie in next step
                return False
        #I have to lie in next step
        return True

    def getCheckFeedback(self, checked, iChecked, iDrewCards, revealedCard, noTakenCards, log=True):
        if self.opCouldDraw:
            self.nOpponentCards += 3
            self.actualPile = self.actualPile[:-2]
        self.opCouldDraw = True
        if checked:
            if iChecked:
                if not iDrewCards:
                    #I checked opponent and was right
                    self.nOpponentCards += noTakenCards
                    self.actualPile = self.actualPile[:-1]
            else:
                if not iDrewCards:
                    #Opponent checked me and was wrong
                    self.nOpponentCards += noTakenCards
                    self.actualPile = self.actualPile[:-2]
#TODO					
class ProbabilisticChecker(YourPlayer):
	if super().checkCard(self, opponent_declaration): return True
	#TODO
	return False