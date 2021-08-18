import configparser
import pprint
from time import time

import pandas as pd

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
    return results


def run_many_time():
    bfs_count = 0
    dfs_count = 0
    iddfs_count = 0
    ggs_count = 0
    a_star_count = 0
    ida_count = 0
    _range = 10
    for i in range(_range):
        bfs_resp = run(dict(
            board="maps/easy2.txt",
            algorithm="bfs",
            heuristic="_",
            iterative_limit=-1

        ))
        bfs_count += bfs_resp.time_taken
        dfs_resp = run(dict(
            board="maps/easy2.txt",
            algorithm="dfs",
            heuristic="_",
            iterative_limit=-1
        ))
        dfs_count += dfs_resp.time_taken
        iddfs_resp = run(dict(
            board="maps/easy2.txt",
            algorithm="iddfs",
            heuristic="_",
            iterative_limit=10
        ))
        iddfs_count += iddfs_resp.time_taken
        for euris_name in heuristics.keys():
            ggs_resp = run(dict(
                board="maps/easy2.txt",
                algorithm="ggs",
                heuristic=euris_name,
                iterative_limit=-1
            ))
            ggs_count += ggs_resp.time_taken
            a_star_resp = run(dict(
                board="maps/easy2.txt",
                algorithm="a_star",
                heuristic=euris_name,
                iterative_limit=-1
            ))
            a_star_count += a_star_resp.time_taken
            ida_resp = run(dict(
                board="maps/easy2.txt",
                algorithm="ida",
                heuristic=euris_name,
                iterative_limit=-1
            ))
            ida_count += ida_resp.time_taken

    print(bfs_count / _range)
    print(dfs_count / _range)
    print(iddfs_count / _range)
    print(ggs_count / (len(heuristics) * _range))
    print(a_star_count / (len(heuristics) * _range))
    print(ida_count / (len(heuristics) * _range))


if __name__ == '__main__':
    run()
