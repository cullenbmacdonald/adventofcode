import argparse
from typing import Any, List, Dict

rules_db = {}

class Page():
    def __init__(self, num: int):
        self.num = num

        self.appears_before = set()
        self.appears_after = set()

    def __lt__(self, other) -> bool:
        return other.num in self.appears_before 

    def __eq__(self, other) -> bool:
        if type(other) == int:
            return self.num == other
        elif type(other) == Page:
            return self.num == other.num
        super()

    def __repr__(self) -> str:
        return str(self.num)


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


def build_rules(raw: List[str]) -> None:
    for line in raw:
        split = line.split("|")
        before_id = int(split[0])
        after_id = int(split[1])

        before = rules_db.get(before_id, Page(before_id))
        after = rules_db.get(after_id, Page(after_id))

        before.appears_before.add(after.num)
        rules_db[before.num] = before
        after.appears_after.add(before.num)
        rules_db[after.num] = after


def filter_valid_updates(rules: Dict[int, Page], updates: List[int], repaired_only: bool=False) -> List[List[Page]]:
    valid_updates = []
    for update in updates:
        og = [u for u in update]
        sorted_update = sorted([rules_db[u] for u in update])
        if og == sorted_update and not repaired_only:
            valid_updates.append(sorted_update)
        elif og != sorted_update and repaired_only:
            valid_updates.append(sorted_update)
    return valid_updates


def solve(file_path: str, repaired_only: bool=False) -> int:
    rules_raw, updates_raw = process_file(file_path)    
    updates = []
    for update in updates_raw:
        updates.append([int(page) for page in update.split(",")])
    rules_hash = build_rules(rules_raw)
    valid_updates = filter_valid_updates(rules_hash, updates, repaired_only=repaired_only)
    total = 0
    for update in valid_updates:
        middle = int(len(update) / 2)
        total += update[middle].num
    return total


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
        result = solve(file_path, repaired_only=False)
    elif args.part == 2:
        result = solve(file_path, repaired_only=True)
    else:
        exit(0)

    print(f"Result: {result}")
