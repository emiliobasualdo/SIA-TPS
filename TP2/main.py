import configparser
import json
import math
import os
import random
import pandas as pd
import plotly.express as px

import asyncio
import websockets

pd.options.plotting.backend = "plotly"
from Player import items, set_item, rand_player, Player, characters
from cross_over_methods import one_point, two_points, anular, uniform
from mutation_methods import single_gen, multi_gen_lim, multi_gen_uni
from selection_methods import random_sel, elite, roulette, universal

_config = configparser.ConfigParser()

MAX_ITEMS = 10000  # todo <--- borrar cuando terminamos
MAX_ITERATIONS = 500  # todo <--- borrar cuando terminamos

selection_methods = {
    "random": random_sel,
    "elite": elite,
    "universal": universal,
    "roulette": roulette,
}

def calculate_stats(generation: [Player]):
    min_fitness = float("inf")
    max_fitness = 0
    avg_fitness = 0

    for player in generation:
        avg_fitness += player.fitness
        if min_fitness > player.fitness:
            min_fitness = player.fitness
        if max_fitness < player.fitness:
            max_fitness = player.fitness
    if len(generation):
        avg_fitness /= len(generation)
    return min_fitness, avg_fitness, max_fitness

async def main(websocket, path):
    # cargamos las configuraciones
    print("Cargando configuración")
    config = _config["DEFAULT"]
    if config["seed"] != "None":
        random.seed(int(config["seed"]))

    # cargamos los items
    print(f"Cargando {MAX_ITEMS} items")
    items_dir = config["items_directory"]
    for key in items.keys():
        set_item(key,
                 pd.read_csv(os.path.join(items_dir, f'{key}.tsv'), index_col="id", sep="\t", header=0, nrows=MAX_ITEMS))

    # creamos los generation random
    N = int(config["N"])
    k = int(config["k"])
    min_h = float(config["min_h"])
    max_h = float(config["max_h"])
    char_class = config["character_class"]
    assert char_class in characters
    print(f"Creando generation N={N} players {char_class}")
    generation = []
    for i in range(N):
        generation.append(rand_player(min_h, max_h, char_class))

    # generamos las funciones según config
    sel_config = _config["SELECTION"]
    selection_method1 = selection_methods[sel_config["method1"]]
    selection_method2 = selection_methods[sel_config["method2"]]
    A = float(sel_config["A"])
    selection = lambda pls: selection_method1(pls, math.floor(k*A)) + selection_method2(pls, math.ceil(k*(1-A)))

    co_config = _config["CROSS_OVER"]
    cross_over_method = co_config["method"]
    if cross_over_method == "one_point":
        point = int(co_config["point"])
        assert 0 <= point <= 6
        cross_over = lambda pls: one_point(pls, point)
    elif cross_over_method == "two_points":
        points = co_config["points"].split(",")
        point_1 = int(points[0])
        point_2 = int(points[1])
        assert 0 <= point_1 < point_2 <= Player.ATTR_LEN-1
        cross_over = lambda pls: two_points(pls, point_1, point_2)
    elif cross_over_method == "anular":
        point = int(co_config["point"])
        length = int(co_config["length"])
        assert 0 <= point + length <= Player.ATTR_LEN-1
        cross_over = lambda pls: anular(pls, point, length)
    elif cross_over_method == "uniform":
        cross_over = uniform
    else:
        raise AttributeError(f"No such CrossOver method {cross_over_method}")

    mu_config = _config["MUTATION"]
    mutation_method = mu_config["method"]
    if mutation_method == "single_gen":
        mutation = single_gen
    elif mutation_method == "multi_gen_uni":
        mutation = multi_gen_uni
    elif mutation_method == "multi_gen_lim":
        M = int(mu_config["M"])
        mutation = lambda pls: multi_gen_lim(pls, M)
    else:
        raise AttributeError(f"No such Mutation method {cross_over_method}")


    new_sel_config = _config["NEW_GEN_SELECTION"]
    new_generation_selection_method1 = selection_methods[new_sel_config["method1"]]
    new_generation_selection_method2 = selection_methods[new_sel_config["method2"]]
    B = float(new_sel_config["B"])
    fill = new_sel_config["fill"]
    if fill == "all":
        new_generation_selection = lambda k_parents, k_kids: new_generation_selection_method1(k_parents + k_kids, math.floor(N*B)) + new_generation_selection_method1(k_parents + k_kids, math.floor(N*(1-B)))
    else:
        if k >= N:
            new_generation_selection = lambda k_parents, k_kids: new_generation_selection_method1(k_kids, math.floor(N*B)) + new_generation_selection_method1(k_kids, math.floor(N*(1-B)))
        else:
            new_generation_selection = lambda k_parents, k_kids: k_kids + new_generation_selection_method2(k_parents, math.floor((N - k)*B)) + new_generation_selection_method2(k_parents, math.floor((N - k)*(1-B)))

    # iteramos
    print(f"Iterando {MAX_ITERATIONS} veces")
    for i in range(MAX_ITERATIONS):
        if i % 5 == 0:
            min_f, avg_f, max_f = calculate_stats(generation)
            await websocket.send(json.dumps((i, min_f, avg_f, max_f, len(generation))))
        k_parents = selection(generation)
        k_kids = cross_over(k_parents)
        mutation(k_kids)
        generation = new_generation_selection(k_parents, k_kids)

    res_df = pd.DataFrame().from_records(generation,
                                columns=["armas", "botas", "cascos", "guantes", "pecheras", "height", "fitness"])
    print("Listo")
    if config["graphs"] == "true":
        px.box(res_df[["height", "fitness"]], x="height", y="fitness").show()
        #px.box(res_df[["height", "fitness"]], x="height", y="fitness").show()


class Ws_mock:
    @staticmethod
    async def send(data):
        pass
if __name__ == '__main__':
    _config.read('config.cfg')
    ws_config = _config["WEBSOCKET"]
    if ws_config["enable"] == "true":
        start_server = websockets.serve(main, "localhost", ws_config["port"])
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()
    else:
        asyncio.run(main(Ws_mock(), ""))