import functools
import operator
from typing import Tuple, List

def __add_to_arr(arr, part):
    arr.append(int(part.strip()))

# Expects to receive an already sorted list. I'm not gonna try to do a once through thing here just yet
def execute(left: List[int], right: List[int]) -> int:
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
    from pdb import set_trace; set_trace()
    solution = execute(*file_input)
    print(solution)
