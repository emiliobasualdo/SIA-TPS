import random

from Player import Player, random_item


def single_gen(players:[Player]):
    for player in players:
        rand_item_index = random.randint(0,4)
        rand_item_value = random_item(rand_item_index)
        player.set_item(rand_item_index, rand_item_value)