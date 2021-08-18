import math

from Board import Board

def sum_of_manhattan(node: Board):
    distance = 0
    free_boxes = node.get_free_boxes()
    if len(free_boxes) == 0:
        return float("-inf")
    for box in free_boxes:
        min_distance = 0
        for goal in node.get_free_goals():
            aux = math.fabs(goal.x - box.x) + math.fabs(goal.y - box.y)
            if min_distance > aux:
                min_distance = aux
        distance += min_distance
    return distance

def manhattan_distance(node: Board):
    min_distance = float("inf")
    free_boxes = node.get_free_boxes()
    if len(free_boxes) == 0:
        return float("-inf")
    for box in free_boxes:
        for goal in node.get_free_goals():
            aux = math.fabs(goal.x - box.x) + math.fabs(goal.y - box.y)
            if min_distance > aux:
                min_distance = aux
    return min_distance

def euclidean_distance(node: Board):
    min_distance = float("inf")
    free_boxes = node.get_free_boxes()
    if len(free_boxes) == 0:
        return float("-inf")
    for box in free_boxes:
        for goal in node.get_free_goals():
            aux = (goal.x - box.x) ** 2 + (goal.y - box.y) ** 2
            if min_distance > aux:
                min_distance = aux
    return min_distance
