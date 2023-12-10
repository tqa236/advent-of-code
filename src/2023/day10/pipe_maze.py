DIRECTIONS = {
    "|": [(-1, 0), (1, 0)],
    "-": [(0, -1), (0, 1)],
    "L": [(-1, 0), (0, 1)],
    "J": [(-1, 0), (0, -1)],
    "7": [(1, 0), (0, -1)],
    "F": [(1, 0), (0, 1)],
    ".": [],
}


def read_input(file_path):
    with open(file_path) as file:
        return file.read()


def parse_input(content):
    matrix = content.split("\n")
    return matrix


def get_starting_position(matrix):
    for i, row in enumerate(matrix):
        if "S" in row:
            return (i, row.index("S"))


def get_reverse_direction(direction):
    return (-direction[0], -direction[1])


def get_default_directions(position, matrix):
    default_directions = set([(-1, 0), (1, 0), (0, -1), (0, 1)])
    if position[0] == 0:
        default_directions.remove((-1, 0))
    if position[0] == len(matrix) - 1:
        default_directions.remove((1, 0))
    if position[1] == 0:
        default_directions.remove((0, -1))
    if position[1] == len(matrix[0]) - 1:
        default_directions.remove((0, 1))
    return default_directions


def move(position, direction):
    return (position[0] + direction[0], position[1] + direction[1])


def get_possible_direction(position, matrix):
    directions = []
    default_directions = get_default_directions(position, matrix)
    for direction in default_directions:
        next_position = move(position, direction)
        reverse_direction = get_reverse_direction(direction)
        if reverse_direction in DIRECTIONS[matrix[next_position[0]][next_position[1]]]:
            directions.append(direction)
    return directions


def next_step(position, direction, matrix):
    next_position = move(position, direction)
    next_direction = [
        new_direction
        for new_direction in DIRECTIONS[matrix[next_position[0]][next_position[1]]]
        if new_direction != get_reverse_direction(direction)
    ][0]
    return next_position, next_direction


def get_path(position):
    return [(i, position[1]) for i in range(position[0])]


def count_cut(position, loop, matrix):
    path = get_path(position)
    return len(
        [
            i
            for i in path
            if i in loop
            and set(DIRECTIONS[matrix[i[0]][i[1]]])
            in [
                set(DIRECTIONS["-"]),
                set(DIRECTIONS["7"]),
                set(DIRECTIONS["J"]),
            ]
        ]
    )


def get_result(case: str, file_path: str):
    content = read_input(file_path)
    matrix = parse_input(content)
    position = get_starting_position(matrix)
    directions = get_possible_direction(position, matrix)
    DIRECTIONS["S"] = directions
    direction = directions[0]
    step = 0
    positions = [position]
    while matrix[position[0]][position[1]] != "S" or step == 0:
        position, direction = next_step(position, direction, matrix)
        positions.append(position)
        step += 1
    if case == "first":
        return step // 2

    positions = set(positions)
    count = 0
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if (i, j) not in positions:
                if count_cut((i, j), positions, matrix) % 2 == 1:
                    count += 1
    return count


if __name__ == "__main__":
    print(get_result("first", "data/2023/day10/pipe_maze/sample.txt"))
    print(get_result("first", "data/2023/day10/pipe_maze/sample2.txt"))
    print(get_result("first", "data/2023/day10/pipe_maze/input1.txt"))
    print(get_result("second", "data/2023/day10/pipe_maze/sample.txt"))
    print(get_result("second", "data/2023/day10/pipe_maze/sample3.txt"))
    print(get_result("second", "data/2023/day10/pipe_maze/sample4.txt"))
    print(get_result("second", "data/2023/day10/pipe_maze/sample5.txt"))
    print(get_result("second", "data/2023/day10/pipe_maze/input1.txt"))
