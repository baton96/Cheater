from abc import ABC

from players import Player
import random


class TestPlayer(Player, ABC):
    def __init__(self, name):
        super().__init__(name)
        self.puttingStrategy = 'HonestPutter'
        self.checkingStrategy = None
        self.nOpponentCards = None
        self.useLastCard = False
        self.opCanDraw = False
        self.winOption = None
        self.true_pile = None
        self.nOption = None
        self.pile = None

    def start(self, cards):
        super().start(cards)
        self.pile = []

    def simple(self, declared_card):
        declared_color = random.choice(list({1, 2, 3, 4} - {declared_card[1]}))
        self.pile.append(self.cards[0])
        return self.cards[0], (declared_card[0], declared_color)

    def last_card(self, declared_card):
        if len(self.true_pile) > 0 and self.true_pile[-1][0] >= declared_card[0]:
            self.pile.append(self.cards[0])
            return self.cards[0], self.true_pile[-2]
        else:
            return self.simple(declared_card)

    def put(self, declared_card):
        for i, card in enumerate(self.cards):  # try not to cheat
            # I don't have to cheat
            if card[0] >= declared_card[0]:
                if self.puttingStrategy == 'HonestPutter':
                    # give worst allowed card
                    declared_card = card
                    true_card = card                    
                elif self.puttingStrategy == 'SneakyPutter':
                    # give worst card and declare worst allowed card
                    declared_card = card
                    true_card = self.cards[0]                    
                elif self.puttingStrategy == 'WinningPutter':
                    winning = len(self.cards) <= self.nOpponentCards + self.winOption
                    if winning:  # play Honest
                        declared_card = card
                        true_card = card                        
                    else:  # play Sneaky
                        declared_card = card
                        true_card = self.cards[0]
                elif self.puttingStrategy == 'OnlyNPutter':
                    if i < self.nOption:  # play Honest
                        declared_card = card
                        true_card = card                        
                    else:  # play Sneaky
                        declared_card = card
                        true_card = self.cards[0]                        
                elif self.puttingStrategy == 'WinningAndOnlyNPutter':
                    winning = len(self.cards) <= self.nOpponentCards + self.winOption
                    if winning and i < self.nOption:  # play Honest
                        declared_card = card
                        true_card = card                        
                    else:  # play Sneaky
                        declared_card = card
                        true_card = self.cards[0]                        
                elif self.puttingStrategy == 'WinningOrOnlyNPutter':
                    winning = len(self.cards) <= self.nOpponentCards + self.winOption
                    if winning or i < self.nOption:  # play Honest
                        declared_card = card
                        true_card = card                        
                    else:  # play Sneaky
                        declared_card = card
                        true_card = self.cards[0]            
                else:
                    # by default don't cheat
                    true_card = card

                self.pile.append(true_card)
                return true_card, declared_card

        # I have to cheat
        else:
            if self.useLastCard:
                return self.last_card(declared_card)
            else:
                return self.simple(declared_card)

    def check(self, opponent_declaration):
        if super().check(opponent_declaration):
            return True

        if (
                self.checkingStrategy == 'PreLastChecker' and
                self.nOpponentCards == 1 and
                self.nOpponentCards < len(self.cards)
        ):
            # Opponent has last card and is winning - check
            return True

        return False
