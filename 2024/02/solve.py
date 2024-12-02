import functools
from typing import List

INCREASING = 1
DECREASING = -1
UNKNOWN = 0 

class WTFError(Exception):
    pass

def get_direction(first: int, second: int) -> int:
    if first < second:
        return INCREASING
    elif first > second:
        return DECREASING
    elif first == second:
        return UNKNOWN
    else:
        raise WTFError()

def increment_safe(safe_count: int, line: str) -> int:
    report = [int(l) for l in line.split(" ")]
    prev_direction = None
    for idx, num in enumerate(report):
        if idx == 0:
            continue

        prev_num = report[idx - 1]
        curr_direction = get_direction(prev_num, num)
        if prev_direction == None:
            prev_direction = curr_direction

        distance = abs(prev_num - num)

        if distance <= 0 or distance > 3:
            return safe_count

        if prev_direction != curr_direction:
            return safe_count

    return safe_count + 1


def execute() -> List[List[int]]:
    left = []
    with open("input.txt") as file:
        safe_count = functools.reduce(increment_safe, file, 0)

    return (safe_count, None)

if __name__ == "__main__":
    solution_01, solution_02 = execute()
    print(solution_01)
    #print(solution_02)
