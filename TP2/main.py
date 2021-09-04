import configparser
import json
import math
import os
import random
from datetime import datetime

import pandas as pd
import plotly.express as px
import time

import asyncio
import websockets

pd.options.plotting.backend = "plotly"
from Player import items, set_item, Player, characters
from cross_over_methods import one_point, two_points, anular, uniform
from mutation_methods import single_gen, multi_gen_lim, multi_gen_uni, complete_mutation
from selection_methods import random_sel, elite, roulette, universal, ranking, det_tourn, prob_tourn, boltzmann
from break_methods import gen_quantity, fitness_goal, stop_by_time

_config = configparser.ConfigParser()


def _mu_method(config):
    mutation_method = config["method"]
    if mutation_method == "single_gen":
        Pm = float(config["Pm"])
        mutation = lambda pls: single_gen(pls, Pm)
    elif mutation_method == "multi_gen_uni":
        Pms = [float(i) for i in config["Pms"].split(",")]
        assert len(Pms) == Player.ATTR_LEN
        mutation = lambda pls: multi_gen_uni(pls, Pms)
    elif mutation_method == "multi_gen_lim":
        M = int(config["M"])
        Pm = float(config["Pm"])
        mutation = lambda pls: multi_gen_lim(pls, M, Pm)
    elif mutation_method == "complete":
        Pm = float(config["Pm"])
        Pms = [float(i) for i in config["Pms"].split(",")]
        assert len(Pms) == Player.ATTR_LEN
        mutation = lambda pls: complete_mutation(pls, Pm, Pms)
    else:
        raise AttributeError(f"No such Mutation method {mutation_method}")
    return mutation

def _cross_over_method(config):
    cross_over_method = config["method"]
    if cross_over_method == "one_point":
        cross_over = one_point
    elif cross_over_method == "two_points":
        cross_over = two_points
    elif cross_over_method == "anular":
        cross_over = anular
    elif cross_over_method == "uniform":
        Pc = float(config["Pc"])
        cross_over = lambda pls: uniform(pls, Pc)
    else:
        raise AttributeError(f"No such CrossOver method {cross_over_method}")
    return cross_over

def _selection_method(config, N: int, k: int):
    def get_method(method_name, config):
        if method_name == "random":
            sel_method = lambda pls, i: random_sel(pls, k)
        elif method_name == "elite":
            sel_method = lambda pls, i: elite(pls, k)
        elif method_name == "roulette":
            sel_method = lambda pls, i: roulette(pls, k)
        elif method_name == "universal":
            sel_method = lambda pls, i: universal(pls, k)
        elif method_name == "ranking":
            sel_method = lambda pls, i: ranking(pls, k)
        elif method_name == "det_tourn":
            M = float(config["M"])
            sel_method = lambda pls, i: prob_tourn(pls, k, M)
        elif method_name == "prob_tourn":
            th = float(config["th"])
            sel_method = lambda pls, i: prob_tourn(pls, k, th)
        elif method_name == "boltzmann":
            t0 = float(config["t0"])
            tc = float(config["tc"])
            sel_method = lambda pls, i: boltzmann(pls, k, i, t0, tc)
        else:
            raise AttributeError(f"No such selection method {method_name}")
        return sel_method

    selection_method1 = get_method(config["method1"], config)
    selection_method2 = get_method(config["method2"], config)
    A = float(config["A"])
    if "fill" not in config:
        return lambda pls: selection_method1(pls, math.floor(k*A)) + selection_method2(pls, math.ceil(k*(1-A)))

    fill = config["fill"]
    if fill == "all":
        selection_method = lambda k_parents, k_kids: selection_method1(k_parents + k_kids, math.floor(N * A)) + selection_method2(k_parents + k_kids, math.floor(N * (1 - A)))
    else:
        if k >= N:
            selection_method = lambda k_parents, k_kids: selection_method1(k_kids, math.floor(N * A)) + selection_method2(k_kids, math.floor(N * (1 - A)))
        else:
            selection_method = lambda k_parents, k_kids: k_kids + selection_method1(k_parents, math.floor((N - k) * A)) + selection_method2(k_parents, math.floor((N - k) * (1 - A)))
    return selection_method

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
    selection = _selection_method(_config["SELECTION"], N, k)
    cross_over = _cross_over_method(_config["CROSS_OVER"])
    mutation = _mu_method(_config["MUTATION"])
    new_generation_selection = _selection_method(_config["NEW_GEN_SELECTION"], N, k)

    # iteramos
    stop_config = _config["STOP_CONDITION"]
    stop_condition_method = stop_config["stop_condition"]
    if stop_condition_method == "gen_quantity":
        condition = int(stop_config["gen_quantity"])
        stop_condition = lambda maxf,gene,timer: gen_quantity(condition, gene)
    elif stop_condition_method == "time":
        condition = float(stop_config["time"])
        stop_condition = lambda maxf,gene,timer: stop_by_time(condition, timer)
    elif stop_condition_method =="fitness_goal":
        condition = float(stop_config["fitness_goal"])
        stop_condition = lambda maxf,gene,timer: fitness_goal(condition, maxf)
    else:
        raise AttributeError(f"No such Stop Condition method {stop_condition_method}")

    print(f"Iterando")
    stop_condition_met = False
    historical_stats = []
    start_timer = datetime.now()
    max_f = 0
    i = 0
    while not stop_condition(max_f, i, (datetime.now()-start_timer).seconds):
        if i % 5 == 0:
            min_f, avg_f, max_f = calculate_stats(generation)
            stats = (i, min_f, avg_f, max_f, len(generation))
            historical_stats.append(stats)
            await websocket.send(json.dumps(stats))
        i += 1
        k_parents = selection(generation)
        k_kids = cross_over(k_parents)
        mutation(k_kids)
        generation = new_generation_selection(k_parents, k_kids)

    col_names = ["i", "min_f", "avg_f", "max_f", "N"]
    stats_df = pd.DataFrame(historical_stats, columns=col_names)
    res_df = pd.DataFrame().from_records(generation,
                                columns=["armas", "botas", "cascos", "guantes", "pecheras", "height", "fitness"])
    print(f"Stop_condition_met = {stop_condition_met}")
    if config["graphs"] == "true":
        #px.box(res_df[["height", "fitness"]], x="height", y="fitness").show()
        top = res_df.nlargest(10, ["fitness"], keep="all")
        print(top)
        px.scatter(top, x="height", y="fitness").show()
        # params = f"Character:{char_class}, N:{N}, k={k}, stop condition:{stop_condition} <br>"
        # for conf_section in ["SELECTION", "CROSS_OVER", "MUTATION", "NEW_GEN_SELECTION"]:
        #     params += "("
        #     for k,v in _config[conf_section].items():
        #         params += f"{k.replace('_', ' ')}:{v}, "
        #     params = params[:-2] + ")<br>"
        px.line(stats_df, x="i", y=col_names[1:-1]).show()


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