from copy import deepcopy
from itertools import combinations


def read_input(file_path):
    with open(file_path) as file:
        return file.read()


def parse_input(content):
    matrix = content.split("\n")
    return [[i for i in row] for row in matrix]


def get_empty_row(matrix):
    return [i for i, row in enumerate(matrix) if "#" not in row]


def get_empty_column(matrix):
    return [
        i
        for i in range(len(matrix[0]))
        if "#" not in [matrix[j][i] for j in range(len(matrix))]
    ]


def expand_row(matrix, indices):
    reversed_indices = sorted(indices, reverse=True)
    empty_row = ["."] * len(matrix[0])
    for i in reversed_indices:
        matrix.insert(i, deepcopy(empty_row))
    return matrix


def expand_column(matrix, indices):
    reversed_indices = sorted(indices, reverse=True)
    for i in range(len(matrix)):
        for j in reversed_indices:
            matrix[i].insert(j, ".")
    return matrix


def get_galaxy(matrix):
    return [
        (i, j)
        for i in range(len(matrix))
        for j in range(len(matrix[0]))
        if matrix[i][j] == "#"
    ]


def get_galaxy_distance(
    left, right, empty_row_indices, empty_column_indices, expansion_factor
):
    base_distance = abs(left[0] - right[0]) + abs(left[1] - right[1])
    row_expansion = len(
        set(empty_row_indices).intersection(
            range(min(left[0], right[0]), max(left[0], right[0]) + 1)
        )
    ) * (expansion_factor - 1)

    column_expansion = len(
        set(empty_column_indices).intersection(
            range(min(left[1], right[1]), max(left[1], right[1]) + 1)
        )
    ) * (expansion_factor - 1)
    return base_distance + row_expansion + column_expansion


def get_result(case: str, file_path: str):
    if case == "first":
        expansion_factor = 2
    else:
        expansion_factor = 10**6
    content = read_input(file_path)
    matrix = parse_input(content)
    empty_row_indices = get_empty_row(matrix)
    empty_column_indices = get_empty_column(matrix)
    galaxy = get_galaxy(matrix)
    return sum(
        get_galaxy_distance(
            left, right, empty_row_indices, empty_column_indices, expansion_factor
        )
        for left, right in combinations(galaxy, 2)
    )


if __name__ == "__main__":
    print(get_result("first", "data/2023/day11/cosmic_expansion/sample.txt"))
    print(get_result("first", "data/2023/day11/cosmic_expansion/input1.txt"))
    print(get_result("second", "data/2023/day11/cosmic_expansion/input1.txt"))
