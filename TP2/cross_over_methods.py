from Player import Player


def one_point(players:[Player], point:int):
    new_born = []
    # agarramos de a pares
    for i in range(int(len(players)/2)):
        new_p = Player(*players[i].attrs[0:point], *players[i+1].attrs[point:])
        new_born.append(new_p)
    players.extend(new_born)

