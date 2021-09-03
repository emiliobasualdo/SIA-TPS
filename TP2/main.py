import configparser
import json
import math
import os
import random
import pandas as pd
import plotly.express as px
import time

import asyncio
import websockets

pd.options.plotting.backend = "plotly"
from Player import items, set_item, Player, characters
from cross_over_methods import one_point, two_points, anular, uniform
from mutation_methods import single_gen, multi_gen_lim, multi_gen_uni, complete_mutation
from selection_methods import random_sel, elite, roulette, universal
from break_methods import gen_quantity, time, fitness_goal

_config = configparser.ConfigParser()

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
    print(f"Cargando items")
    items_dir = config["items_directory"]
    for key in items.keys():
        set_item(key,
                 pd.read_csv(os.path.join(items_dir, f'{key}.tsv'), index_col="id", sep="\t", header=0))

    # creamos los generation random
    N = int(config["N"])
    k = int(config["k"])
    min_h = float(config["min_h"])
    max_h = float(config["max_h"])
    char_class = config["character_class"]
    assert char_class in characters
    print(f"Creando generation N={N} players {char_class}")
    Player.set_height(min_h, max_h)
    generation = []
    for i in range(N):
        generation.append(Player.rand_player(char_class))

    # generamos las funciones según config
    sel_config = _config["SELECTION"]
    selection_method1 = selection_methods[sel_config["method1"]]
    selection_method2 = selection_methods[sel_config["method2"]]
    A = float(sel_config["A"])
    selection = lambda pls: selection_method1(pls, math.floor(k*A)) + selection_method2(pls, math.ceil(k*(1-A)))

    co_config = _config["CROSS_OVER"]
    cross_over_method = co_config["method"]
    if cross_over_method == "one_point":
        cross_over = one_point
    elif cross_over_method == "two_points":
        cross_over = two_points
    elif cross_over_method == "anular":
        cross_over = anular
    elif cross_over_method == "uniform":
        Pc = float(co_config["Pc"])
        cross_over = lambda pls: uniform(pls, Pc)
    else:
        raise AttributeError(f"No such CrossOver method {cross_over_method}")

    mu_config = _config["MUTATION"]
    mutation_method = mu_config["method"]
    if mutation_method == "single_gen":
        Pm = float(mu_config["Pm"])
        mutation = lambda pls: single_gen(pls, Pm)
    elif mutation_method == "multi_gen_uni":
        Pms = [float(i) for i in mu_config["Pms"].split(",")]
        assert len(Pms) == Player.ATTR_LEN
        mutation = lambda pls: multi_gen_uni(pls, Pms)
    elif mutation_method == "multi_gen_lim":
        M = int(mu_config["M"])
        Pm = float(mu_config["Pm"])
        mutation = lambda pls: multi_gen_lim(pls, M, Pm)
    elif mutation_method == "complete":
        Pm = float(mu_config["Pm"])
        Pms = [float(i) for i in mu_config["Pms"].split(",")]
        assert len(Pms) == Player.ATTR_LEN
        mutation = lambda pls: complete_mutation(pls, Pm, Pms)
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
    condition = None
    gen = 0

    stop_condition_method = config["stop_condition"]
    if stop_condition_method == "gen_quantity":
        condition = int(config["gen_quantity"])
        stop_condition = lambda maxf,gene,timer: gen_quantity(gene,condition)
    elif stop_condition_method == "time":
        condition = float(config["time"])
        stop_condition = lambda maxf,gene,timer: time(timer,condition)
    elif stop_condition_method =="fitness_goal":
        condition = int(config["fitness_goal"])
        stop_condition = lambda maxf,gene,timer: fitness_goal(maxf,condition)

    else:
        raise AttributeError(f"No such Stop Condition method {stop_condition_method}")

    print(f"Iterando")
    stop_condition_met = False
    start_timer = time.clock()
    while not stop_condition(max_f,gen,current_time):
        if i % 5 == 0:
            current_time = time.clock() - start_timer
            gen = gen + 5
            min_f, avg_f, max_f = calculate_stats(generation)
            await websocket.send(json.dumps((i, min_f, avg_f, max_f, len(generation))))
            if stop_condition(max_f,gen,current_time):
                stop_condition_met = True
                break
        k_parents = selection(generation)
        k_kids = cross_over(k_parents)
        mutation(k_kids)
        generation = new_generation_selection(k_parents, k_kids)

    res_df = pd.DataFrame().from_records(generation,
                                columns=["armas", "botas", "cascos", "guantes", "pecheras", "height", "fitness"])
    print(f"Stop_condition_met = {stop_condition_met}")
    if config["graphs"] == "true":
        #px.box(res_df[["height", "fitness"]], x="height", y="fitness").show()
        #px.box(res_df[["height", "fitness"]], x="height", y="fitness").show()
        top = res_df.nlargest(10, ["fitness"], keep="all")
        print(top)
        px.scatter(top, x="height", y="fitness", ).show()


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