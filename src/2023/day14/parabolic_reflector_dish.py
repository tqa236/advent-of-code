def read_input(file_path):
    with open(file_path) as file:
        return file.read()


def parse_input(content):
    matrix = content.split("\n")
    return transpose_matrix(matrix)


def transpose_matrix(matrix):
    return tuple(list(zip(*matrix)))


def count_one_line(row):
    score = 0
    for i, symbol in enumerate(row):
        if symbol == "O":
            score += len(row) - i
    return score


def rotate_matrix(matrix):
    return tuple(list(zip(*matrix))[::-1])


def tilt_one_line(row):
    location = 0
    row = list(row)
    for i, symbol in enumerate(row):
        if symbol == "O":
            row[location], row[i] = row[i], row[location]
            location += 1
        elif symbol == "#":
            location = i + 1
    return tuple(row)


def tilt_matrix(matrix):
    return (tilt_one_line(row) for row in matrix)


def tile_one_cycle(matrix):
    for i in range(4):
        matrix = tilt_matrix(matrix)
        matrix = rotate_matrix(matrix)
    return matrix


def get_result(case: str, file_path: str):
    content = read_input(file_path)
    matrix = parse_input(content)
    if case == "first":
        return sum(count_one_line(row) for row in tilt_matrix(matrix))

    if case == "second":
        rotated_matrix = {}
        results = {}
        for i in range(10**9):
            matrix = tile_one_cycle(matrix)
            if matrix in rotated_matrix:
                start_cycle = rotated_matrix[matrix]
                cycle_length = i + 1 - start_cycle
                break
            else:
                rotated_matrix[matrix] = i + 1
            results[i + 1] = sum(count_one_line(row) for row in matrix)
    cycle_location = (10**9 - start_cycle) % cycle_length + start_cycle
    return results[cycle_location]


if __name__ == "__main__":
    print(get_result("first", "data/2023/day14/parabolic_reflector_dish/sample.txt"))
    print(get_result("first", "data/2023/day14/parabolic_reflector_dish/input1.txt"))
    print(get_result("second", "data/2023/day14/parabolic_reflector_dish/sample.txt"))
    print(get_result("second", "data/2023/day14/parabolic_reflector_dish/input1.txt"))
