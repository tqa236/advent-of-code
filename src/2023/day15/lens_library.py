def read_input(file_path):
    with open(file_path) as file:
        return file.read()


def parse_input(content):
    return content.split(",")


def parse_input_string(input_string):
    if "-" in input_string:
        return ("-", input_string.split("-")[0])
    return ("=", input_string.split("=")[0], int(input_string.split("=")[1]))


def get_hash(input_string):
    value = 0
    for character in input_string:
        value += ord(character)
        value *= 17
        value = value % 256
    return value


def get_result(case: str, file_path: str):
    content = read_input(file_path)
    input_strings = parse_input(content)
    if case == "first":
        return sum(get_hash(input_string) for input_string in input_strings)
    actions = [parse_input_string(input_string) for input_string in input_strings]
    boxes = [[] for _ in range(256)]
    for action in actions:
        hash_value = get_hash(action[1])
        if action[0] == "-":
            for i, lens in enumerate(boxes[hash_value]):
                if lens[0] == action[1]:
                    del boxes[hash_value][i]
                    break
        else:
            for i, lens in enumerate(boxes[hash_value]):
                if lens[0] == action[1]:
                    boxes[hash_value][i][1] = action[2]
                    break
            else:
                boxes[hash_value].append([action[1], action[2]])
    return sum(
        (i + 1) * (j + 1) * lens[1]
        for i, box in enumerate(boxes)
        for j, lens in enumerate(box)
    )


if __name__ == "__main__":
    print(get_result("first", "data/2023/day15/lens_library/sample.txt"))
    print(get_result("first", "data/2023/day15/lens_library/input1.txt"))
    print(get_result("second", "data/2023/day15/lens_library/sample.txt"))
    print(get_result("second", "data/2023/day15/lens_library/input1.txt"))
