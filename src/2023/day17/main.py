from heapq import heappop, heappush
from math import inf

LEGAL_MOVES = {
    (0, 0): ((1, 0), (0, 1)),
    (0, -1): ((1, 0), (-1, 0)),
    (1, 0): ((0, -1), (0, 1)),
    (0, 1): ((1, 0), (-1, 0)),
    (-1, 0): ((0, -1), (0, 1)),
}


def traverse(matrix: str, mmin: int, mmax: int):
    destination_coord = (len(matrix[0]) - 1, len(matrix) - 1)
    heap = [(0, (0, 0), (0, 0))]
    heat_map = {(0, 0): 0}
    visited = set()

    while heap:
        heat_loss, coord, direction = heappop(heap)

        if coord == destination_coord:
            break

        if (coord, direction) in visited:
            continue

        visited.add((coord, direction))

        for new_direction in LEGAL_MOVES[direction]:
            new_heat_loss = heat_loss
            for steps in range(1, mmax + 1):
                new_coord = (
                    coord[0] + steps * new_direction[0],
                    coord[1] + steps * new_direction[1],
                )
                if (
                    new_coord[0] < 0
                    or new_coord[1] < 0
                    or new_coord[0] > destination_coord[0]
                    or new_coord[1] > destination_coord[1]
                ):
                    continue
                new_heat_loss = new_heat_loss + matrix[new_coord[1]][new_coord[0]]
                if steps >= mmin:
                    new_node = (new_coord, new_direction)
                    if heat_map.get(new_node, inf) <= new_heat_loss:
                        continue
                    heat_map[new_node] = new_heat_loss
                    heappush(heap, (new_heat_loss, new_coord, new_direction))

    return heat_loss


def read_input(file_path):
    with open(file_path) as file:
        return file.read()


def parse_input(content):
    return [[int(i) for i in row] for row in content.split("\n")]


def get_result(case: str, file_path: str):
    content = read_input(file_path)
    matrix = parse_input(content)
    mmin, mmax = (1, 3) if case == "first" else (4, 10)
    return traverse(matrix, mmin, mmax)


if __name__ == "__main__":
    print(get_result("first", "data/2023/day17/sample.txt"))
    print(get_result("first", "data/2023/day17/sample2.txt"))
    print(get_result("first", "data/2023/day17/input1.txt"))
    print(get_result("second", "data/2023/day17/sample.txt"))
    print(get_result("second", "data/2023/day17/input1.txt"))
