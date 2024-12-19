from __future__ import annotations
import argparse, itertools, copy, functools, operator
from collections import defaultdict, namedtuple, deque
from argparse import Namespace
from typing import List, Dict, Set, Tuple, Type

# returns up, down, left, right
def surrounding_indices(x: int, y: int) -> List[Tuple[str, int, int]]:
    return [
        ("v",x, y + 1),
        ("^", x, y - 1), 
        ("<", x - 1, y),
        (">", x + 1, y)
    ]


class Move:
    def __init__(self, facing: str, x: int, y: int, inc_score: int, total_score: int, board: Board):
        self.x = x
        self.y = y
        self.facing = facing
        self.inc_score = inc_score
        self.total_score = total_score
        self.board = board
        self.pos_moves = surrounding_indices(x, y)

    def move_tuple(self) -> Tuple[str, int, int]:
        return (self.facing, self.x, self.y)


class Board:
    def __init__(self, file: str):
        self.map_raw = self.__get_map(file)
        self.start = None
        self.end = None
        self.walls = set()
        self.dead_ends = set()
        self.solved_paths = []
        self.final_score_from_location = defaultdict(set)

        for y, row in enumerate(self.map_raw):
            for x, cell in enumerate(row):
                if cell == "S":
                    self.start = (x, y)
                elif cell == "#":
                    self.walls.add((x, y))
                elif cell == "E":
                    self.end = (x, y)

    def print_map(self, move: Move):
        for y in range(len(self.map_raw)):
            row = ""
            for x in range(len(self.map_raw[0])):
                if (x, y) in self.walls:
                    row += "#"
                elif (x, y) == (move.x, move.y):
                    row += move.facing
                elif (x, y) == self.end:
                    row += "E"
                elif (x, y) == self.start:
                    row += "S"
                else:
                    row += "."
            print(row)

    def __get_map(self, file: str) -> List[List[str]]:
        with open(f"{file}.txt") as file:
            return [[cell.strip() for cell in row.strip()] for row in file]


    def find_lowest_score(self) -> int:
        scores = []
        paths = deque([[set(), Move(">", self.start[0], self.start[1], 0, 0, self)]])
        iteration = 0
        while paths:
            print(iteration)
            iteration += 1
            current_path = paths.popleft()
            last_move = current_path[-1]
            seen = current_path[0]
            #self.print_map(last_move)
            if (last_move.x, last_move.y) == self.end:
                scores.append(last_move.total_score)
                final_score = last_move.total_score
                # for move in current_path[1:]:
                #     final_score -= move.inc_score
                #     self.final_score_from_location[move.move_tuple()].add(final_score)
                continue

            # try:
            #     score_from_here = min(self.final_score_from_location[last_move.move_tuple()])
            # except ValueError:
            #     score_from_here = None

            # if score_from_here:
            #     final_score = last_move.total_score + score_from_here
            #     scores.append(final_score)
            #     for move in current_path[1:]:
            #         self.final_score_from_location[move.move_tuple()].add(final_score)
            #         final_score -= move.inc_score
            #     continue

            seen = seen.union({(last_move.x, last_move.y)})

            pos_moves = [(facing, x, y) for facing, x, y in last_move.pos_moves
                         if (x, y) not in seen and 
                         (x, y) not in self.walls and
                         (facing, x, y) not in self.dead_ends]

            # if len(pos_moves) == 0:
            #     for move in reversed(current_path[1:]):
            #         if move.move_tuple() in self.dead_ends:
            #             continue
            #         pos_moves = [(facing, x, y) for facing, x, y in move.pos_moves
            #                     if (x, y) not in self.walls and
            #                     (facing, x, y) not in self.dead_ends]
            #         if len(pos_moves) > 1:
            #             break
            #         self.dead_ends = self.dead_ends.union(set(pos_moves))
            #     continue

            for pos_move in pos_moves:
                if pos_move[0] == last_move.facing:
                    inc_score = 1
                else:
                    inc_score = 1001

                move = Move(*pos_move, inc_score, last_move.total_score + inc_score, self)
                paths.extend([[seen, move]])
        return min(scores)


def solve(file: str) -> any:
    board = Board(file)
    return board.find_lowest_score()

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
