import argparse, itertools, copy
from argparse import Namespace
from typing import List, Dict, Set, Tuple

def get_file_contents(file_path: str) -> List[List[str]]:
    with open(file_path) as file:
        return [[l.strip() for l in row.strip()] for row in file]


def print_grid(grid):
    for row in grid:
        print(''.join(row))
    print("\n")

def get_next_index(from_i: Tuple[int, int], to_i: Tuple[int, int]) -> Tuple[int, int]:
    potential_antinode_x = to_i[0] + (to_i[0] - from_i[0])
    potential_antinode_y = to_i[1] + (to_i[1] - from_i[1])
    return (potential_antinode_x, potential_antinode_y)

def solve(file_path: str, keep_going=False):
    grid = get_file_contents(file_path)
    ants = [(value, (x, y)) for y, row in enumerate(grid) for x, value in enumerate(row) if value != "."]
    found_nodes = set()
    max_x = len(grid[0])
    max_y = len(grid)

    def in_bounds(x, y) -> bool:
        if y < 0 or y >= max_y:
            return False
        if x < 0 or x >= max_x:
            return False
        return True
    
    cursor = 0
    while cursor < len(ants):
        curr_ant, curr_index = ants[cursor]
        for ant, index in ants[cursor+1:]: # only look at ants after me
            if ant == curr_ant and curr_index != index:
                
                # if we dont care about distance, and we have a match, then add the node we're looking towards and ourselves
                if keep_going:
                    found_nodes.add(index)
                    found_nodes.add(curr_index)

                # Look in the same direction/distance from the current index to the next one
                # Because we'll never go the "other way", we need to process both directions 
                for to_i, from_i in [(curr_index, index), (index, curr_index)]:
                    potential = get_next_index(from_i, to_i)
                    while in_bounds(*potential):
                        found_nodes.add(potential)
                        if not keep_going:
                            break
                        from_i = to_i
                        to_i = potential
                        potential = get_next_index(from_i, to_i)

        # Increment cursor to start looking at the next ant
        cursor += 1

    # Print the thing for debugging
    for i in found_nodes:
        current_value = grid[i[1]][i[0]]
        if current_value == ".":
            grid[i[1]][i[0]] = "#"
    print_grid(grid)
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
        result = solve(file_path)
    elif args.part == 2:
        result = solve(file_path, keep_going=True)
    else:
        exit(0)

    print(f"Result: {result}")
