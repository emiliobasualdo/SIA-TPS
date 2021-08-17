from time import time
from copy import deepcopy
from heapq import heappop, heappush


def ggs(board, results, heuristic):
    nodes_expanded = 0
    frontier = [(0, board)]
    explored = set()
    keepLooking = True
    while keepLooking:
        currNode = heappop(frontier)[1]
        if currNode.is_win():
            results.solved = True
            results.nodes_expanded = nodes_expanded
            results.frontier_size = len(frontier)
            return
        moves = currNode.moves_available()
        currNode.fboxes = frozenset(currNode.boxes)
        explored.add(currNode)
        if moves:
            nodes_expanded += 1
            print(len(moves))
            for m in moves:
                child = deepcopy(currNode)
                child.move(m)
                if child not in explored:
                    h = heuristic(child)
                    heappush(frontier, (h, child))
