import argparse, itertools
from argparse import Namespace
from typing import List, Dict, Set, Tuple


def solve_part_2(file_path: str):
    blocks = defrag_contiguous_blocks(get_file_contents(file_path))
    return calculate_checksum(blocks)
    pass


def solve_part_1(file_path: str) -> int:
    blocks = defrag_split_blocks(get_file_contents(file_path))
    return calculate_checksum(blocks)


def get_file_contents(file_path: str) -> List[int]:
    with open(file_path) as file:
        return [int(c.strip()) for row in file for c in row.strip()]


def convert_blocks(blocks: List[int]) -> any:
    # First build an array of sized/id blocks
    left_cursor = 0
    insert_id = 0
    d_blocks = []

    while left_cursor < len(blocks):
        size = blocks[left_cursor]
        if left_cursor % 2 > 0:
            value = None
        else:
            value = insert_id
        while size > 0:
            d_blocks.append(value)
            size -= 1
        if left_cursor % 2 == 0:
            insert_id += 1
        left_cursor += 1
    
    return d_blocks


def defrag_contiguous_blocks(blocks: List[int]) -> List[int]:
    empty = [(-1, b_size) for i, b_size in enumerate(blocks) if i % 2 > 0]
    files = [(file_id, file_size) for file_id, file_size in enumerate([b for i, b in enumerate(blocks) if i % 2 == 0])]

    blocks = []
    for i, file in enumerate(files):
        blocks.append(file)
        try:
            blocks.append(empty[i])
        except IndexError:
            pass

    right_cursor = len(blocks) - 1
    seen = set()
    while right_cursor > 0:
        left_cursor = 0
        file_id, file_size = blocks[right_cursor]

        if file_id >= 0 and file_id not in seen:
            while left_cursor < len(blocks) and left_cursor < right_cursor:
                look_id, look_size = blocks[left_cursor]
                remaining_size = look_size - file_size

                if look_id < 0 and remaining_size >= 0 and (file_id, file_size):
                    blocks[left_cursor] = (file_id, file_size)
                    blocks[right_cursor] = (-1, file_size)
                    if remaining_size > 0:
                        blocks.insert(left_cursor + 1, (-1, remaining_size))
                    break
                left_cursor += 1
            seen.add(file_id)
        right_cursor -= 1
    
    ret = []

    for block in blocks:
        block_id, block_size = block
        for _ in range(block_size):
            if block_id == -1:
                ret.append(None)
            else:
                ret.append(block_id)

    return ret
    

def defrag_split_blocks(blocks: List[int]) -> List[int]:
    blocks = convert_blocks(blocks)

    # Pack the bins
    right_cursor = len(blocks) - 1
    left_cursor = 0

    while right_cursor > 0 and left_cursor < len(blocks) - 1:
        if blocks[right_cursor] is None:
            right_cursor -= 1
            continue
        if blocks[left_cursor] is None:
            block_id = blocks.pop()
            if block_id != None:
                blocks[left_cursor] = block_id
                right_cursor -= 1
        else:
            left_cursor += 1        

    return [block for block in blocks]


def calculate_checksum(blocks: List[int]) -> int:
    return sum([i * v for i, v in enumerate(blocks) if v is not None])


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
