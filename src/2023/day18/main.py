import numpy as np

DIRECTIONS = ["R", "D", "L", "U"]


def read_input(file_path):
    with open(file_path) as file:
        return file.read()


def parse_input(content):
    return [
        (row.split(" ")[0], int(row.split(" ")[1]), row.split(" ")[2][1:-1])
        for row in content.split("\n")
    ]


def move(position, direction, step):
    if direction == "U":
        return (position[0] - step, position[1])
    if direction == "D":
        return (position[0] + step, position[1])
    if direction == "L":
        return (position[0], position[1] - step)
    if direction == "R":
        return (position[0], position[1] + step)


def get_vertices(start_position, rows):
    vertices = [start_position]
    position = start_position
    for row in rows:
        position = move(position, row[0], row[1])
        vertices.append(position)
    return vertices


def count_points_on_edges(vertices):
    count = 0
    for i in range(len(vertices) - 1):
        count += abs(vertices[i + 1][0] - vertices[i][0]) + abs(
            vertices[i + 1][1] - vertices[i][1]
        )
    return count


def count_points(vertices):
    points = np.array(np.vstack(vertices))
    x = points[:, 0]
    y = points[:, 1]
    area = polygon_area(x, y)
    point_on_edges = count_points_on_edges(vertices)
    point_inside = (2 * area - point_on_edges + 2) / 2
    return int(point_on_edges + point_inside)


def polygon_area(x, y):
    correction = x[-1] * y[0] - y[-1] * x[0]
    main_area = np.dot(x[:-1], y[1:]) - np.dot(y[:-1], x[1:])
    return 0.5 * np.abs(main_area + correction)


def decode_instruction(row):
    step = int(row[2][1:-1], 16)
    direction = DIRECTIONS[int(row[2][-1])]
    return (direction, step)


def get_result(case: str, file_path: str):
    content = read_input(file_path)
    rows = parse_input(content)
    if case == "second":
        rows = [decode_instruction(row) for row in rows]
    start_position = (0, 0)
    vertices = get_vertices(start_position, rows)

    return count_points(vertices)


if __name__ == "__main__":
    print(get_result("first", "data/2023/day18/sample.txt"))
    print(get_result("first", "data/2023/day18/input1.txt"))
    print(get_result("second", "data/2023/day18/sample.txt"))
    print(get_result("second", "data/2023/day18/input1.txt"))
