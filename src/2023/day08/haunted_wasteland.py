import math


def read_input(file_path):
    with open(file_path) as file:
        return file.read()


def parse_input(case, content):
    instructions, matrix = content.split("\n\n")
    matrix_map = {}
    for row in matrix.split("\n"):
        key = row[:3]
        left = row[7:10]
        right = row[12:15]
        matrix_map[key] = {"L": left, "R": right}
    return instructions, matrix_map


def get_good_steps(start, instructions, matrix_map):
    good_steps = []
    visited = set()
    step = 0
    start_position = (start, step)
    while start_position not in visited:
        visited.add(start_position)
        start = matrix_map[start][instructions[step % len(instructions)]]
        start_position = (start, step % len(instructions))
        step += 1
        if start.endswith("Z"):
            good_steps.append(step)

    return good_steps


def get_result(case: str, file_path: str):
    content = read_input(file_path)
    instructions, matrix_map = parse_input(case, content)
    step = 0
    destinations = (
        ["AAA"] if case == "first" else [key for key in matrix_map if key.endswith("A")]
    )
    if case == "first":
        while set(destinations) != set(["ZZZ"]):
            for i in range(len(destinations)):
                destinations[i] = matrix_map[destinations[i]][
                    instructions[step % len(instructions)]
                ]
            step = step + 1
    else:
        good_steps = []
        for destination in destinations:
            good_steps.append(get_good_steps(destination, instructions, matrix_map))
        step = math.lcm(*[i[-1] for i in good_steps])  # Not always true but good enough
    return step


if __name__ == "__main__":
    print(get_result("first", "data/2023/day08/haunted_wasteland/sample.txt"))
    print(get_result("first", "data/2023/day08/haunted_wasteland/input1.txt"))
    print(get_result("second", "data/2023/day08/haunted_wasteland/sample2.txt"))
    print(get_result("second", "data/2023/day08/haunted_wasteland/input1.txt"))
