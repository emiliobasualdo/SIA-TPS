import math
import random

from Player import Player


def random_sel(players: [Player], k: int) -> [Player]:
    selection = []
    for i in range(k):
        selected = players[random.randint(0, len(players) - 1)].copy()
        selection.append(selected)
    return selection


def _sorter(p: Player):
    return p.fitness


def elite(players: [Player], k: int) -> [Player]:
    selection = []
    players.sort(key=_sorter, reverse=True)
    N = len(players)
    for i in range(len(players)):
        if k-i <= 0:
            break
        p_count = math.ceil((k-i)/N)
        for _ in range(p_count):
            selection.append(players[i].copy())
    return selection


def roulette(players: [Player], k: int) -> [Player]:
    population_fitness = 0
    r = 0
    selection = []
    player_accumulative_fitness = [(0, None)]
    accumulative_fitness = 0
    for player in players:
        population_fitness = population_fitness + player.fitness
    for player in players:
        relative_fitness = player.fitness / population_fitness
        accumulative_fitness = accumulative_fitness + relative_fitness
        player_accumulative_fitness.append((accumulative_fitness, player))
    for i in range(k):
        r = random.uniform(0, 1)
        for j in range((len(player_accumulative_fitness) - 1)):
            lower_value = player_accumulative_fitness[j][0]
            upper_value = player_accumulative_fitness[j + 1][0]

            if lower_value <= r <= upper_value:
                selection.append(player_accumulative_fitness[j + 1][1])
    return selection


def universal(players: [Player], k: int) -> [Player]:
    population_fitness = 0
    r = 0
    selection = []
    player_accumulative_fitness = [(0, None)]
    accumulative_fitness = 0
    for player in players:
        population_fitness = population_fitness + player.fitness
    for player in players:
        relative_fitness = player.fitness / population_fitness
        accumulative_fitness = accumulative_fitness + relative_fitness
        player_accumulative_fitness.append((accumulative_fitness, player))
    for i in range(k):
        random_number = random.uniform(0, 1)
        r = (random_number + i) / k
        for j in range((len(player_accumulative_fitness) - 1)):
            lower_value = player_accumulative_fitness[j][0]
            upper_value = player_accumulative_fitness[j + 1][0]

            if lower_value <= r <= upper_value:
                selection.append(player_accumulative_fitness[j + 1][1])
    return selection

# retocar roulette y universal
