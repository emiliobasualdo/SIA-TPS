import math
import random
from typing import Any

import pandas as pd

idd = 0
ARMAS = "armas"
BOTAS = "botas"
CASCOS = "cascos"
GUANTES = "guantes"
PECHERAS = "pecheras"
item_indexes = [ARMAS, BOTAS, CASCOS, GUANTES, PECHERAS]

items = {
    ARMAS: pd.DataFrame(),
    BOTAS: pd.DataFrame(),
    CASCOS: pd.DataFrame(),
    GUANTES: pd.DataFrame(),
    PECHERAS: pd.DataFrame(),
}

def set_item(k, v: pd.DataFrame):
    items[k] = v.copy(deep=True)


GUERRERO = "guerrero"
ARQUERO = "arquero"
DEFENSOR = "defensor"
INFLITRADO = "infiltrado"
characters = [GUERRERO, ARQUERO, DEFENSOR, INFLITRADO]
fitness_funcs = {
    GUERRERO: lambda a, d: 0.6 * a + 0.6 * d,
    ARQUERO: lambda a, d: 0.9 * a + 0.1 * d,
    DEFENSOR: lambda a, d: 0.3 * a + 0.8 * d,
    INFLITRADO: lambda a, d: 0.8 * a + 0.3 * d,
}

class Player:
    MIN_H = 0
    MAX_H = 0

    ARMA = 0
    BOTA = 1
    CASCO = 2
    GUANTE = 3
    PECHERA = 4
    HEIGHT = 5

    ITEMS_LEN = 5
    ATTR_LEN = 6

    def __init__(self, arma: int, bota: int, casco: int, guante: int, pechera: int, h: float, char_class: str):
        self.char_class = char_class
        self.fitness_func = fitness_funcs[char_class]
        self.attrs = [arma, bota, casco, guante, pechera, h]
        # calculamos el fitness
        global idd
        self.id = idd
        idd += 1

    @property
    def fitness(self):
        return self.calculate_fitness()

    def calculate_fitness(self):
        arma, bota, casco, guante, pechera, h = self.attrs
        atm = 0.7 - math.pow(3 * h - 5, 4) + math.pow(3 * h - 5, 2) + (h / 4)
        dem = 1.9 + math.pow(2.5 * h - 4.16, 4) - math.pow(2.5 * h - 4.16, 2) - (3 * h / 10)
        fue = 0
        agi = 0
        per = 0
        res = 0
        vid = 0
        for index, item_id in enumerate(self.attrs[0:Player.ITEMS_LEN]):
            item_scores = items[item_indexes[index]].iloc[item_id]
            fue += item_scores["Fu"]
            agi += item_scores["Ag"]
            per += item_scores["Ex"]
            res += item_scores["Re"]
            vid += item_scores["Vi"]

        fue = 100 * math.tanh(0.01 * fue)
        agi = math.tanh(0.01 * agi)
        per = 0.6 * math.tanh(0.01 * per)
        res = math.tanh(0.01 * res)
        vid = 100 * math.tanh(0.01 * vid)

        a = (agi + per) * fue * atm
        d = (res + per) * vid * dem

        return self.fitness_func(a, d)

    def set_item(self, index, item_value):
        self.attrs[index] = item_value

    def copy(self):
        return Player(*self.attrs, self.char_class)

    def __repr__(self):
        resp = "("
        resp += ",".join(str(x) for x in self.attrs)
        return resp + ")"

    def __iter__(self):
        return [*self.attrs, self.fitness].__iter__()

    @classmethod
    def set_height(cls, min_h: float, max_h: float):
        cls.MIN_H = min_h
        cls.MAX_H = max_h

    @classmethod
    def random_attr(cls, index):
        if index == Player.HEIGHT:
            return random.uniform(cls.MIN_H, cls.MAX_H)
        df = items[item_indexes[index]]
        return df.index[random.randint(0, len(df.index) - 1)]

    @classmethod
    def rand_player(cls, char_class: str):
        return Player(
            random.randint(0, len(items[ARMAS]) - 1),
            random.randint(0, len(items[BOTAS]) - 1),
            random.randint(0, len(items[CASCOS]) - 1),
            random.randint(0, len(items[GUANTES]) - 1),
            random.randint(0, len(items[PECHERAS]) - 1),
            random.uniform(cls.MIN_H, cls.MAX_H),
            char_class
        )

