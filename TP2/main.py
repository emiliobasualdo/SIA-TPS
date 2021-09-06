import configparser
import json
import math
import os
import random
from datetime import datetime

import numpy as np
import pandas as pd
import plotly.express as px
import time

import asyncio
import websockets
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from Player import items, set_item, Player, characters, item_indexes
from cross_over_methods import one_point, two_points, anular, uniform
from mutation_methods import single_gen, multi_gen_lim, multi_gen_uni, complete_mutation
from selection_methods import random_sel, elite, roulette, universal, ranking, det_tourn, prob_tourn, boltzmann
from break_methods import gen_quantity, fitness_goal, stop_by_time

_config = configparser.ConfigParser()
pd.options.plotting.backend = "plotly"


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


def _cross_over_method(config, mutation_method):
    cross_over_method = config["method"]
    if cross_over_method == "one_point":
        cross_over = lambda pls: one_point(pls, mutation_method)
    elif cross_over_method == "two_points":
        cross_over = lambda pls: two_points(pls, mutation_method)
    elif cross_over_method == "anular":
        cross_over = lambda pls: anular(pls, mutation_method)
    elif cross_over_method == "uniform":
        Pc = float(config["Pc"])
        cross_over = lambda pls: uniform(pls, Pc, mutation_method)
    else:
        raise AttributeError(f"No such CrossOver method {cross_over_method}")
    return cross_over


def _selection_method(config, N: int, k: int):
    def get_method(method_name, config, _k):
        if method_name == "random":
            sel_method = lambda pls, i: random_sel(pls, _k)
        elif method_name == "elite":
            sel_method = lambda pls, i: elite(pls, _k)
        elif method_name == "roulette":
            sel_method = lambda pls, i: roulette(pls, _k)
        elif method_name == "universal":
            sel_method = lambda pls, i: universal(pls, _k)
        elif method_name == "ranking":
            sel_method = lambda pls, i: ranking(pls, _k)
        elif method_name == "det_tourn":
            M = int(config["M"])
            sel_method = lambda pls, i: det_tourn(pls, _k, M)
        elif method_name == "prob_tourn":
            th = float(config["th"])
            sel_method = lambda pls, i: prob_tourn(pls, _k, th)
        elif method_name == "boltzmann":
            t0 = float(config["t0"])
            tc = float(config["tc"])
            sel_method = lambda pls, i: boltzmann(pls, _k, i, t0, tc)
        else:
            raise AttributeError(f"No such selection method {method_name}")
        return sel_method

    m1 = config["method1"]
    m2 = config["method2"]
    A = float(config["A"])
    if "fill" not in config:
        method1 = get_method(m1, config, math.floor(k * A))
        method2 = get_method(m2, config, math.ceil(k * (1 - A)))
        return lambda pls, i: method1(pls, i) + method2(pls, i)

    fill = config["fill"]
    if fill == "all":
        method1 = get_method(m1, config, math.floor(N * A))
        method2 = get_method(m2, config, math.ceil(N * (1 - A)))
        selection_method = lambda k_parents, k_kids, i: method1(k_parents + k_kids, i) + method2(k_parents + k_kids, i)
    else:
        if k >= N:
            method1 = get_method(m1, config, math.floor(N * A))
            method2 = get_method(m2, config, math.ceil(N * (1 - A)))
            selection_method = lambda k_parents, k_kids, i: method1(k_kids, i) + method2(k_kids, i)
        else:
            method1 = get_method(m1, config, math.floor((N - k) * A))
            method2 = get_method(m2, config, math.ceil((N - k) * (1 - A)))
            selection_method = lambda k_parents, k_kids, i: k_kids + method1(k_parents, i) + method2(k_parents, i)
    return selection_method


