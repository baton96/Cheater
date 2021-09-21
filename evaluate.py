from players import SimplePlayer, RandomPlayer
from collections import Counter
from MyPlayer import MyPlayer
from Game import Game


def evaluate(repeats=100):
    player1 = RandomPlayer()
    player2 = SimplePlayer()
    player3 = MyPlayer()
    players = [player1, player2, player3]
    # random.seed(0)
    errors = 0

    stats = {}
    for player in players:
        stats[player] = Counter(wins=0)

    for _ in range(repeats):
        game = Game(players)
        error = False
        while True:
            valid, player = game.take_turn()
            if not valid:
                error = True
                errors += 1
                break

            if game.finished():
                stats[player]["wins"] += 1
                break

        if not error:
            for player in players:
                stats[player] += game.stats[player]
    valid_repeats = repeats - errors

    print("%-20s" % "", " ".join("%-20s" % player for player in players))
    stat_names = ["wins", "cheats", "checks", "draws"]
    for stat in stat_names:
        print("%-20s" % stat.title(), " ".join("%-20s" % (stats[player][stat] / valid_repeats) for player in players))


if __name__ == '__main__':
    evaluate()
