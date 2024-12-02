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

def check_level(prev_direction: int, level: int, prev_level: int) -> bool:
    curr_direction = get_direction(prev_level, level)
    distance = abs(prev_level - level)
    if distance <= 0 or distance > 3:
        return False
    if prev_direction != curr_direction:
        return False

    return True

def check_report(report: List[int]) -> bool:
    direction = None
    for idx, level in enumerate(report):
        if idx == 0:
            continue

        prev_level = report[idx - 1]
        if direction == None:
            direction = get_direction(prev_level, level)

        if not check_level(direction, level, prev_level):
            return False

    return True

def dampened_report(report: List[int]) -> bool:
    cursor = 0
    bad_count = 0 
    while cursor < len(report):
        new_report = [l for i, l in enumerate(report) if i != cursor]
        print(report, new_report)
        safe = check_report(new_report)
        if not safe:
            cursor += 1
        else:
            return True


def get_inc(dampen_problems=False):
    def increment_safe(safe_count: int, line: str) -> int:
        report = [int(l) for l in line.split(" ")]
        safe = check_report(report)
        if safe:
            return safe_count + 1
        if dampen_problems:
            if dampened_report(report):
                return safe_count + 1
        return safe_count

    return increment_safe


def execute() -> List[List[int]]:
    left = []
    with open("input.txt") as file:
        safe_count = functools.reduce(get_inc(), file, 0)
        file.seek(0)
        dampened_safe_count = functools.reduce(get_inc(dampen_problems=True), file, 0)
    
    return (safe_count, dampened_safe_count)

if __name__ == "__main__":
    solution_01, solution_02 = execute()
    print(solution_01)
    print(solution_02)