def calculate_stats(generation: [Player]):
    min_fitness = float("inf")
    max_fitness = 0
    avg_fitness = 0

    min_height = float("inf")
    max_height = 0
    avg_height = 0

    diversity = [set() for _ in range(Player.ATTR_LEN)]

    for player in generation:
        avg_fitness += player.fitness
        if min_fitness > player.fitness:
            min_fitness = player.fitness
        if max_fitness < player.fitness:
            max_fitness = player.fitness

        avg_height += player.attrs[Player.HEIGHT]
        if min_height > player.attrs[Player.HEIGHT]:
            min_height = player.attrs[Player.HEIGHT]
        if max_height < player.attrs[Player.HEIGHT]:
            max_height = player.attrs[Player.HEIGHT]

        for i in range(Player.ATTR_LEN):
            diversity[i].add(player.attrs[i])

    avg_fitness /= len(generation)
    avg_height /= len(generation)

    diversity = list(map(lambda s: len(s), diversity))
    return min_fitness, avg_fitness, max_fitness, min_height, avg_height, max_height, diversity


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
    mutation = _mu_method(_config["MUTATION"])
    cross_over = _cross_over_method(_config["CROSS_OVER"], mutation)
    new_generation_selection = _selection_method(_config["NEW_GEN_SELECTION"], N, k)

    # iteramos
    stop_config = _config["STOP_CONDITION"]
    stop_condition_method = stop_config["stop_condition"]
    if stop_condition_method == "gen_quantity":
        condition = int(stop_config["gen_quantity"])
        stop_condition = lambda maxf, gene, timer: gen_quantity(condition, gene)
    elif stop_condition_method == "time":
        condition = float(stop_config["time"])
        stop_condition = lambda maxf, gene, timer: stop_by_time(condition, timer)
    elif stop_condition_method == "fitness_goal":
        condition = float(stop_config["fitness_goal"])
        stop_condition = lambda maxf, gene, timer: fitness_goal(condition, maxf)
    else:
        raise AttributeError(f"No such Stop Condition method {stop_condition_method}")

    print(f"Iterando")
    historical_f_stats = []
    historical_h_stats = []
    historical_d_stats = []
    start_timer = datetime.now()
    max_f = 0
    i = 0
    while not stop_condition(max_f, i, (datetime.now() - start_timer).seconds):
        if i % 5 == 0:
            min_f, avg_f, max_f, min_h, avg_h, max_h, diversity = calculate_stats(generation)
            f_stats = (i, min_f, avg_f, max_f)
            historical_f_stats.append(f_stats)
            h_stats = (i, min_h, avg_h, max_h)
            historical_h_stats.append(h_stats)
            d_stats = (i, *diversity)
            historical_d_stats.append(d_stats)
            await websocket.send(json.dumps((f_stats, h_stats, d_stats)))
        i += 1
        k_parents = selection(generation, i)
        k_kids = cross_over(k_parents)
        generation = new_generation_selection(k_parents, k_kids, i)

    time_taken = (datetime.now() - start_timer).seconds
    if config["graphs"] == "true":

        f_col_names = ["i", "min_f", "avg_f", "max_f"]
        h_col_names = ["i", "min_h", "avg_h", "max_h"]
        d_col_names = ["i"] + item_indexes + ["height"]
        f_stats_df = pd.DataFrame(historical_f_stats, columns=f_col_names)
        h_stats_df = pd.DataFrame(historical_h_stats, columns=h_col_names)
        d_stats_df = pd.DataFrame(historical_d_stats, columns=d_col_names)
        res_df = pd.DataFrame().from_records(generation,
                                             columns=["armas", "botas", "cascos", "guantes", "pecheras", "height",
                                                      "fitness"])

        top = res_df[["height", "fitness"]].groupby(by=["height", "fitness"]).size()
        top = top.reset_index(name='count')
        print(top, top.sum())
        fig = make_subplots(rows=3, cols=2,
                            specs=[[{}, {"rowspan": 2}],
                                   [{}, None],
                                   [{}, None]],
                            shared_xaxes=True, vertical_spacing=0.02, horizontal_spacing=0.1)

        for col in f_col_names[1:]:
            fig.append_trace(go.Scatter(legendgroup='1', name=col, x=f_stats_df["i"], y=f_stats_df[col]), 1, 1)
        for col in h_col_names[1:]:
            fig.append_trace(go.Scatter(legendgroup='2', name=col, x=h_stats_df["i"], y=h_stats_df[col]), 2, 1)
        for col in d_col_names[1:]:
            fig.append_trace(go.Scatter(legendgroup='3', name=col, x=d_stats_df["i"], y=d_stats_df[col]), 3, 1)

        fig.add_trace(
            go.Scatter(name="FxH", x=top["height"], y=top["fitness"], mode='markers', marker=dict(size=np.log(top["count"]))),
            row=1, col=2)

        # axis names
        fig.update_yaxes(title_text="Fitness", row=1, col=1)
        fig.update_yaxes(title_text="Height", row=2, col=1)
        fig.update_yaxes(title_text="Alelos por locus", row=3, col=1)
        fig.update_xaxes(title_text="Generation", row=3, col=1)

        fig.update_yaxes(title_text="Fitness", row=1, col=2)
        fig.update_xaxes(title_text="Height", row=1, col=2)

        # title
        params = f"Fitness, Height & Generation Count. Time taken={round(time_taken / 60, 2)}min <br>"
        params += f"Character: {char_class}, N: {N}, k: {k}, stop condition: {stop_condition_method} <br>"
        params += "<span style='font-size: 10px;'>"
        for conf_section in ["SELECTION", "CROSS_OVER", "MUTATION", "NEW_GEN_SELECTION"]:
            for k, v in _config[conf_section].items():
                if k not in _config["DEFAULT"].keys():
                    params += f"{k.replace('_', ' ').title()}: {v.replace('_', ' ').title()}, "
            params = params[:-2] + " | "
        params += "</span>"
        fig.update_layout(
            title_text=params,
            showlegend=False,
            # hovermode='x unified'
        )
        fig.show()


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
