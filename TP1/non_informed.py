from copy import deepcopy

nodes = 0

def bfs(board, results):
    nodes_expanded = 0
    frontier = [board]
    explored = set()
    keepLooking = True
    initial_pos = board.player
    while keepLooking:
        currNode = frontier.pop(0)
        if currNode.is_win():
            results.solved = True
            results.steps = currNode.dir_list
            results.initial_pos = initial_pos
            results.end_pos = currNode.player
            results.nodes_expanded = nodes_expanded
            results.frontier_size = len(frontier)
            return
        moves = currNode.moves_available()
        currNode.fboxes = frozenset(currNode.boxes)
        explored.add(currNode)
        if moves:
            nodes_expanded += 1
        for m in moves:
            child = deepcopy(currNode)
            child.move(m)
            if child not in explored:
                frontier.append(child)


def dfs(board, results):
    nodes_expanded = 0
    frontier = [board]
    explored = set()
    keepLooking = True
    initial_pos = board.player
    while keepLooking:
        currNode = frontier.pop()
        if currNode.is_win():
            results.solved = True
            results.steps = currNode.dir_list
            results.initial_pos = initial_pos
            results.end_pos = currNode.player
            results.nodes_expanded = nodes_expanded
            results.frontier_size = len(frontier)
            return
        moves = currNode.moves_available()
        currNode.fboxes = frozenset(currNode.boxes)
        explored.add(currNode)
        if moves:
            nodes_expanded += 1
        for m in moves:
            child = deepcopy(currNode)
            child.move(m)
            if child not in explored:
                frontier.append(child)


def iddfs(board, results, LIMIT_INCREASE):
    frontier = [board]
    explored = set()
    limit = 0
    start = 0
    nodes_expanded = []
    last_level_nodes = []
    results.initial_pos = board.player
    while True:
        while frontier:
            result = iddfs_rec(start, limit, frontier, results, nodes_expanded, last_level_nodes, explored)
            if result is not None:
                return result
        start = limit
        limit += LIMIT_INCREASE
        frontier = last_level_nodes.copy()
        last_level_nodes = []
        if results.solved:
            return


def iddfs_rec(start, limit, frontier, results, nodes_expanded, last_level_nodes, explored):
    if not frontier:
        return None
    currNode = frontier.pop()

    if start == limit:
        last_level_nodes.insert(0, currNode)
        return None

    if currNode.is_win():
        results.solved = True
        results.steps = currNode.dir_list
        results.end_pos = currNode.player
        results.nodes_expanded = len(nodes_expanded)
        results.frontier_size = len(frontier)
        return currNode

    nodes_expanded.append(1)
    moves = currNode.moves_available()
    currNode.fboxes = frozenset(currNode.boxes)
    explored.add(currNode)

    for m in moves:
        child = deepcopy(currNode)
        child.move(m)
        if child not in explored:
            result = iddfs_rec(start+1, limit, frontier, results, nodes_expanded, last_level_nodes, explored)
            frontier.append(child)
            if result is not None:
                return result
    return None

