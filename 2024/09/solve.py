import argparse, itertools
from argparse import Namespace
from typing import List, Dict, Set, Tuple


def solve_part_2(file_path: str):
    pass


def solve_part_1(file_path: str) -> int:
    blocks = defrag(get_file_contents(file_path))
    from pdb import set_trace; set_trace()
    return calculate_checksum(blocks)


def get_file_contents(file_path: str) -> List[int]:
    with open(file_path) as file:
        return [int(c.strip()) for row in file for c in row.strip()]
    

def defrag(blocks: List[int]) -> List[int]:
    left_cursor = 0
    right_cursor = len(blocks) - 1
    right_id = int(right_cursor / 2)
    left_id = 0
    d_blocks = []


    insert_id =  None
    left_id = 0
    direction = "from_left"
    while right_cursor > 0 and left_cursor < len(blocks) - 1:
        if left_cursor % 2 == 0 or left_cursor == 0:
            insert_id = left_id
            size_block = blocks[left_cursor]
            direction = "from_left"
        else:
            insert_id = right_id
            size_block = blocks[right_cursor]
            direction = "from_right"

        size_free = blocks[left_cursor]

        while size_free > 0 and size_block > 0:
            d_blocks.append(insert_id)
            size_free -= 1
            size_block -= 1

        if size_free == 0:
            left_cursor += 1

        if size_block == 0:
            if direction == "from_right":
                right_cursor -= 2
                right_id -= 1
            else:
                left_id += 1

    return d_blocks


def calculate_checksum(blocks: List[int]) -> int:
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
        result = solve_part_1(file_path)
    elif args.part == 2:
        result = solve_part_2(file_path)
    else:
        exit(0)

    print(f"Result: {result}")
