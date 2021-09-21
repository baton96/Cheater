from abc import ABC, abstractmethod
import random


class Player(ABC):
    def __init__(self, name=None):
        self.name = name or self.__class__.__name__
        self.cards = None

    def __str__(self):
        return self.name

    @abstractmethod
    def put(self, declared_card):
        """
        Declare card to be put on the pile or draw from pile.

        :param declared_card: card declared to be on the top of the pile, None if pile is empty
        :return: "draw" or tuple (true card put on the pile, declared card put on the pile)
        :raises TypeError: Can't instantiate abstract class Player with abstract methods
        """
        raise TypeError
        # return self.cards[0], self.cards[0]

    @abstractmethod
    def check(self, opponent_declaration):
        """
        Check

        :param opponent_declaration:
        :return: bool
        :raises TypeError: Can't instantiate abstract class Player with abstract methods
        """
        raise TypeError

    def feedback(self, checked, i_checked, i_drew, true_card, n_cards_taken, log=False):
        """
        :param checked: True -> someone checked, if False remaining inputs do not play any role
        :param i_checked: True -> I checked, False -> my opponent checked
        :param i_drew: True -> I checked but was wrong or my opponent checked and was right, False -> otherwise
        :param true_card: true card on top of the pile
        :param n_cards_taken: number of cards taken
        :param log:
        :return:
        """
        if not log:
            return
        if not checked:
            print(f"{self.name}: I don't check")
            return

        who_checked = "I" if i_checked else "My Opponent"
        who_drew = "I" if i_drew else "My Opponent"
        print(f"{self.name}: {who_checked} check and {who_drew} draw {n_cards_taken} cards")

    def start(self, cards):
        self.cards = cards

    # Add some cards to player's hand (if player checked opponent's move, but player was wrong)
    def take(self, cards_to_take):
        self.cards = self.cards + cards_to_take


class RandomPlayer(Player, ABC):
    def put(self, declared_card):
        # Last card held is worse than the one at the top of the pile - draw from the pile
        if len(self.cards) == 1 and declared_card is not None and self.cards[0][0] < declared_card[0]:
            return "draw"

        # Randomly decide which card to put on the table
        card = random.choice(self.cards)
        declaration = card

        # Randomly decide whether to cheat or not
        cheat = random.choice([True, False])
        # If decided to cheat, randomly declare the card
        if cheat:
            declaration = random.choice(self.cards)

        # If pile is not empty and card on the top of the pile is better
        if declared_card is not None and declaration[0] < declared_card[0]:
            declaration = (min(declared_card[0] + 1, 14), declaration[1])

        # Return decision (true card, declared card)
        return card, declaration

    # Randomly decide whether to check or not
    def check(self, opponent_declaration):
        return random.choice([True, False])


class DrawPlayer(Player, ABC):
    # Always draw
    def put(self, declared_card):
        return "draw"

    # Randomly decide whether to check or not
    def check(self, opponent_declaration):
        return random.choice([True, False])


class SimplePlayer(Player, ABC):
    def put(self, declared_card):
        # Last card held is worse than the one at the top of the pile - draw from the pile
        if len(self.cards) == 1 and declared_card is not None and self.cards[0][0] < declared_card[0]:
            return "draw"

        # Worst card held
        card = min(self.cards, key=lambda x: x[0])
        declaration = (card[0], card[1])

        if declared_card is not None and card[0] < declared_card[0]:
            declaration = (min(declared_card[0] + 1, 14), declaration[1])

        return card, declaration

    def check(self, opponent_declaration):
        # This card is in my hand - check
        if opponent_declaration in self.cards:
            return True
        # Randomly decide whether to check or not
        return random.choices([True, False], [0.3, 0.7], k=1)[0]
