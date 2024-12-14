from __future__ import annotations
import argparse, itertools, copy
from collections import defaultdict
from argparse import Namespace
from typing import List, Dict, Set, Tuple, Type

def get_grid_from_file(file_path: str) -> List[List[str]]:
    with open(file_path) as file:
        return [[l.strip() for l in row.strip()] for row in file]


def get_lines_from_file(file_path: str) -> List[str]:
    with open(file_path) as file:
        return [row.strip() for row in file]


def entire_contents(file_path: str) -> str:
    with open(file_path) as file:
        return file.read()


def in_bounds(index: Tuple[int], grid: List[List[int]]) -> bool:
    x, y = index
    if y < 0 or y >= len(grid):
        return False
    if x < 0 or x >= len(grid[0]):
        return False
    return True
