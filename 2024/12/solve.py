from __future__ import annotations
import argparse, itertools, copy
from collections import defaultdict
from argparse import Namespace
from typing import List, Dict, Set, Tuple, Type

def get_file_contents(file_path: str) -> List[List[str]]:
    with open(file_path) as file:
        return [[l.strip() for l in row.strip()] for row in file]


# returns up, down, left, right
# left doesnt really matter...i dont think. 
def surrounding_indices(x: int, y: int) -> List[Tuple[int]]:
    return [
        (x, y - 1), 
        (x, y + 1),
        (x - 1, y),
        (x + 1, y)
    ]


def in_bounds(index: Tuple[int], grid: List[List[int]]) -> bool:
    x, y = index
    if y < 0 or y >= len(grid):
        return False
    if x < 0 or x >= len(grid[0]):
        return False
    return True


def get_next_cells(x: int, y: int, grid: List[List[int]]) -> List[Tuple[int, int]]:
    indices = surrounding_indices(x, y)
    return [i for i in indices if in_bounds(i, grid)]


def contiguous_areas(grid: List[List[str]]) -> List[List[Tuple[int, int]]]:
    seen: Set[Tuple[int, int]] = set()
    # Last index is (area, perimeter)
    plots: List[List[Tuple[int, int]]] = []

    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if (x, y) in seen:
                continue
            plot = [(x ,y)]
            area = 1
            perimeter = 4
            seen.add((x, y))
            next_options = get_next_cells(x, y, grid)
            while next_options:
                looking = next_options.pop()
                this_perimeter = 4
                value = grid[looking[1]][looking[0]]
                if value == cell:
                    perimeter -= 1
                    if looking in seen:
                        continue 
                    area += 1
                    perimeter += 4
                    plot.append(looking)
                    seen.add(looking)
                    next_options += get_next_cells(looking[0], looking[1], grid)
            plot.append((area, perimeter))
            plots.append(plot)
    return plots 


def solve(file_path: str) -> Tuple[int, int]:
    grid = get_file_contents(file_path)

    plots = contiguous_areas(grid)
    prices = []
    for plot in plots:
        area, perimeter = plot[-1]
        prices.append(area * perimeter)
    return sum(prices)
            
 

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
        result = solve(file_path)
    elif args.part == 2:
        result = solve(file_path)
    else:
        exit(0)

    print(f"Result: {result}")
