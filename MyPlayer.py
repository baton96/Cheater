from players import Player
from abc import ABC
import random


class MyPlayer(Player, ABC):
    def __init__(self, name=None):
        super().__init__(name)

        # Value determined empirically during tests
        self.advantage_offset = 2

        self.nOpponentCards = None
        self.cards = None
        self.pile = None

    def start(self, cards):
        self.nOpponentCards = len(cards)
        self.cards = sorted(cards)
        self.pile = []

    def take(self, cards_to_take):
        self.cards = sorted(self.cards + cards_to_take)

    def put(self, declared_card):
        # Empty pile - put worst card held
        if declared_card is None:
            self.pile.append(self.cards[0])
            return self.cards[0], self.cards[0]

        # Last card held is worse than the one at the top of the pile - draw from the pile
        if len(self.cards) == 1 and self.cards[0][0] < declared_card[0]:
            self.pile = self.pile[:-1]
            return "draw"

        # Check if I have to cheat
        for card in self.cards:
            # I have a card not worse than the one at the top of the pile
            if card[0] >= declared_card[0]:
                winning = len(self.cards) <= self.nOpponentCards + self.advantage_offset
                if winning:
                    # Put and declare that card
                    self.pile.append(card)
                    return card, card
                else:
                    # Declare that card but put worst card held
                    self.pile.append(self.cards[0])
                    return self.cards[0], card
        # I have to cheat so put worst card held
        else:
            # Declare previously put card if it's no worse that the one on top
            previous_card = self.pile[-1]
            if previous_card[0] >= declared_card[0]:
                self.pile.append(self.cards[0])
                return self.cards[0], previous_card

            # Declare card with same value as card on top but different color
            declared_color = random.choice(list({1, 2, 3, 4} - {declared_card[1]}))
            self.pile.append(self.cards[0])
            return self.cards[0], (declared_card[0], declared_color)

    def check(self, opponent_declaration):
        self.nOpponentCards -= 1

        # This card is in my hand - check
        if opponent_declaration in self.cards:
            return True

        # This card is in the pile - check
        if opponent_declaration in self.pile:
            return True

        # Check whether I would have to cheat in the next step
        for card in self.cards:
            # I dont have to lie in next step - don't check
            if card[0] >= opponent_declaration[0]:
                return False

        # I would have to cheat in next step - check before cheating
        return True

    def feedback(self, checked, i_checked, i_drew, true_card, n_cards_taken, log=False):
        if not checked and n_cards_taken:
            self.nOpponentCards += n_cards_taken
            if n_cards_taken == 3:
                self.pile = self.pile[:-2]
            else:
                self.pile = self.pile[:-1]

        if checked and not i_drew:
            if i_checked:
                # I checked opponent and was right
                self.nOpponentCards += n_cards_taken
                self.pile = self.pile[:-1]
            else:
                # Opponent checked me and was wrong
                self.nOpponentCards += n_cards_taken
                self.pile = self.pile[:-2]
