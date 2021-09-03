

def gen_quantity(condition: int, generation_number: int):
    if generation_number >= condition:
        return True
    return False

def stop_by_time(condition: float, time_passed: float):
    if time_passed >= condition:
        return True
    return False

def fitness_goal(condition: int, maxf: int):
    if maxf >= condition:
        return True
    return False

