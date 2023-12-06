import math
from functools import reduce


def read_input(file_path):
    with open(file_path) as file:
        return file.read()


def parse_input(case, content):
    sections = content.split("\n")
    times, distances = sections
    if case == "first":
        times = [int(i) for i in times.split(":")[1].split(" ") if i]
        distances = [int(i) for i in distances.split(":")[1].split(" ") if i]
        return times, distances
    times = [int(times.split(":")[1].replace(" ", ""))]
    distances = [int(distances.split(":")[1].replace(" ", ""))]
    return times, distances


def equation_roots(a, b, c):
    dis = b * b - 4 * a * c
    sqrt_val = math.sqrt(abs(dis))

    if dis > 0:
        return (-b - sqrt_val) / (2 * a), (-b + sqrt_val) / (2 * a)

    elif dis == 0:
        return -b / (2 * a)

    return None


def get_possible_time(time, distance):
    roots = equation_roots(1, -time, distance)
    if len(roots) < 2:
        return 0
    lower_bound, upper_bound = roots
    valid_lower_bound = int(math.floor((lower_bound))) + 1
    valid_upper_bound = int(math.ceil(upper_bound)) - 1
    return valid_upper_bound - valid_lower_bound + 1


def get_result(case: str, file_path: str):
    content = read_input(file_path)
    times, distances = parse_input(case, content)

    valid_choices = [
        get_possible_time(time, distance) for time, distance in zip(times, distances)
    ]
    return reduce(lambda x, y: x * y, valid_choices)


if __name__ == "__main__":
    print(get_result("first", "data/2023/day06/wait_for_it/sample.txt"))
    print(get_result("first", "data/2023/day06/wait_for_it/input1.txt"))
    print(get_result("second", "data/2023/day06/wait_for_it/sample.txt"))
    print(get_result("second", "data/2023/day06/wait_for_it/input1.txt"))
