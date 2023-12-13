from copy import deepcopy
import functools


def read_input(file_path):
    with open(file_path) as file:
        return file.read()


def parse_input(content, fold):
    rows = content.split("\n")
    puzzles = []
    for row in rows:
        core_symbol = [i for i in row.split()[0]]
        symbol = deepcopy(core_symbol)
        for i in range(fold - 1):
            symbol = symbol + ["?"] + core_symbol
        quantity = [int(i) for i in row.split()[1].split(",")] * fold
        puzzles.append((tuple(symbol), tuple(quantity)))
    return puzzles


@functools.cache
def solve_puzzle(symbol, quantity, continuous):
    symbol = list(symbol)
    quantity = list(quantity)
    while symbol and symbol[0] == ".":
        if continuous:
            if quantity and quantity[0] > 0:
                return 0
        continuous = False
        symbol.pop(0)
        while quantity and quantity[0] == 0:
            quantity.pop(0)
    if not symbol:
        if not quantity or sum(quantity) == 0:
            return 1
        return 0
    if symbol[0] == "#":
        if quantity and quantity[0] > 0:
            return solve_puzzle(
                tuple(symbol[1:]),
                tuple([quantity[0] - 1] + quantity[1:]),
                continuous=True,
            )
        else:
            return 0
    else:
        if continuous:
            if quantity and quantity[0] == 0:
                return solve_puzzle(
                    (tuple(["."] + symbol[1:])), tuple(quantity), continuous=False
                )
            return solve_puzzle(
                tuple(["#"] + symbol[1:]), tuple(quantity), continuous=True
            )
        return solve_puzzle(
            tuple(["#"] + symbol[1:]), tuple(quantity), continuous=False
        ) + solve_puzzle(tuple(["."] + symbol[1:]), tuple(quantity), continuous=False)


def get_result(case: str, file_path: str):
    if case == "first":
        fold = 1
    else:
        fold = 5
    content = read_input(file_path)
    puzzles = parse_input(content, fold)
    count = 0
    for i, puzzle in enumerate(puzzles):
        result = solve_puzzle(*puzzle, continuous=False)
        count += result
    return count


if __name__ == "__main__":
    print(get_result("first", "data/2023/day12/hot_springs/sample.txt"))
    print(get_result("first", "data/2023/day12/hot_springs/sample2.txt"))
    print(get_result("first", "data/2023/day12/hot_springs/input1.txt"))
    print(get_result("second", "data/2023/day12/hot_springs/sample.txt"))
    print(get_result("second", "data/2023/day12/hot_springs/input1.txt"))
