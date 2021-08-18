from time import time
from copy import deepcopy
from heapq import heappop, heappush
import bisect
import math


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


def ida(board, results, heuristic):
    nodes_expanded = 0
    keepLooking = True
    initial_pos = board.player
    bound = heuristic(board)
    while keepLooking:
        explored = set()
        frontier = [(0,board)]
        min_f = math.inf
        while frontier:
            _, currNode = heappop(frontier)
            explored.add(currNode)
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
            if moves:
                nodes_expanded += 1
                for m in moves:
                    child = deepcopy(currNode)
                    child.move(m)
                    if child not in explored:
                        f = heuristic(child) + len(child.dir_list)
                        if f > bound:
                            if f < min_f:
                                min_f = f
                            continue
                        heappush(frontier, (f, child))
        bound = min_f





def a_star(board, results, heuristic):
    nodes_expanded = 0
    frontier = [(0, board)]
    explored = set()
    keepLooking = True
    initial_pos = board.player
    while keepLooking:
        heuristic(frontier[0][1])
        currNode = heappop(frontier)[1]
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
                    f = heuristic(child) + len(child.dir_list)  # f(nj) = h(nj) + c(ni, nj)
                    heappush(frontier, (f, child))

#
# def a_star1(board, results, heuristic):
#     nodes_expanded = 0
#     frontier = [board]
#     explored = set()
#     initial_pos = board.player
#     while frontier:
#         currNode = frontier.pop(0)
#         if currNode.is_win():
#             results.solved = True
#             results.steps = currNode.dir_list
#             results.initial_pos = initial_pos
#             results.end_pos = currNode.player
#             results.nodes_expanded = nodes_expanded
#             results.frontier_size = len(frontier)
#             return
#         moves = currNode.moves_available()
#         currNode.fboxes = frozenset(currNode.boxes)
#         explored.add(currNode)
#         if moves:
#             nodes_expanded += 1
#             print(len(moves))
#             for m in moves:
#                 child = deepcopy(currNode)
#                 child.move(m)
#                 if child not in explored:
#                     h = heuristic(child)
#                     bisect.insort(frontier, child)
