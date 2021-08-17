from time import time
from copy import deepcopy

def bfs(board,results):
    nodes_expanded = 0
    frontier = [board]
    explored = set()
    keepLooking = True
    while keepLooking:
        nodes_expanded += 1
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
            child.move(m)
            if child not in explored:
                frontier.append(child)

def dfs(board,results):
    nodes_expanded = 0
    frontier = [board]
    explored = set()
    keepLooking = True
    while keepLooking:
        nodes_expanded += 1
        currNode = frontier.pop()
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
            child.move(m)
            if child not in explored:
                frontier.append(child)
