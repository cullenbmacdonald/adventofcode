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

def get_obstacles(grid: List[List[str]]) -> Set[Tuple[int]]:
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


def guard_inbounds(position: Tuple[int], grid: List[List[str]]) -> bool:
    max_x = len(grid[0]) - 1
    max_y = len(grid) - 1
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
    grid = []
    with open(file_path) as file:
        for row in file:
            grid.append([cell for cell in row.strip()])

    obstacles = get_obstacles(grid)
    placed_obstacles = set()
    # For progress logging
    total = len(grid) * len(grid[0])
    count = 0

    # Ok lets put a temporary obstacle in each cell and see if we get a loop
    for temp_obs in [(obs_y, obs_x) for obs_y in range(len(grid)) for obs_x in range(len(grid))]:
        visited = set()
        guard_position = guard_start_position(grid)
        direction_i = 0
        count +=1

        print(f"checking {count} out of {total} potential obstacles")

        if temp_obs in obstacles:
            continue
        obstacles.add(temp_obs)

        while guard_inbounds(guard_position, grid):
            visited.add((guard_position, direction_i))
            guard_position, direction_i = walk(guard_position, direction_i, obstacles)
            
            # If we've been here going this direction before, then we're in a lop
            if (guard_position, direction_i) in visited:
                placed_obstacles.add(temp_obs)
                break
        obstacles = get_obstacles(grid)
    return len(placed_obstacles)


def solve_part_1(file_path: str):
    grid = []
    with open(file_path) as file:
        for row in file:
            grid.append([cell for cell in row.strip()])

    obstacles = get_obstacles(grid)
    guard_position = guard_start_position(grid)
    direction_i = 0

    visited = set()
    while guard_inbounds(guard_position, grid):
        visited.add(guard_position)
        guard_position, direction_i = walk(guard_position, direction_i, obstacles)
        
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
