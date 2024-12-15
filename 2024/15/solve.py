from __future__ import annotations
import argparse, itertools, copy, functools, operator
from collections import defaultdict
from argparse import Namespace
from typing import List, Dict, Set, Tuple, Type

def get_moves(file: str) -> List[str]:
    with open(f"{file}_moves.txt") as file:
        return [cell.strip() for row in file for cell in row.strip()]


def get_map(file: str) -> List[List[str]]:
    with open(f"{file}_map.txt") as file:
        return [[cell.strip() for cell in row.strip()] for row in file]


def print_map(
        max_x: int, max_y: int, 
        boxes: Set[Tuple[int, int]], 
        walls: Set[Tuple[int, int]], 
        robot: Tuple[int, int]) -> None:
    for y in range(max_y):
        row = ""
        for x in range(max_x):
            if (x, y) in walls:
                row += "#"
            elif (x, y) in boxes:
                row += "O"
            elif (x, y) == robot:
                row += "@"
            else:
                row += "."
        print(row)


def get_new_pos(move: str, robot: Tuple[int, int]) -> Tuple[int, int]:
    x, y = robot
    if move == "^":
        return (x, y - 1)
    elif move == "<":
        return (x - 1, y)
    elif move == ">":
        return (x + 1, y)
    elif move == "v":
        return (x, y + 1)



def solve(file: str) -> any:
    moves_raw = get_moves(file)
    map_raw = get_map(file)

    max_x = len(map_raw[0])
    max_y = len(map_raw)
    boxes = set()
    walls = set()
    robot = None

    for y, row in enumerate(map_raw):
        for x, cell in enumerate(row):
            if cell == "@":
                robot = (x, y)
            elif cell == "#":
                walls.add((x, y))
            elif cell == "O":
                boxes.add((x, y))

    print_map(max_x, max_y, boxes, walls, robot)

    for move in moves_raw:
        new_robot = get_new_pos(move, robot)
        if new_robot in walls:
            continue
        if new_robot in boxes:
            box_to_move = new_robot
            boxes_to_move = []
            while box_to_move:
                new_box = get_new_pos(move, box_to_move)
                if new_box in walls:
                    boxes_to_move = []
                    break
                if new_box in boxes:
                    box_to_move = new_box
                else:
                    box_to_move = None
                boxes_to_move.append(new_box)
            if len(boxes_to_move) > 0:
                boxes.remove(new_robot) 
                robot = new_robot
            for box in boxes_to_move:
                boxes.add(box)
        else:
            robot = new_robot
        #print(f"MOVE: {move}")
        #print_map(max_x, max_y, boxes, walls, robot)
        #from pdb import set_trace; set_trace()
        #continue
    return sum(100*c[1]+c[0] for c in boxes)





        

 

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
        file = "test"
    else:
        file= "input"

    if args.part == 1:
        result = solve(file)
    elif args.part == 2:
        result = solve(file)
    else:
        exit(0)

    print(f"Result: {result}")
