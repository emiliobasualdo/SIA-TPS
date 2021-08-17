import configparser
from time import time

from Board import load_board, Results
from TP1.ggs import ggs
from TP1.heuristics import linear_distance
from bfs import bfs, dfs

non_informed = {
    "bfs": bfs,
    "dfs": dfs,
    # "iddfs": iddfs # ToDo <-- cambiar!
}
informed = {
    "ggs": ggs,
    # "a_start": a_start,
    # "ida": ida,
}
heuristics = {
    "linear_distance": linear_distance
}

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.cfg')
    _config=config["DEFAULT"]
    # cargamos el tablero
    board = load_board(_config["board"])

    algo = _config["algorithm"]
    results = Results()
    results.algorithm = algo
    start = time()
    if algo in non_informed:
        non_informed[algo](board, results)
    else:
        heuristic = heuristics[_config["heuristic"]]
        informed[algo](board, results, heuristic)

    end = time()
    results.time_taken = (end-start)
    print(results)

