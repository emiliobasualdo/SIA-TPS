import random

from Player import Player


def one_point(players: [Player], point: int):
    new_born = []
    # agarramos de a pares
    for i in range(int(len(players) / 2)):
        new_p = Player(*players[i].attrs[0:point], *players[i + 1].attrs[point:])
        new_born.append(new_p)
        new_p = Player(*players[i + 1].attrs[0:point], *players[i].attrs[point:])
        new_born.append(new_p)
    players.extend(new_born)


def two_points(players: [Player], point_1: int, point_2: int):
    new_born = []
    # agarramos de a pares
    for i in range(int(len(players) / 2)):
        new_p = Player(*players[i].attrs[0:point_1],
                       *players[i + 1].attrs[point_1:point_2],
                       *players[i].attrs[point_2:])
        new_born.append(new_p)
        new_p = Player(*players[i + 1].attrs[0:point_1],
                       *players[i].attrs[point_1:point_2],
                       *players[i + 1].attrs[point_2:])
        new_born.append(new_p)
    players.extend(new_born)


def anular(players: [Player], point: int, length: int):
    new_born = []
    # agarramos de a pares
    for i in range(int(len(players) / 2)):
        new_p = Player(*players[i].attrs[0:point],
                       *players[i + 1].attrs[point:point + length],
                       *players[i].attrs[point + length:])
        new_born.append(new_p)
        new_p = Player(*players[i + 1].attrs[0:point],
                       *players[i].attrs[point:point + length],
                       *players[i + 1].attrs[point + length:])
        new_born.append(new_p)
    players.extend(new_born)

def uniform(players: [Player]):
    for i in range(int(len(players) / 2)):
        new_genes = [-1] * Player.ATTR_LEN
        for j in range(Player.ATTR_LEN):
            if random.uniform(0, 1) < 0.5:
                new_genes[j] = players[i].attrs[j]
            else:
                new_genes[j] = players[i+1].attrs[j]