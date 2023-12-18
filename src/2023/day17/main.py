from enum import Enum
from heapq import heappop, heappush

MIN_DISTANCE = 1e9


class Direction(Enum):
    NORTH = (-1, 0)
    EAST = (0, 1)
    SOUTH = (1, 0)
    WEST = (0, -1)

    def turn_clockwise(self):
        new_direction = Direction((self.value[1], -self.value[0]))
        return new_direction

    def turn_counter_clockwise(self):
        new_direction = Direction((-self.value[1], self.value[0]))
        return new_direction


class Graph:
    def __init__(self, matrix):
        self.matrix = matrix
        self.row = len(matrix)
        self.column = len(matrix[0])
        self.positions = [(i, j) for i in range(self.row) for j in range(self.column)]
        self.visited = set()
        self.distance = {
            position: {
                direction: [MIN_DISTANCE, MIN_DISTANCE, MIN_DISTANCE]
                for direction in Direction
            }
            for position in self.positions
        }

    def get_neighbor(self, position):
        neighbors = []
        if not position[0] < 1:
            neighbors.append((position[0] - 1, position[1]))
        if not position[0] >= self.row - 1:
            neighbors.append((position[0] + 1, position[1]))
        if not position[1] < 1:
            neighbors.append((position[0], position[1] - 1))
        if not position[0] >= self.column - 1:
            neighbors.append((position[0], position[1] + 1))
        return neighbors

    def get_direction(self, position):
        directions = []
        if not position[0] < 1:
            directions.append(Direction.NORTH)
        if not position[0] >= self.row - 1:
            directions.append(Direction.SOUTH)
        if not position[1] < 1:
            directions.append(Direction.WEST)
        if not position[1] >= self.column - 1:
            directions.append(Direction.EAST)
        return set(directions)

    def get_valid_move(self, position, direction, step):
        valid_directions_from_direction = set(
            [
                direction,
                direction.turn_clockwise(),
                direction.turn_counter_clockwise(),
            ]
        )
        valid_directions_from_position = self.get_direction(position)
        valid_directions = valid_directions_from_direction.intersection(
            valid_directions_from_position
        )
        if step == 2 and direction in valid_directions:
            valid_directions.remove(direction)
        return valid_directions

    def get_min_cost(self, position, step, new_direction):
        distance = self.distance[position]
        # print("get_min_cost")
        # print(distance)
        # print(position, step, new_direction)
        cost_same_direction = MIN_DISTANCE
        if new_direction is not None:
            cost_same_direction = min(
                distance[new_direction][step + 1 :] + [MIN_DISTANCE]
            )
        cost_different_direction = min(
            min(distance[d]) for d in Direction if d != new_direction
        )
        return min(cost_same_direction, cost_different_direction)

    def update_cost(self, position, new_position, new_direction):
        for d in Direction:
            pass

    def traverse(self, start):
        self.distance[start] = {direction: [0, 0, 0] for direction in Direction}
        directions = self.get_direction(start)
        queue = [(start, direction, 0) for direction in directions]
        while queue:
            position, direction, step = queue.pop(0)
            print(position, direction, step)
            valid_directions = self.get_valid_move(position, direction, step)
            if step == 2:
                print(valid_directions)
            for new_direction in valid_directions:
                new_position = move(position, new_direction)
                add_new_position = False
                cost = self.get_min_cost(position, step, new_direction)
                new_cost = cost + self.matrix[new_position[0]][new_position[1]]
                for d in Direction:
                    if d == new_direction:
                        for s in range(step + 1, 3):
                            if s < 0 or s >= 3:
                                continue
                            if new_cost < self.distance[new_position][d][s]:
                                self.distance[new_position][d][s] = new_cost
                                add_new_position = True
                    else:
                        for s in range(3):
                            if new_cost < self.distance[new_position][d][s]:
                                self.distance[new_position][d][s] = new_cost
                                add_new_position = True
                if add_new_position:
                    new_step = step + 1 if new_direction == direction else 0
                    queue.append((new_position, new_direction, new_step))


def move(position, direction):
    return position[0] + direction.value[0], position[1] + direction.value[1]


def read_input(file_path):
    with open(file_path) as file:
        return file.read()


def parse_input(content):
    return [[int(i) for i in row] for row in content.split("\n")]


def get_result(case: str, file_path: str):
    content = read_input(file_path)
    matrix = parse_input(content)
    graph = Graph(matrix)
    # print(graph.row, graph.column)
    graph.traverse((0, 0))
    for key, value in graph.distance.items():
        print(key)
        print(value)
    return graph.get_min_cost((graph.row - 1, graph.column - 1), None, None)


if __name__ == "__main__":
    # print(get_result("first", "data/2023/day17/sample.txt"))
    print(get_result("first", "data/2023/day17/sample2.txt"))
    # print(get_result("first", "data/2023/day17/input1.txt"))
    # print(get_result("second", "data/2023/day17/sample.txt"))
    # print(get_result("second", "data/2023/day17/input1.txt"))
