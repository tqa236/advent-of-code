from enum import Enum

MAX_DISTANCE = 10000


class Direction(Enum):
    NORTH = (-1, 0)
    EAST = (0, 1)
    SOUTH = (1, 0)
    WEST = (0, -1)


def read_input(file_path):
    with open(file_path) as file:
        return file.read()


def parse_input(content):
    matrix = content.split("\n")
    matrix = add_border(matrix)
    return matrix


def add_border(matrix):
    matrix = ["#" + row + "#" for row in matrix]
    matrix = ["#" * len(matrix[0])] + matrix + ["#" * len(matrix[0])]
    return matrix


def get_starting_position(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == "S":
                return i, j


def move(position, direction):
    return position[0] + direction.value[0], position[1] + direction.value[1]


def get_valid_move(position, matrix, distance):
    valid_positions = []
    for direction in Direction:
        next_position = move(position, direction)
        if (
            matrix[next_position[0]][next_position[1]] != "#"
            and distance[next_position[0]][next_position[1]]
            > distance[position[0]][position[1]] + 1
        ):
            valid_positions.append(next_position)
    return valid_positions


def bfs(starting_position, matrix):
    distance = [
        [MAX_DISTANCE for j in range(len(matrix[0]))] for i in range(len(matrix))
    ]
    distance[starting_position[0]][starting_position[1]] = 0
    to_visit = [starting_position]
    while to_visit:
        position = to_visit.pop(0)
        valid_positions = get_valid_move(position, matrix, distance)
        # print(position)
        # print(valid_positions)

        for valid_position in valid_positions:
            distance[valid_position[0]][valid_position[1]] = (
                distance[position[0]][position[1]] + 1
            )
        to_visit += valid_positions
    return distance


def get_result(case: str, file_path: str, step):
    content = read_input(file_path)
    matrix = parse_input(content)
    starting_position = get_starting_position(matrix)
    distance = bfs(starting_position, matrix)
    # print(distance)
    # for i in distance:
    #     print(i)
    if case == "first":
        return sum(
            len([i for i in row if i <= step and i % 2 == 0]) for row in distance
        )
    even_corners = sum(
        len([i for i in row if MAX_DISTANCE > i > 65 and i % 2 == 0])
        for row in distance
    )
    odd_corners = sum(
        len([i for i in row if MAX_DISTANCE > i > 65 and i % 2 == 1])
        for row in distance
    )
    even_full = sum(
        len([i for i in row if i < MAX_DISTANCE and i % 2 == 0]) for row in distance
    )
    odd_full = sum(
        len([i for i in row if i < MAX_DISTANCE and i % 2 == 1]) for row in distance
    )
    n = (step - (len(matrix) - 2) // 2) // (len(matrix) - 2)
    return (
        (n + 1) ** 2 * odd_full
        + n**2 * even_full
        - (n + 1) * odd_corners
        + n * even_corners
    )


if __name__ == "__main__":
    print(get_result("first", "data/2023/day21/sample.txt", 6))
    print(get_result("first", "data/2023/day21/input1.txt", 64))
    print(get_result("second", "data/2023/day21/input1.txt", 26501365))
