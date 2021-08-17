from time import time
from copy import deepcopy
from heapq import heappop, heappush
import bisect


def a_star(board, results, heuristic):
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


def a_star1(board, results, heuristic):
    nodes_expanded = 0
    frontier = [board]
    explored = set()
    keepLooking = True
    while keepLooking:
        currNode = frontier(0)
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
                    bisect.insort(frontier, child)