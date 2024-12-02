import functools, operator
from typing import Tuple, List, Dict
from collections import defaultdict

def __add_to_arr(arr, part):
    arr.append(int(part.strip()))
def __add_to_arr(arr, part):
    arr.append(int(part.strip()))

def __process_right_list(right: List[int]) -> Dict[int, int]:
    counts = defaultdict(int)
    for location_id in right:
        counts[location_id] = counts[location_id] + 1
    return counts

# Doesnt need to be sorted for this one
def solve_02(left: List[int], right: List[int]) -> int:
    right_counts = __process_right_list(right)
    similarity = [l * right_counts[l] for l in left]
    return functools.reduce(operator.add, similarity)

# Expects to receive an already sorted list. I'm not gonna try to do a once through thing here just yet
def solve_01(left: List[int], right: List[int]) -> int:
    distances = [abs(l[0] - l[1]) for l in zip(left, right)]
    return functools.reduce(operator.add, distances)

def process_file_input() -> Tuple[List[int], List[int]]:
    left = []
    right = []
    with open("input.txt") as file:
        for line in file:
            split_up = line.split("   ")
            __add_to_arr(left, split_up[0])
            __add_to_arr(right, split_up[1])

    return (sorted(left), sorted(right))

if __name__ == "__main__":
    file_input = process_file_input()
    print(solve_01(*file_input))
    print(solve_02(*file_input))
