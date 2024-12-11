from __future__ import annotations
import argparse, itertools, copy
from collections import defaultdict
from argparse import Namespace
from typing import List, Dict, Set, Tuple, Type
from gmpy2 import mpz

def get_file_contents(file_path: str) -> List[int]:
    with open(file_path) as file:
        for row in file:
            return [int(l.strip()) for l in row.strip().split(" ")]


class Node:
    def __init__(self, value: int, head: Type[Node] | None = None, spawned=False, next_node: Type[Node] | None = None):
        self.value = value
        self.head = head
        self.next_node = next_node
        self.spawned = spawned
        self.count = 1
        if head is None:
            self.head = self
        else:
            self.head.count += 1

    def blink(self):
        str_value = str(self.value)
        str_length = len(str_value)

        # if self.spawned:
        #     self.spawned = False
        if self.value == 0:
            self.value = 1
        elif str_length % 2 == 0:
            left = str_value[:str_length//2]
            right = str_value[str_length//2:]
            self.value = int(left)
            prev_next_node = self.next_node
            new_node = Node(int(right), head=self.head, spawned=True, next_node=prev_next_node)
            self.next_node = new_node
        else: 
            self.value *= 2024


def process_one(value: int, this_blink_count: int, computed: Dict[int, int]) -> int:
    key = (value, this_blink_count)
    count = computed.get(key, None)
    if count:
        return count
    count = 1
    for i in range(this_blink_count):
        str_value = str(value)
        str_length = len(str_value)
        if value == 0:
            value = 1
        elif str_length % 2 == 0:
            left = str_value[:str_length//2]
            right = str_value[str_length//2:]
            value = int(left)
            count += process_one(int(right), this_blink_count - 1 - i, computed)
        else: 
            value *= 2024
    computed[key] = count
    return computed[key]


def solve_fast(file_path: str, blink_count: int) -> int:
    computed: Dict[int, int] = {}
    return sum(process_one(value, blink_count, computed) for value in get_file_contents(file_path))


def solve(file_path: str, blink_count: int) -> int:
    head: Node | None = None
    prev: Node | None = None
    for i, engraving in enumerate(get_file_contents(file_path)):
        new_node = Node(engraving, head=head)
        if prev:
            prev.next_node = new_node
        if head is None:
            head = new_node
        prev = new_node

    for i in range(blink_count):
        print(f"blinking {i+1} out of {blink_count} times")
        stone = head 
        while stone:
            next_node = stone.next_node
            stone.blink()

            if next_node:
                stone = next_node
            else:
                stone = None

    
    return head.count

 

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
        result = solve_fast(file_path, blink_count=25)
    elif args.part == 2:
        result = solve_fast(file_path, blink_count=75)
    else:
        exit(0)

    print(f"Result: {result}")
