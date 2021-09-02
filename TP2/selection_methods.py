import math
import random
import copy
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

def ranking(players: [Player], k: int, population: int) -> [Player]:
    selection = []
    ranked_players = []
    players.sort(key=_sorter, reverse=True)
    for i, player in enumerate(players):
        new_fitness = (population - i) / population
        ranked_player = copy.deepcopy(player)
        ranked_player.fitness = new_fitness
        ranked_players.append(ranked_player)

    ranked_players = roulette(ranked_players, k)
    for ranked_player in enumerate(ranked_players):
        for player in enumerate(players):
            if player.idd == ranked_player.idd:
                selection.append(player)
                break

    return selection

def deterministic_tournament(players: [Player], k: int, population: int, m: int) -> [Player]:
    selection = []
    for i in range(k):
        first_selection = players[random.randint(0, population - 1)].copy()
        for j in range(m):
            m_selection = players[random.randint(0, population - 1)].copy()
            if m_selection.fitness > first_selection.fitness:
                first_selection = m_selection
        selection.append(first_selection)
    return selection

def probabilistic_tournament(players: [Player], k: int, population: int, m: int) -> [Player]:
    selection = []

def boltzmann(players: [Player], k: int, population: int, gen: int, t0: int, tc: int, kbol: int) -> [Player]:
	selection = []
	ranked_players = []
	val = tc + (t0 - tc) * math.exp(-kbol * gen)
	population_average = sum(list(map(lambda player: math.exp(player.fitness/val), players)))/len(players)
	for i, player in enumerate(players):
		new_fitness = math.exp(player.fitness/val)/population_average
		ranked_player = copy.deepcopy(player)
        ranked_player.fitness = new_fitness
        ranked_players.append(ranked_player)

	ranked_players = roulette(ranked_players, k)
	for ranked_player in enumerate(ranked_players):
		for player in enumerate(players):
			if player.idd == ranked_player.idd:
				selection.append(player)
				break

	return selection

#retocar roulette y universal
