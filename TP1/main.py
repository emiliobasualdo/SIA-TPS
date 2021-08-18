import configparser
import pprint
import sys
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
    return results


def run_many_time():
    counters = {**{f"ggs-{euris_name}": 0 for euris_name in heuristics.keys()},
                **{f"a_star-{euris_name}": 0 for euris_name in heuristics.keys()},
                **{f"ida-{euris_name}": 0 for euris_name in heuristics.keys()},
                "bfs": 0, "dfs": 0, "iddfs": 0}
    _range = 10
    board = "maps/easy2.txt"
    resp = {}
    for i in range(_range):
        bfs_resp = run(dict(
            board=board,
            algorithm="bfs",
            heuristic="_",
            iterative_limit=-1
        ))
        resp["bfs"] = bfs_resp.to_dict()
        counters["bfs"] += bfs_resp.time_taken
        dfs_resp = run(dict(
            board=board,
            algorithm="dfs",
            heuristic="_",
            iterative_limit=-1
        ))
        resp["dfs"] = dfs_resp.to_dict()
        counters["dfs"] += dfs_resp.time_taken
        iddfs_resp = run(dict(
            board=board,
            algorithm="iddfs",
            heuristic="_",
            iterative_limit=10
        ))
        resp["iddfs"] = iddfs_resp.to_dict()
        counters["iddfs"] += iddfs_resp.time_taken
        for euris_name in heuristics.keys():
            ggs_resp = run(dict(
                board=board,
                algorithm="ggs",
                heuristic=euris_name,
                iterative_limit=-1
            ))
            name = f"ggs-{euris_name}"
            resp[name] = ggs_resp.to_dict()
            counters[name] += ggs_resp.time_taken
            a_star_resp = run(dict(
                board=board,
                algorithm="a_star",
                heuristic=euris_name,
                iterative_limit=-1
            ))
            name = f"a_star-{euris_name}"
            resp[name] = a_star_resp.to_dict()
            counters[name] += a_star_resp.time_taken
            ida_resp = run(dict(
                board=board,
                algorithm="ida",
                heuristic=euris_name,
                iterative_limit=-1
            ))
            name = f"ida-{euris_name}"
            resp[name] = ida_resp.to_dict()
            counters[name] += ida_resp.time_taken


    df = pd.DataFrame.from_dict(resp, orient="index")
    filename = "results.csv"
    df[["solved", "frontier_size", "nodes_expanded", "depth", "initial_pos","end_pos"]].to_csv(filename)
    print("Results saved to:", filename)
    time_df = pd.Series(counters) / _range
    print(f"mean seconds taken on {_range} runs:")
    print(time_df)

if __name__ == '__main__':
    if sys.argv[1] == "many":
        run_many_time()
    else:
        results = run()
        pp = pprint.PrettyPrinter(indent=2)
        pp.pprint(results.to_dict())
