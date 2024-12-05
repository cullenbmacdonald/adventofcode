import argparse
from typing import Any, List, Dict

class Page():
    def __init__(self, num: int):
        self.num = num

        self.appears_before = set()
        self.appears_after = set()

    def __lt__(self, other) -> bool:
        return other.num in self.appears_before or self.num in other.appears_after


def process_file(file_path: str) -> tuple[str, str]:
    rules = []
    updates = []

    do_updates = False
    with open(file_path) as file:
        for line in file:
            if do_updates:
                updates.append(line.strip())
            elif line == "\n":
                do_updates = True
            else:
                rules.append(line.strip())
    return (rules, updates)

def build_rules(raw: List[str]) -> Dict[int, Dict[str, List[int]]]:
    rules_hash = {}
    for line in raw:
        split = line.split("|")
        before = int(split[0])
        after = int(split[1])
        existing_before = rules_hash.get(before, {"BEFORE": set(), "AFTER": set()})
        existing_after = rules_hash.get(after, {"BEFORE": set(), "AFTER": set()})
        existing_before["BEFORE"].add(after)
        existing_after["AFTER"].add(before)
        rules_hash[before] = existing_before
        rules_hash[after] = existing_after

    return rules_hash


def solve_part_2(file_path: str):
    pass


def solve_part_1(file_path: str):
    rules_raw, updates_raw = process_file(file_path)    
    rules_hash = build_rules(rules_raw)
    print(rules_hash)



#### TEMPLATE FOR EACH DAY BEGIN NOW

def parse_args() -> Any:
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
        result = solve_part_1(file_path)
    else:
        exit(0)

    print(f"Result: {result}")
