import argparse, itertools
from argparse import Namespace
from typing import List, Dict, Set, Tuple

U = "up"
UR = "up-right"
R = "right"
DR = "down-right"
D = "down"
DL = "down-left"
L = "left"
UL = "up-left"

def get_file_contents(file_path: str) -> List[List[str]]:
    with open(file_path) as file:
        return [[l.strip() for l in row.strip()] for row in file]


def get_next_index(x: int, y: int, dir: str, distance: int) -> Tuple[int]:
    dirs = {
        U: (x, y - distance),
        UR: (x + distance, y - distance),
        R: (x + distance, y),
        DR: (x + distance, y + distance),
        D: (x, y + distance),
        DL: (x - distance, y + distance),
        L: (x - distance, y),
        UL: (x - distance, y - distance)
    }

    return dirs[dir]


def solve_part_2(file_path: str):
    pass


def solve_part_1(file_path: str):
    grid = get_file_contents(file_path)
    ants = set([(value, (x, y)) for y, row in enumerate(grid) for x, value in enumerate(row) if value != "."])
    found_nodes = set() # (dimension, ant1, ant2) order doesnt matter. can be more than one node at a location
    max_x = len(grid[0])
    max_y = len(grid)

    def in_bounds(x, y) -> bool:
        if y < 0 or y >= max_y:
            return False
        if x < 0 or x >= max_x:
            return False
        return True

    # go through each ant
    for ant in ants:
        letter = ant[0]
        x = ant[1][0]
        y = ant[1][1]

        for direction in [U, UR, R, DR, D, DL, L, UL]:
            distance = 1
            next_index = get_next_index(x, y, direction, distance)
            while in_bounds(*next_index):
                if grid[next_index[1]][next_index[0]] == letter:
                    potential_antinode = get_next_index(next_index[0], next_index[1], direction, distance)
                    if in_bounds(*potential_antinode):
                        found_nodes.add((letter, potential_antinode))
                distance += 1
                next_index = get_next_index(x, y, direction, distance)

    return len(found_nodes)


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
        result = solve_part_1(file_path)
    elif args.part == 2:
        result = solve_part_2(file_path)
    else:
        exit(0)

    print(f"Result: {result}")
