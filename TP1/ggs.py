from copy import deepcopy
from heapq import heappop, heappush


def ggs(board, results, heuristic):
    nodes_expanded = 0
    frontier = [(0, board)]
    explored = set()
    keepLooking = True
    initial_pos = board.player
    while keepLooking:
        _, currNode = heappop(frontier)
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
                    h = heuristic(child)
                    heappush(frontier, (h, child))

