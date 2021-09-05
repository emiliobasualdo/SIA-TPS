import random

from Player import Player


# todo hay que re-hacer esto. Solo se estan mutando los atributos. Hay que mutar altura y character tambien
def single_gen(player: Player, Pm: float):
    if random.uniform(0, 1) <= Pm:
        rand_item_index = random.randint(0, Player.ATTR_LEN - 1)
        rand_item_value = Player.random_attr(rand_item_index)
        player.set_item(rand_item_index, rand_item_value)


def multi_gen_lim(player: Player, M: int, Pm: float):
    for i in range(M):
        if random.uniform(0, 1) <= Pm:
            rand_item_index = random.randint(0, Player.ATTR_LEN - 1)
            rand_item_value = Player.random_attr(rand_item_index)
            player.set_item(rand_item_index, rand_item_value)

def multi_gen_uni(player: Player, Pms: [float]):
    for item_i in range(Player.ATTR_LEN):
        if random.uniform(0, 1) <= Pms[item_i]:
            rand_item_value = Player.random_attr(item_i)
            player.set_item(item_i, rand_item_value)

def complete_mutation(player: Player, Pm: float, Pms: [float]):
    if random.uniform(0, 1) <= Pm:
        for item_i in range(Player.ATTR_LEN):
            if random.uniform(0, 1) <= Pms[item_i]:
                rand_item_value = Player.random_attr(item_i)
                player.set_item(item_i, rand_item_value)