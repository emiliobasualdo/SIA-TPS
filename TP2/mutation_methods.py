import random

from Player import Player, random_item


# todo hay que re-hacer esto. Solo se estan mutando los atributos. Hay que mutar altura y character tambien
def single_gen(players: [Player], Pm: float):
    for player in players:
        if random.uniform(0, 1) <= Pm:
            rand_item_index = random.randint(0, Player.ITEMS_LEN - 1)
            rand_item_value = random_item(rand_item_index)
            player.set_item(rand_item_index, rand_item_value)


def multi_gen_lim(players: [Player], M: int, Pm: float):
    for player in players:
        for i in range(M):
            if random.uniform(0, 1) <= Pm:
                rand_item_index = random.randint(0, Player.ITEMS_LEN - 1)
                rand_item_value = random_item(rand_item_index)
                player.set_item(rand_item_index, rand_item_value)

def multi_gen_uni(players: [Player], Pms: [float]):
    for player in players:
        for item_i in range(Player.ITEMS_LEN):
            if random.uniform(0, 1) <= Pms[item_i]:
                rand_item_value = random_item(item_i)
                player.set_item(item_i, rand_item_value)

def complete_mutation(players: [Player], Pm:float, Pms: [float]):
    for player in players:
        if random.uniform(0, 1) <= Pm:
            for item_i in range(Player.ITEMS_LEN):
                if random.uniform(0, 1) <= Pms[item_i]:
                    rand_item_value = random_item(item_i)
                    player.set_item(item_i, rand_item_value)