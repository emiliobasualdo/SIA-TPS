import configparser
import json
import os
import random
import pandas as pd
import plotly.express as px

import asyncio
import websockets

pd.options.plotting.backend = "plotly"
from Player import items, set_item, rand_player, Player
from cross_over_methods import one_point
from mutation_methods import single_gen
from selection_methods import random_selection, elite_selection

_config = configparser.ConfigParser()

MAX_ROWS = 100  # todo <--- borrar cuando terminamos
MAX_ITERATIONS = 100  # todo <--- borrar cuando terminamos

selection_methods = {
    "random": random_selection,
    "elite": elite_selection,
}
cross_over_methods = {
    "one_point": one_point,
}
mutation_methods = {
    "single_gen": single_gen,
}
def calculate_stats(players: [Player]):
    min_fitness = 0
    avg_fitness = 0

    for player in players:
        avg_fitness += player.fitness
        if min_fitness < player.fitness:
            min_fitness = player.fitness
    if len(players):
        avg_fitness /= len(players)
    return min_fitness, avg_fitness

async def main(websocket, path):
    # cargamos las configuraciones
    print("Cargando configuración")
    config = _config["DEFAULT"]
    if config["seed"] != "None":
        random.seed(int(config["seed"]))

    # cargamos los items
    print("Cargando items")
    items_dir = config["items_directory"]
    for key in items.keys():
        set_item(key,
                 pd.read_csv(os.path.join(items_dir, f'{key}.tsv'), index_col="id", sep="\t", header=0, nrows=MAX_ROWS))

    # creamos los players random
    N = int(config["N"])
    min_h = float(config["min_h"])
    max_h = float(config["max_h"])
    print(f"Creando players N={N} player")
    players = []
    for i in range(N):
        players.append(rand_player(min_h, max_h))

    # generamos las funciones según config
    sel_config = _config["SELECTION"]
    selection_method = selection_methods[sel_config["method"]]
    delta_k = int(sel_config["delta_k"])
    selection = lambda pls: selection_method(pls, len(pls) + delta_k)

    co_config = _config["CROSS_OVER"]
    cross_over_method = cross_over_methods[co_config["method"]]
    point = int(co_config["point"])
    assert 0 <= point <= 6
    cross_over = lambda pls: cross_over_method(pls, point)

    mu_config = _config["MUTATION"]
    mutation = mutation_methods[mu_config["method"]]

    new_sel_config = _config["NEW_GEN_SELECTION"]
    new_generation_selection_method = selection_methods[new_sel_config["method"]]
    new_delta_k = int(new_sel_config["delta_k"])
    new_generation_selection = lambda pls: new_generation_selection_method(pls, len(pls) + new_delta_k)

    data = []
    # iteramos
    print("Iterando por el conjunto")
    for i in range(MAX_ITERATIONS):
        if i % 5 == 0:
            min_f, avg_f = calculate_stats(players)
            data.append((i, min_f, avg_f))
            await websocket.send(json.dumps(data))
        cross_over(selection(players))
        mutation(players)
        players = new_generation_selection(players)

    res_df = pd.DataFrame().from_records(players,
                                columns=["armas", "botas", "cascos", "guantes", "pecheras", "height", "character", "fitness"])
    print("Listo")
    if config["graphs"] == "true":
        fig = px.box(res_df[["character", "fitness"]], x="character", y="fitness")
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