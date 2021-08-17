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

LEFT = "l"
RIGHT = "r"
UP = "u"
DOWN = "p"
L = Direction(Tile(-1, 0), LEFT)
R = Direction(Tile(1, 0), RIGHT)
U = Direction(Tile(0, -1), UP)
D = Direction(Tile(0, 1), DOWN)
directions = [U, D, L, R]


class Board:
    '''
    Board's overloaded functions and functions for
    board manipulation live here
    '''

    def __init__(self, dir_list):
        self.dir_list = dir_list  # list of directions for solution
        self.walls = set()
        self.goals = set()
        self.boxes = set()
        self.fboxes = frozenset()  # since set() is not hashable
        self.player = None
        self.cost = 1  # used for UCS and heuristic searches

    def __eq__(self, other):
        ''' checking for 'equality' of box positions and player positions '''
        if self.boxes.issubset(other.boxes) and self.player == other.player:
            return True
        else:
            return False

    def __hash__(self):
        ''' hashes by frozenset of box positions '''
        return hash((self.fboxes, self.player))

    def __gt__(self, other):
        ''' comparison by cost '''
        if self.cost > other.cost:
            return True
        else:
            return False

    def __lt__(self, other):
        ''' comparison by cost '''
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
                    # what if there's a wall or box behind it?
                    if self.player + d.tile.double() not in self.boxes.union(self.walls):
                        moves.append(d)
                else:
                    moves.append(d)
        return moves

    def move(self, direction):
        ''' moves player and box '''
        p = self.player + direction.tile
        if p in self.boxes:
            self.boxes.remove(p)
            self.boxes.add(p + direction.tile)
            self.ucsCost = 2
        self.player = p
        self.dir_list.append(direction)

    def is_win(self):
        ''' Checks for winning/final state '''
        if self.goals.issubset(self.boxes):
            return True
        else:
            return False

    def getDirections(self):
        ''' Outputs the list of directions taken for the solution '''
        chars = ''
        for d in self.dir_list:
            chars += d.char
            chars += ', '
        return chars


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
