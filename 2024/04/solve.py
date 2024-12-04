from typing import List

def build_matrix(path: str) -> List[List[str]]:
    with open(path) as file:
        return [[letter for letter in line.strip()] for line in file]

def surrounding_indices(x: int, y: int) -> List[List[List[int]]]:
    return [
        [x - 1, y - 1], [x, y - 1], [x + 1, y - 1],
        [x - 1, y],                 [x + 1, y],
        [x - 1, y + 1], [x, y + 1], [x + 1, y + 1]
    ]

def get_next_index(x: int, y: int, curr_x: int, curr_y: int) -> List[int]:
    dir_x = x - curr_x
    dir_y = y - curr_y
    if dir_x == 0:
        next_x = x
    elif dir_x < 0:
        next_x = curr_x + 1
    elif dir_x > 0:
        next_x = curr_x - 1

    if dir_y == 0:
        next_y = y
    elif dir_y < 0:
        next_y = curr_y + 1
    elif dir_y > 0:
        next_y = curr_y - 1

    return [next_x, next_y]


def execute_01(matrix: List[List[str]]) -> int:
    start = "X"
    search_arr = "MAS"
    match_count = 0
    max_x = len(matrix[0])
    max_y = len(matrix)

    # Loop through each letter and if its a start, check in all directions for a word
    # Dont forget that matrices are index'd by y, x
    # should also check for out of bounds
    for y, row in enumerate(matrix):
        for x, letter in enumerate(row):
            if letter != start:
                continue

            def check_next_letter(look_x: int, look_y: int, word_so_far: List[List[int]], cursor: int = 0) -> tuple[bool, List[List[int]]]:
                look_letter = matrix[look_y][look_x]
                if look_letter == search_arr[cursor]:
                    cursor += 1
                else:
                    return False, None

                word_so_far.append([look_x, look_y])
                if cursor == len(search_arr):
                    return True, word_so_far

                next_x, next_y = get_next_index(x, y, look_x, look_y)

                if next_x < 0 or next_x >= max_x:
                    return False, None
                if next_y < 0 or next_y >= max_y:
                    return False, None
                
                return check_next_letter(next_x, next_y, word_so_far, cursor)

            for look_x, look_y in surrounding_indices(x, y):
                if look_y < 0 or look_y >= max_y:
                    continue
                if look_x < 0 or look_x >= max_x:
                    continue
                word_so_far = [[x, y]]
                valid, built_word = check_next_letter(look_x, look_y, word_so_far)
                if valid:
                    #print(built_word)
                    match_count += 1
    return match_count


if __name__ == "__main__":
    matrix = build_matrix("input.txt")
    print(execute_01(matrix))
    #execute_02(path)