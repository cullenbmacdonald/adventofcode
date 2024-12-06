import argparse
from argparse import Namespace
from typing import List, Dict, Set, Tuple

direction_order = ["up", "right", "down", "left"]
moves = {
    "up": (0, -1),
    "right": (1, 0),
    "down": (0, 1),
    "left": (-1, 0)
}

def build_sparse_positions(grid: List[List[str]]) -> Set[Tuple[int]]:
    obstacles = set()
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == "#":
                obstacles.add((x, y))
    return obstacles


def guard_start_position(grid: List[List[str]]) -> Tuple[int]:
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == "^":
                return (x, y)


def guard_inbounds(position: Tuple[int], max_x: int, max_y) -> bool:
    return (position[0] >= 0 and position[0] <= max_x) and \
        (position[1] >= 0 and position[1] <= max_y)


def walk(start: Tuple[int], direction_i: int, obstacles: Set[Tuple[int]]) -> Tuple[Tuple[int], int]:
    change = moves[direction_order[direction_i]]
    new_position = (start[0] + change[0], start[1] + change[1])
    if new_position in obstacles:
        if direction_i >= len(direction_order) - 1:
            direction_i = 0
        else:
            direction_i += 1
        return start, direction_i
    return new_position, direction_i


def print_grid(grid):
    for row in grid:
        print(''.join(row))
    print("\n")
    

def solve_part_2(file_path: str):
    pass


def solve_part_1(file_path: str):
    grid = []
    with open(file_path) as file:
        for row in file:
            grid.append([cell for cell in row.strip()])

    obstacles = build_sparse_positions(grid)
    guard_position = guard_start_position(grid)
    direction_i = 0
    max_x = len(grid[0]) - 1
    max_y = len(grid) - 1
    print_grid(grid)

    visited = set()
    while guard_inbounds(guard_position, max_x, max_y):
        visited.add(guard_position)
        grid[guard_position[1]][guard_position[0]] = "X"
        guard_position, direction_i = walk(guard_position, direction_i, obstacles)
        
    print_grid(grid)
    return len(visited)


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
