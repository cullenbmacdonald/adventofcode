from __future__ import annotations
import argparse, itertools, copy, functools, operator
from collections import defaultdict
from argparse import Namespace
from typing import List, Dict, Set, Tuple, Type

GRID_MAX_X = 101
GRID_MAX_Y = 103

def get_lines_for_file(file_path: str) -> List[str]:
    with open(file_path) as file:
        return [row.strip() for row in file]


class Robot:
    def __init__(self, coordinate: Tuple[int], velocity: Tuple[int]):
        self._original_coordinate = coordinate
        self.coordinate = coordinate
        self.velocity = velocity

    def move(self):
        x, y = self.coordinate
        new_x = self.velocity[0] + x
        new_y = self.velocity[1] + y

        if new_x >= GRID_MAX_X:
            new_x -= GRID_MAX_X
        elif new_x < 0:
            new_x += GRID_MAX_X

        if new_y >= GRID_MAX_Y:
            new_y -= GRID_MAX_Y
        elif new_y < 0:
            new_y += GRID_MAX_Y

        self.coordinate = (new_x, new_y)


def print_grid(width: int, height: int, robots: List[Robot]) -> None:
    robot_by_location = set()
    for robot in robots:
        robot_by_location.add(robot.coordinate)

    for y in range(height):
        string = ""
        for x in range(width):
            if (x, y) in robot_by_location:
                string += "#"
            else:
                string += "."
        print(string)


def solve(file_path: str) -> any:
    lines = get_lines_for_file(file_path)
    robots: List[Robot] = []
    for line in lines:
        coord_part, velo_part = line.split(" ")
        coord = tuple(int(p) for p in coord_part.split("=")[1].split(","))
        velo = tuple(int(p) for p in velo_part.split("=")[1].split(","))
        robots.append(Robot(coord, velo))

    locations = defaultdict(int)
    for robot in robots:
        x, y = robot.coordinate 
        locations[robot.coordinate] += 1

    inc = 33
    for c in range(10000):
        [robot.move() for robot in robots]
        if c+1 == inc:
            print(f"{c + 1} MOVES")
            print_grid(GRID_MAX_X, GRID_MAX_Y, robots)
            inc += 103
            from pdb import set_trace; set_trace()
        print("")
        continue

    locations = {0: 0, 1: 0, 2: 0, 3: 0}
    half_x = ((GRID_MAX_X - 1) / 2) 
    half_y = ((GRID_MAX_Y - 1) / 2) 
    for robot in robots:
        x, y = robot.coordinate 

        if x < half_x and y < half_y:
            locations[0] += 1

        if x > half_x and y < half_y:
            locations[1] += 1
    
        if x < half_x and y > half_y:
            locations[2] += 1

        if x > half_x and y > half_y:
            locations[3] += 1

    return functools.reduce(operator.mul, locations.values())

 

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
        GRID_MAX_X = 11
        GRID_MAX_Y = 7
    else:
        file_path = "input.txt"

    if args.part == 1:
        result = solve(file_path)
    elif args.part == 2:
        result = solve(file_path)
    else:
        exit(0)

    print(f"Result: {result}")
