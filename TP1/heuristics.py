import math

from Board import Board


def linear_distance(node: Board):
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
