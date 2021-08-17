import configparser
from time import time

from Board import load_board, Results
from TP1.ggs import ggs
from TP1.heuristics import linear_distance
from bfs import bfs, dfs

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.cfg')
    _config=config["DEFAULT"]
    # cargamos el tablero
    board = load_board(_config["board"])

    non_informed = {
        "bfs": bfs,
        "dfs": dfs,
        "bfs": bfs
    }
    informed = {
        "ggs": ggs
    }
    heuristics = {
        "linear_distance": linear_distance
    }
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

