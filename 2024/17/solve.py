from __future__ import annotations
import argparse, itertools, copy, functools, operator
from collections import defaultdict
from argparse import Namespace
from typing import List, Dict, Set, Tuple, Type

registers = {
    "A": None,
    "B": None,
    "C": None,
}

def restore_state(file: str) -> List[int]:
    with open(file) as f:
        for line in f:
            if "Register " in line:
                val = line.strip("Register ").split()
                registers[val[0].strip(":")] = int(val[1].strip())
            elif "Program: " in line:
                return [int(l) for l in line.strip("Program: ").split(",")]

def combo_operand(val: int) -> int:
    match val:
        case 4:
            return registers["A"]
        case 5:
            return registers["B"]
        case 6:
            return registers["C"]
        case 7:
            raise NotImplemented
        case default:
            return val


def adv(operand):
    denom = 2**combo_operand(operand)
    registers["A"] = int(registers["A"] / denom)

def bxl(operand):
    registers["B"] = registers["B"] ^ operand

def bst(operand):
    registers["B"] = combo_operand(operand) % 8

def bxc(operand):
    registers["B"] = registers["B"] ^ registers["C"]

def out_fn(operand):
    return combo_operand(operand) % 8

def bdv(operand):
    denom = 2**combo_operand(operand)
    registers["B"] = int(registers["A"] / denom)

def cdv(operand):
    denom = 2**combo_operand(operand)
    registers["C"] = int(registers["A"] / denom)

def solve(program: List[int]) -> any:
    out = []
    pointer = 0
    while pointer < len(program):
        opcode = program[pointer]
        operand = program[pointer + 1]
        match opcode:
            case 0:
                adv(operand)
            case 1:
                bxl(operand)
            case 2:
                bst(operand)
            case 3:
                if registers["A"] != 0:
                    pointer = operand
                    continue
            case 4:
                bxc(operand)
            case 5:
                out.append(out_fn(operand))
            case 6:
                bdv(operand)
            case 7:
                cdv(operand)

        pointer += 2
    return out


def find_register_a(program: List[int]) -> int:
    reg_a = 0
    registers = {"A": 0, "B": 0, "C": 0}
    
    while program != solve(program):
        print(f"trying {reg_a}")
        registers = {"A": 0, "B": 0, "C": 0}
        reg_a += 1
        registers["A"] = reg_a

    return reg_a



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
        file = "test.txt"
    else:
        file= "input.txt"

    ## load the program
    program = restore_state(file)

    if args.part == 1:
        result = solve(program)
    elif args.part == 2:
        result = find_register_a(program)
    else:
        exit(0)

    print(f"Result: {result}")
