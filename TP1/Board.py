from collections import Set

from typing import Set


class Direction:
    def __init__(self, tile, char):
        self.tile = tile
        self.char = char

    def __str__(self):
        return self.char


class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        else:
            return False

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Tile(x, y)

    def __hash__(self):
        return hash((self.x, self.y))

    def __str__(self):
        return str(self.x) + ', ' + str(self.y)

    def double(self):
        # usado para mirar un paso más allá del actual
        return Tile(self.x * 2, self.y * 2)


L = Direction(Tile(-1, 0), 'l')
R = Direction(Tile(1, 0), 'r')
U = Direction(Tile(0, -1), 'u')
D = Direction(Tile(0, 1), 'd')
directions = [U, D, L, R]


class Board:
    def __init__(self, dir_list):
        self.dir_list = dir_list  # list of directions for solution
        self.walls: Set[Tile] = set()
        self.goals: Set[Tile] = set()
        self.boxes = set()
        self.fboxes = frozenset()  # since set() is not hashable
        self.player: Tile = None
        self.cost = 1  # used for UCS and heuristic searches

    def __eq__(self, other):
        if self.boxes.issubset(other.boxes) and self.player == other.player:
            return True
        else:
            return False

    def __hash__(self):
        return hash((self.fboxes, self.player))

    def __gt__(self, other):
        if self.cost > other.cost:
            return True
        else:
            return False

    def __lt__(self, other):
        if self.cost < other.cost:
            return True
        else:
            return False

    def add_wall(self, x, y):
        self.walls.add(Tile(x, y))

    def add_goal(self, x, y):
        self.goals.add(Tile(x, y))

    def add_box(self, x, y):
        self.boxes.add(Tile(x, y))

    def set_player(self, x, y):
        self.player = Tile(x, y)

    def moves_available(self):
        moves = []
        for d in directions:
            if self.player + d.tile not in self.walls:
                if self.player + d.tile in self.boxes:
                    if self.player + d.tile.double() not in self.boxes.union(self.walls):
                        moves.append(d)
                else:
                    moves.append(d)
        return moves

    def move(self, direction):
        p = self.player + direction.tile
        if p in self.boxes:
            self.boxes.remove(p)
            self.boxes.add(p + direction.tile)
        self.player = p
        self.dir_list.append(direction)

    def is_win(self):
        if self.goals.issubset(self.boxes):
            return True
        else:
            return False

    def get_free_goals(self):
        return self.goals.difference(self.boxes)

    def get_free_boxes(self):
        return self.boxes.difference(self.goals)

    def getDirections(self):
        chars = ''
        for d in self.dir_list:
            chars += d.char
            chars += ', '
        return chars


class Results:
    def __init__(self):
        self.algorithm = None
        self.solved = None
        self.frontier_size = None
        self.nodes_expanded = 0
        self.time_taken = -1

    def __repr__(self):
        return str({
            "algorithm": self.algorithm,
            "solved": self.solved,
            "frontier_size": self.frontier_size,
            "nodes_expanded": self.nodes_expanded,
            "time_taken": self.time_taken,
        })


def load_board(filename):
    # lista vacía de soluciones
    e = []
    b = Board(e)
    # recorremos el archivo linea por linea, caracter por caracter
    with open(filename, 'r') as f:
        read_data = f.read()
    lines = read_data.split('\n')
    x = 0
    y = 0
    for line in lines:
        for char in line:
            if char == '#':
                b.add_wall(x, y)
            elif char == '.':
                b.add_goal(x, y)
            elif char == '@':
                b.set_player(x, y)
            elif char == '$':
                b.add_box(x, y)
            elif char == '*':
                b.add_box(x, y)
                b.add_goal(x, y)
            x += 1
        y += 1
        x = 0

    # chequeos básicos
    assert len(b.goals) == len(b.boxes)
    assert b.player

    return b
