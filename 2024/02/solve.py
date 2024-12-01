import functools, operator
from collections import defaultdict
from typing import Tuple, List, Dict

def __add_to_arr(arr, part):
    arr.append(int(part.strip()))

def __process_right_list(right: List[int]) -> Dict[int, int]:
    counts = defaultdict(int)
    for location_id in right:
        counts[location_id] = counts[location_id] + 1
    return counts

# Doesnt need to be sorted for this one
def execute(left: List[int], right: List[int]) -> int:
    right_counts = __process_right_list(right)
    similarity = [l * right_counts[l] for l in left]
    return functools.reduce(operator.add, similarity)

def process_file_input() -> Tuple[List[int], List[int]]:
    left = []
    right = []
    with open("input.txt") as file:
        for line in file:
            split_up = line.split("   ")
            __add_to_arr(left, split_up[0])
            __add_to_arr(right, split_up[1])

    return (left, right)

if __name__ == "__main__":
    file_input = process_file_input()
    solution = execute(*file_input)
    print(solution)
