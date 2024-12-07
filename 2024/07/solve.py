import argparse, itertools
from argparse import Namespace
from typing import List, Dict, Set, Tuple

ops = ["plus", "mult"]

def split_line(line: set) -> Tuple[int, List[int]]:
    parts = line.strip().split(": ")
    add = int(parts[0])
    nums = [int(p) for p in parts[1].split(" ")]

    return add, nums


def process_line(line: str, operators: List[str]) -> (bool, int):
    total, nums = split_line(line)
    start = nums[0]
    sequences = itertools.product(operators, repeat=len(nums) - 1)

    for sequence in sequences:
        current = start
        for i, n in enumerate(nums[1:]):
            op = sequence[i]
            if op == "+":
                current += n
            elif op == "*":
                current *= n
            elif op == "||":
                current = int(f"{current}{n}")
        if current == total:
            return True, total

    return False, total


def solve_part_2(file_path: str):
    valid = []
    with open(file_path) as file:
        for line in file:
            result, amt = process_line(line, ["+", "*", "||"])
            if result:
                valid.append(amt)
    return sum(valid)

def solve_part_1(file_path: str):
    valid = []
    with open(file_path) as file:
        for line in file:
            result, amt = process_line(line, ["+", "*"])
            if result:
                valid.append(amt)
    return sum(valid)

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
