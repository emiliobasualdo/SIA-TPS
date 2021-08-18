import configparser
import pprint
from time import time

from Board import load_board, Results

from heuristics import euclidean_distance
from non_informed import bfs, dfs, iddfs
from informed import a_star, ida, ggs

non_informed = {
    "bfs": bfs,
    "dfs": dfs,
}
informed = {
    "ggs": ggs,
    "a_star": a_star,
}
iterative = {
    "idds": iddfs,
    "ida": ida,
}
heuristics = {
    "euclidean_distance": euclidean_distance
}


def run(_config=None):
    if _config is None:
        config = configparser.ConfigParser()
        config.read('config.cfg')
        _config = config["DEFAULT"]
    # cargamos el tablero
    board = load_board(_config["board"])

    algo = _config["algorithm"]
    results = Results(algo, _config["board"])
    start = time()

    if algo in non_informed:
        non_informed[algo](board, results)
    elif algo in iterative:
        iterative_limit = _config["iterative_limit"]
        results.iterative_limit = iterative_limit
        iterative[algo](board, results, iterative_limit)
    else:
        heuristic_name = _config["heuristic"]
        results.heuristic = heuristic_name
        informed[algo](board, results, heuristics[heuristic_name])

    end = time()
    results.time_taken = (end - start)
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(results.to_dict())

if __name__ == '__main__':
    run()