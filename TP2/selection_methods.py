import random

from Player import Player

def random_selection(players: [Player], k: int) -> [Player]:
    selection = []
    for i in range(k):
        selected = players[random.randint(0, len(players)-1)].copy()
        selection.append(selected)
    return selection


def elite_selection(players: [Player], k: int) -> [Player]:
    raise NotImplemented()
