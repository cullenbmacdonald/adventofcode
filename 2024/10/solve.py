import argparse, itertools, copy
from collections import defaultdict
from argparse import Namespace
from typing import List, Dict, Set, Tuple

def get_file_contents(file_path: str) -> List[List[int]]:
    with open(file_path) as file:
        return [[int(l.strip()) for l in row.strip()] for row in file]


def surrounding_indices(x: int, y: int) -> List[List[List[int]]]:
    return [
                   [x, y - 1], 
        [x - 1, y],           [x + 1, y],
                    [x, y + 1]
    ]


def in_bounds(x: int, y: int, grid: List[List[int]]) -> bool:
    if y < 0 or y >= len(grid):
        return False
    if x < 0 or x >= len(grid[0]):
        return False
    return True
    

def solve_1(file_path: str) -> int:
    grid = get_file_contents(file_path)
    trailhead_pos = [] # list of tuple of trails
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == 0:
                trailhead_pos.append(((x, y),))

    trailhead_peaks = defaultdict(set)
    positions = trailhead_pos

    while len(positions) > 0:
        trail = positions.pop()
        standing_x, standing_y = trail[-1] # get the last one off this trail
        surrounding = surrounding_indices(standing_x, standing_y)
        current_value = grid[standing_y][standing_x]
        for looking_x, looking_y in surrounding:
            if not in_bounds(looking_x, looking_y, grid):
                continue
            cell = grid[looking_y][looking_x] 
            if cell == current_value + 1:
                extended_trail = trail + ((looking_x, looking_y),)
                positions.append(extended_trail)
                if cell == 9:
                    trailhead_peaks[trail[0]].add(extended_trail[-1])
    
    return sum([len(peaks) for peaks in trailhead_peaks.values()])


def solve_2(file_path: str):
    pass


#### TEMPLATE FOR EACH DAY BEGIN NOW

def parse_args() -> Namespace:
    parser = argparse.ArgumentParser(description="Advent of Code Solver")
    parser.add_argument(
        "--test", 
        action="store_true", 
        help="Use the test input instead of the real input."
    )
    parser.add_argument(
        "--part", 
        type=int, 
        choices=[1, 2], 
        default=0, 
        help="Which part of the puzzle to run (1 or 2)."
    )
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    if args.part == 0:
        print("specify part 1 or part 2")
        exit(0)

    print(f"Running part {args.part} with {'test' if args.test else 'real'} input.")
    if args.test:
        file_path = "test.txt"
    else:
        file_path = "input.txt"

    if args.part == 1:
        result = solve_1(file_path)
    elif args.part == 2:
        result = solve_2(file_path)
    else:
        exit(0)

    print(f"Result: {result}")
