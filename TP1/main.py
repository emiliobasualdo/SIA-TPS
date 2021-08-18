import configparser
import pprint
from time import time

from Board import load_board, Results

from heuristics import euclidean_distance, manhattan_distance, sum_of_manhattan
from non_informed import bfs, dfs, iddfs
from informed import a_star, ida, ggs

non_informed = {
    "bfs": bfs,
    "dfs": dfs,
    "iddfs": iddfs,
}
informed = {
    "ggs": ggs,
    "a_star": a_star,
    "ida": ida,
}
heuristics = {
    "euclidean_distance": euclidean_distance,
    "manhattan_distance": manhattan_distance,
    "sum_of_manhattan": sum_of_manhattan
}


def run(_config=None):
    if _config is None:
        config = configparser.ConfigParser()
        config.read('config.cfg')
        _config = config["DEFAULT"]
    # cargamos el tablero
    board = load_board(_config["board"])

    algo = _config["algorithm"]
    iterative_limit = int(_config["iterative_limit"])
    heuristic_name = _config["heuristic"]

    results = Results(algo, _config["board"])
    start = time()
    if algo in non_informed:
        non_informed[algo](board, results, iterative_limit)
    else:
        results.heuristic = heuristic_name
        informed[algo](board, results, heuristics[heuristic_name])

    end = time()
    results.time_taken = (end - start)
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(results.to_dict())

if __name__ == '__main__':
    run()