import configparser
from time import time

from Board import load_board, Results
from bfs import bfs, dfs, iddfs

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.cfg')
    _config=config["DEFAULT"]
    # cargamos el tablero
    board = load_board(_config["board"])

    algo = _config["algorithm"]
    results = Results()
    start = time()
    if algo == "bfs":
        results.algorithm = 'bfs'
        bfs(board, results)
    elif algo == "dfs":
        results.algorithm = 'dfs'
        dfs(board, results)
    elif algo == "iddfs":
        results.algorithm = 'iddfs'
        iddfs(board, results)

    end = time()
    results.time_taken = (end-start)
    print(results)

