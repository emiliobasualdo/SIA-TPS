import configparser

from TP1.Board import load_board
from TP1.dfs import dfs

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.cfg')
    _config=config["DEFAULT"]
    # cargamos el tablero
    board = load_board(_config["board"])

    algo = _config["algorithm"]
    if algo == "dfs":
        results = dfs(board)

    print(board)