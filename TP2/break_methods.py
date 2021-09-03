
def gen_quantity(condition: int, generation_number: int):
    if generation_number >= condition:
        return True;
    return False

def time(condition: float, current_time: float):
    if current_time >= condition:
        return True;
    return False

def fitness_goal(condition: int, maxf: int):
    if maxf >= condition:
        return True;
    return False

