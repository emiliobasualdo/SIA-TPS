import math
import random
import copy
from Player import Player

kbol = 1.380649e-23

def _sorter(p: Player):
    return p.fitness

def random_sel(players: [Player], k: int) -> [Player]:
    selection = []
    for i in range(k):
        selected = players[random.randint(0, len(players) - 1)].copy()
        selection.append(selected)
    return selection

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

def roulette(players: [Player], k: int, fitness_accessor=Player.F_ACCESSOR) -> [Player]:
    population_fitness = 0
    r = 0
    selection = []
    player_accumulative_fitness = [(0, None)]
    accumulative_fitness = 0
    for player in players:
        population_fitness = population_fitness + player[fitness_accessor]
    for player in players:
        relative_fitness = player[fitness_accessor] / population_fitness
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

def ranking(players: [Player], k: int) -> [Player]:
    selection = []
    players.sort(key=_sorter, reverse=True)
    population = len(players)
    for i, player in enumerate(players):
        relative_fitness = (population - i) / population
        player.relative_fitness = relative_fitness

    ranked_players = roulette(players, k, Player.RF_ACCESSOR)
    for ranked_player in ranked_players:
        for player in players:
            if player.id == ranked_player.id:
                selection.append(player)
                break

    return selection

def det_tourn(players: [Player], k: int, m: int) -> [Player]:
    selection = []
    population = len(players)
    for i in range(k):
        first_selection = players[random.randint(0, population - 1)].copy()
        for j in range(m):
            m_selection = players[random.randint(0, population - 1)].copy()
            if m_selection.fitness > first_selection.fitness:
                first_selection = m_selection
        selection.append(first_selection)
    return selection

def prob_tourn(players: [Player], k: int, threshold: float) -> [Player]:
    selection = []
    population = len(players)
    for i in range(k):
        first_selection = players[random.randint(0, population - 1)].copy()
        second_selection = players[random.randint(0, population - 1)].copy()
        r = random.uniform(0, 1)
        if r < threshold:
            if first_selection.fitness > second_selection.fitness:
                selection.append(first_selection)
            else:
                selection.append(second_selection)

        else:
            if first_selection.fitness < second_selection.fitness:
                selection.append(first_selection)
            else:
                selection.append(second_selection)

    return selection

def boltzmann(players: [Player], k: int, ti: int, t0: float, tc: float) -> [Player]:
    selection = []
    val = tc + (t0 - tc) * math.exp(-kbol * ti)
    population_average = sum(list(map(lambda player: math.exp(player.fitness/val), players)))/len(players)
    for i, player in enumerate(players):
        relative_fitness = math.exp(player.fitness/val)/population_average
        player.relative_fitness = relative_fitness

    ranked_players = roulette(players, k, Player.RF_ACCESSOR)
    for ranked_player in ranked_players:
        for player in players:
            if player.id == ranked_player.id:
                selection.append(player)
                break

    return selection

#retocar roulette y universal
