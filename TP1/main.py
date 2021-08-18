import configparser
import pprint
from time import time

from Board import load_board, Results

from ggs import ggs
from heuristics import linear_distance
from non_informed import bfs, dfs, iddfs
from informed import a_star, ida

non_informed = {
    "bfs": bfs,
    "dfs": dfs,
}
informed = {
    "ggs": ggs,
    "a_start": a_star,
}
iteratives = {
    "idds": iddfs,
    "ida": ida,
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
    elif algo in iterative:
        iterative_limit = _config["iterative_limit"]
        results.iterative_limit = iterative_limit
        iterative[algo](board, results, iterative_limit)
    else:
        heuristic_name = _config["heuristic"]
        results.heuristic = heuristic_name
        informed[algo](board, results, heuristics[heuristic_name])

    end = time()
    results.time_taken = (end-start)
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(results.to_dict())

