import random

from Player import Player


def one_point(players: [Player]):
    new_born = []
    # agarramos de a pares
    for i in range(int(len(players) / 2)):
        point = random.randint(0, Player.ITEMS_LEN)
        new_p = Player(*players[i].attrs[0:point], *players[i + 1].attrs[point:], players[0].char_class)
        new_born.append(new_p)
        new_p = Player(*players[i + 1].attrs[0:point], *players[i].attrs[point:], players[0].char_class)
        new_born.append(new_p)
    return new_born


def two_points(players: [Player]):
    new_born = []
    # agarramos de a pares
    for i in range(int(len(players) / 2)):
        point1 = random.randint(0, Player.ITEMS_LEN)
        point2 = random.randint(0, Player.ITEMS_LEN)
        new_p = Player(*players[i].attrs[0:point1],
                       *players[i + 1].attrs[point1:point2],
                       *players[i].attrs[point2:], players[0].char_class)
        new_born.append(new_p)
        new_p = Player(*players[i + 1].attrs[0:point1],
                       *players[i].attrs[point1:point2],
                       *players[i + 1].attrs[point2:], players[0].char_class)
        new_born.append(new_p)
    return new_born


def anular(players: [Player]):
    new_born = []
    # agarramos de a pares
    for i in range(int(len(players) / 2)):
        point = random.randint(0, Player.ITEMS_LEN)
        length = random.randint(0, Player.ITEMS_LEN - point)
        new_p = Player(*players[i].attrs[0:point],
                       *players[i + 1].attrs[point:point + length],
                       *players[i].attrs[point + length:], players[0].char_class)
        new_born.append(new_p)
        new_p = Player(*players[i + 1].attrs[0:point],
                       *players[i].attrs[point:point + length],
                       *players[i + 1].attrs[point + length:], players[0].char_class)
        new_born.append(new_p)
    return new_born

def uniform(players: [Player], Pc: float):
    new_born = []
    for i in range(int(len(players) / 2)):
        new_genes_1 = [-1] * Player.ATTR_LEN
        new_genes_2 = [-1] * Player.ATTR_LEN
        for j in range(Player.ATTR_LEN):
            if random.uniform(0, 1) < Pc:
                new_genes_1[j] = players[i].attrs[j]
                new_genes_2[j] = players[i+1].attrs[j]
            else:
                new_genes_1[j] = players[i+1].attrs[j]
                new_genes_2[j] = players[i].attrs[j]
        new_born.append(Player(*new_genes_1, players[0].char_class))
        new_born.append(Player(*new_genes_2, players[0].char_class))
    return new_born