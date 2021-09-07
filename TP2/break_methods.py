

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

def content(condition: int, gen_count: int):
	if gen_count >= condition:
		return True
	return False

def structure(condition: int, div_count: int):
	if div_count >= condition:
		return True
	return False
