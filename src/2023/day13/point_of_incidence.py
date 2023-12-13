import itertools


def read_input(file_path):
    with open(file_path) as file:
        return file.read()


def parse_input(content):
    matrices = content.split("\n\n")
    return [matrix.split("\n") for matrix in matrices]


def transpose_matrix(matrix):
    return list(zip(*matrix))


def check_reflection(matrix, error):
    reversed_matrix = matrix[::-1]
    reflection_lines = []
    for i in range(1, len(matrix)):
        half_length = min(i, len(matrix) - i)
        if (
            calculate_error(
                matrix[i - half_length : i + half_length],
                reversed_matrix[-i - half_length : -i + half_length or None],
            )
            == error
        ):
            reflection_lines.append(i)
    return reflection_lines


def calculate_error(list1, list2):
    return sum(
        i != j
        for i, j in zip(
            itertools.chain.from_iterable(list1), itertools.chain.from_iterable(list2)
        )
    )


def get_result(case: str, file_path: str):
    content = read_input(file_path)
    matrices = parse_input(content)
    if case == "first":
        error = 0
    else:
        error = 2
    return sum(
        sum(check_reflection(transpose_matrix(matrix), error)) for matrix in matrices
    ) + 100 * sum(sum(check_reflection(matrix, error)) for matrix in matrices)


if __name__ == "__main__":
    print(get_result("first", "data/2023/day13/point_of_incidence/sample.txt"))
    print(get_result("first", "data/2023/day13/point_of_incidence/sample2.txt"))
    print(get_result("first", "data/2023/day13/point_of_incidence/input1.txt"))
    print(get_result("second", "data/2023/day13/point_of_incidence/sample.txt"))
    print(get_result("second", "data/2023/day13/point_of_incidence/input1.txt"))
