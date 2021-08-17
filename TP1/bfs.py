from time import time
from copy import deepcopy

def bfs(board, results):
    nodes_expanded = 1
    frontier = [board]
    explored = set()
    keepLooking = True
    while keepLooking:
        currNode = frontier.pop(0)
        if currNode.is_win():
            results.solved = True
            results.nodes_expanded = nodes_expanded
            results.frontier_size = len(frontier)
            return
        moves = currNode.moves_available()
        currNode.fboxes = frozenset(currNode.boxes)
        explored.add(currNode)
        for m in moves:
            child = deepcopy(currNode)
            nodes_expanded += 1
            child.move(m)
            if child not in explored:
                frontier.append(child)
