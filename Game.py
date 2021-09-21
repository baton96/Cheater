from collections import Counter
import random


def get_deck(size=7):
    return [(number, color) for color in range(4) for number in range(size)]


def deal(deck, n_players, cards_per_hand=8):
    if cards_per_hand > len(deck) / n_players:
        raise Exception("Too many cards per hand to deal")

    deck_set = set(deck)
    hands = []
    for _ in range(n_players):
        hand = random.sample(deck_set, cards_per_hand)
        deck_set -= set(hand)
        hands.append(hand)
    return hands


class Game:
    def __init__(self, players):
        self.players = players
        self.n_players = len(players)
        self.stats = {player: Counter() for player in self.players}

        deck = get_deck()
        self.player_cards = deal(deck, self.n_players)
        self.used_deck = {card for cards in self.player_cards for card in cards}

        for player, cards in zip(players, self.player_cards):
            player.start(cards.copy())

        self.pile = []
        self.true_card = None
        self.declared_card = None
        self.previous_declaration = None
        self.player_id = random.choice(range(self.n_players))

    def opponent_id(self):
        return (self.player_id + 1) % self.n_players

    def draw(self, player_id):
        player = self.players[player_id]
        n_to_take = min(len(self.pile), 3)
        to_take = self.pile[-n_to_take:]
        player.take(to_take)
        for c in to_take:
            self.pile.remove(c)
        self.player_cards[player_id].extend(to_take)
        self.declared_card = None
        self.true_card = None
        return to_take

    def take_turn(self):
        self.player_id = self.opponent_id()
        player = self.players[self.player_id]
        opponent = self.players[self.opponent_id()]

        self.previous_declaration = self.declared_card
        decision = player.put(self.declared_card)

        if decision == "draw":
            self.stats[player]['draws'] += 1
            to_take = self.draw(self.player_id)
            player.feedback(False, False, False, None, None)
            opponent.feedback(False, False, False, None, len(to_take))
            return self.debug_general(), player

        self.true_card, self.declared_card = decision
        if self.true_card != self.declared_card:
            self.stats[player]['cheats'] += 1

        if not self.debug_move():
            return False, self.player_id

        player.cards.remove(self.true_card)
        self.player_cards[self.player_id].remove(self.true_card)
        self.pile.append(self.true_card)

        if opponent.check(self.declared_card):
            if not self.true_card == self.declared_card:
                to_take = self.draw(self.player_id)
                player.feedback(True, False, True, None, len(to_take))
                opponent.feedback(True, True, False, tuple(to_take[-1]), len(to_take))
            else:
                to_take = self.draw(self.opponent_id())
                player.feedback(True, False, False, None, len(to_take))
                opponent.feedback(True, True, True, tuple(to_take[-1]), len(to_take))
        else:
            player.feedback(False, False, False, None, None)
            opponent.feedback(False, False, False, None, None)

        return self.debug_general(), player

    def finished(self, log=False):
        player = self.players[self.player_id]
        if len(player.cards) == 0:
            if log:
                print(f"{player} wins!")
            return True
        return False

    def debug_move(self):
        if (
                self.previous_declaration is not None and
                self.true_card[0] < self.previous_declaration[0] and
                len(self.players[self.player_id].cards) == 1
        ):
            print("[ERROR] Last played card should be valid (it is revealed, you cannot cheat)!")
            return False
        if len(self.true_card) != 2:
            print("[ERROR] You put too many cards!")
            return False
        if self.true_card not in self.player_cards[self.player_id]:
            print("[ERROR] You do not have this card!")
            return False
        if self.true_card not in self.used_deck:
            print("[ERROR] There is no such card!")
            return False
        if (self.previous_declaration is not None) and len(self.pile) == 0:
            print("[ERROR] Inconsistency")
            return False
        if (self.previous_declaration is not None) and (self.declared_card[0] < self.previous_declaration[0]):
            print("[ERROR] Improper move!")
            return False
        return True

    def debug_general(self):
        for i, player in enumerate(self.players):
            if set(player.cards) != set(self.player_cards[i]):
                return False
        hand_cards = {card for hand in self.player_cards for card in hand}
        game_deck = hand_cards | set(self.pile)
        if game_deck != self.used_deck:
            return False

        return True
