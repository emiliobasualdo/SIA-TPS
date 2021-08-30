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

def roulette_selection(players: [Player], k: int) -> [Player]:
    population_fitness = 0
    r = 0
    selection = []
    player_accumulative_fitness = [(0, None)]
    for player in players:
        population_fitness = population_fitness + player.fitness
    for player in players:
        relative_fitness = player.fitnes / population_fitness
        accumulative_fitness = accumulative_fitness + relative_fitness
        player_accumulative_fitness.append(accumulative_fitness, player)
    for i in range(k):
        r = random.uniform(0, 1)
        for j in range((len(player_accumulative_fitness)-1)):
            lower_value = player_accumulative_fitness[j][0]
            upper_value = player_accumulative_fitness[j+1][0]

            if r in range(lower_value, upper_value):
                selection.append(player_accumulative_fitness[j+1][1])
    return selection

def universal_selection(players: [Player], k: int) -> [Player]:
    population_fitness = 0
    r = 0
    selection = []
    player_accumulative_fitness = [(0, None)]
    for player in players:
        population_fitness = population_fitness + player.fitness
    for player in players:
        relative_fitness = player.fitnes / population_fitness
        accumulative_fitness = accumulative_fitness + relative_fitness
        player_accumulative_fitness.append(accumulative_fitness, player)
    for i in range(k):
        random_number = random.uniform(0, 1)
        r = (random_number + i) / k
        for j in range((len(player_accumulative_fitness) - 1)):
            lower_value = player_accumulative_fitness[j][0]
            upper_value = player_accumulative_fitness[j + 1][0]

            if r in range(lower_value, upper_value):
                selection.append(player_accumulative_fitness[j + 1][1])
    return selection

#retocar roulette y universal

