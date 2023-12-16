from dataclasses import dataclass
from enum import Enum
import itertools


@dataclass
class position:
    x: int
    y: int


class Direction(Enum):
    NORTH = (-1, 0)
    EAST = (0, 1)
    SOUTH = (1, 0)
    WEST = (0, -1)

    def turn_clockwise(self):
        # Turning clockwise by swapping x and y and negating the new x
        new_direction = Direction((self.value[1], -self.value[0]))
        return new_direction

    def turn_counter_clockwise(self):
        # Turning counter-clockwise by swapping x and y and negating the new y
        new_direction = Direction((-self.value[1], self.value[0]))
        return new_direction


@dataclass
class Beam:
    position: tuple
    direction: Direction


def read_input(file_path):
    with open(file_path) as file:
        return file.read()


def parse_input(content):
    return content.split("\n")


def move(position, direction):
    return position[0] + direction.value[0], position[1] + direction.value[1]


def traverse(position, direction, matrix):
    symbol = matrix[position[0]][position[1]]
    if symbol == ".":
        new_direction = direction
    if symbol == "/":
        if direction in (Direction.NORTH, Direction.SOUTH):
            new_direction = direction.turn_clockwise()
        if direction in (Direction.EAST, Direction.WEST):
            new_direction = direction.turn_counter_clockwise()
    if symbol == "\\":
        if direction in (Direction.NORTH, Direction.SOUTH):
            new_direction = direction.turn_counter_clockwise()
        if direction in (Direction.EAST, Direction.WEST):
            new_direction = direction.turn_clockwise()
    if symbol == "-":
        if direction in (Direction.EAST, Direction.WEST):
            new_direction = direction
        if direction in (Direction.NORTH, Direction.SOUTH):
            return [
                Beam(move(position, Direction.EAST), Direction.EAST),
                Beam(move(position, Direction.WEST), Direction.WEST),
            ]
    if symbol == "|":
        if direction in (Direction.NORTH, Direction.SOUTH):
            new_direction = direction
        if direction in (Direction.EAST, Direction.WEST):
            return [
                Beam(move(position, Direction.NORTH), Direction.NORTH),
                Beam(move(position, Direction.SOUTH), Direction.SOUTH),
            ]
    new_position = move(position, new_direction)
    return Beam(new_position, new_direction)


def out_of_bound(beam, matrix):
    if beam.position[0] < 0 or beam.position[0] >= len(matrix):
        return True
    if beam.position[1] < 0 or beam.position[1] >= len(matrix[0]):
        return True
    return False


def visit_matrix(starting_beam, matrix):
    visited = [[0 for j in range(len(matrix[0]))] for i in range(len(matrix))]
    caches = set()
    beams = [starting_beam]
    while beams:
        beam = beams.pop(0)
        if (beam.position, beam.direction) in caches:
            continue
        if not out_of_bound(beam, matrix):
            visited[beam.position[0]][beam.position[1]] = 1
            new_beams = traverse(beam.position, beam.direction, matrix)
            if not isinstance(new_beams, list):
                new_beams = [new_beams]
            for new_beam in new_beams:
                if not out_of_bound(new_beam, matrix):
                    beams.append(new_beam)
        caches.add((beam.position, beam.direction))
    return sum(sum(i) for i in visited)


def get_result(case: str, file_path: str):
    content = read_input(file_path)
    matrix = parse_input(content)
    if case == "first":
        starting_beam = Beam((0, 0), Direction.EAST)
        return visit_matrix(starting_beam, matrix)
    starting_beams = (
        [Beam((0, i), Direction.SOUTH) for i in range(len(matrix[0]))]
        + [Beam((len(matrix) - 1, i), Direction.NORTH) for i in range(len(matrix[0]))]
        + [Beam((i, 0), Direction.EAST) for i in range(len(matrix))]
        + [Beam((i, len(matrix[0]) - 1), Direction.WEST) for i in range(len(matrix))]
    )
    return max(visit_matrix(starting_beam, matrix) for starting_beam in starting_beams)


if __name__ == "__main__":
    print(get_result("first", "data/2023/day16/lava_floor/sample.txt"))
    print(get_result("first", "data/2023/day16/lava_floor/input1.txt"))
    print(get_result("second", "data/2023/day16/lava_floor/sample.txt"))
    print(get_result("second", "data/2023/day16/lava_floor/input1.txt"))
