import random

from Player import Player, random_item


# todo hay que re-hacer esto. Solo se estan mutando los atributos. Hay que mutar altura y character tambien
def single_gen(players: [Player]):
    for player in players:
        rand_item_index = random.randint(0, Player.ITEMS_LEN - 1)
        rand_item_value = random_item(rand_item_index)
        player.set_item(rand_item_index, rand_item_value)


def multi_gen_lim(players: [Player], M: int):
    for player in players:
        for i in range(M):
            rand_item_index = random.randint(0, Player.ITEMS_LEN - 1)
            rand_item_value = random_item(rand_item_index)
            player.set_item(rand_item_index, rand_item_value)

def multi_gen_uni(players: [Player]):
    for player in players:
        for item_i in range(Player.ITEMS_LEN):
            rand_item_value = random_item(item_i)
            player.set_item(item_i, rand_item_value)
