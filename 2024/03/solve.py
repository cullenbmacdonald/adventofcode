import re
from functools import reduce
from operator import mul
from typing import List

reg = re.compile("mul\((\d+,\d+)\)")

def get_total_for_matches(matches: List[str]) -> int:
    total = 0
    for group in matches:
        total += mul(*[int(i) for i in group.split(",")])
    return total


def process_file(line: str) -> int:
    groups = reg.findall(line)
    return get_total_for_matches(groups)


def process_file_dos(file: str) -> int:
    split_up = file.split("don't()")
    first_groups = reg.findall(split_up[0])
    total = get_total_for_matches(first_groups)
    for do_chunk in split_up[1:]:
        split_donts = do_chunk.split("do()")
        for dos in split_donts[1:]:
            groups = reg.findall(dos)
            total += get_total_for_matches(groups) 
    return total


def execute(path: str, follow_instructions=False) -> int:
    with open(path) as f:
        contents = f.read().replace("\n", "")
        if follow_instructions: 
            return process_file_dos(contents)
        return process_file(contents)


if __name__ == "__main__":
    file_path = "input.txt"
    result_01 = execute(file_path, follow_instructions=False)
    result_02 = execute(file_path, follow_instructions=True)
    print(result_01)
    print(result_02)