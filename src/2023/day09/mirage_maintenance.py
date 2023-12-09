from math import comb


def read_input(file_path):
    with open(file_path) as file:
        return file.read()


def parse_input(content):
    rows = content.split("\n")
    rows = [[int(i) for i in series.split(" ")] for series in rows if series]
    return rows


def get_signature(series):
    differences = [series]
    while set(differences[-1]) != set([0]):
        differences.append(
            [
                differences[-1][i + 1] - differences[-1][i]
                for i in range(len(differences[-1]) - 1)
            ]
        )
    return [differences[i][0] for i in range(len(differences) - 1)]


def get_next_value(signature, n):
    return sum(comb(n, k) * signature[k] for k in range(len(signature)))


def get_result(case: str, file_path: str):
    content = read_input(file_path)
    rows = parse_input(content)
    total = 0
    for row in rows:
        if case == "second":
            row = row[::-1]
        signature = get_signature(row)
        total += get_next_value(signature, len(row))
    return total


if __name__ == "__main__":
    print(get_result("first", "data/2023/day09/mirage_maintenance/sample.txt"))
    print(get_result("first", "data/2023/day09/mirage_maintenance/input1.txt"))
    print(get_result("second", "data/2023/day09/mirage_maintenance/sample.txt"))
    print(get_result("second", "data/2023/day09/mirage_maintenance/input1.txt"))
