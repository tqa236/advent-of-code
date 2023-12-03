def get_full_number(row: str, index: int):
    last_index = index
    while last_index < len(row) and row[last_index].isdigit():
        last_index += 1
    return last_index - 1


def get_row_number_locations(row: str, row_index: int):
    locations = []
    last_index = -1
    for i in range(len(row)):
        if i <= last_index:
            continue
        if row[i].isdigit():
            last_index = get_full_number(row, i)
            locations.append((row_index, i, last_index))
    return locations


def get_number_locations(matrix):
    locations = []
    for i, row in enumerate(matrix):
        locations += get_row_number_locations(row, i)
    return locations


def get_valid_coordinates(
    row_index, first_column_index, last_column_index, row_length, column_length
):
    number_coordinates = {
        (row_index, column)
        for column in range(first_column_index, last_column_index + 1)
    }
    all_coordinates = {
        (row, column)
        for row in range(max(0, row_index - 1), min(row_index + 2, row_length))
        for column in range(
            max(0, first_column_index - 1), min(last_column_index + 2, column_length)
        )
    }
    return all_coordinates - number_coordinates


def is_next_to_symbol(matrix, number_location):
    row_length = len(matrix)
    column_length = len(matrix[0])
    row_index, first_column_index, last_column_index = number_location
    valid_coordinates = get_valid_coordinates(
        row_index, first_column_index, last_column_index, row_length, column_length
    )
    return any(
        (
            matrix[valid_coordinate[0]][valid_coordinate[1]] != "."
            and not matrix[valid_coordinate[0]][valid_coordinate[1]].isdigit()
        )
        for valid_coordinate in valid_coordinates
    )


def get_gear_locatio(matrix):
    row_length = len(matrix)
    column_length = len(matrix[0])

    return {
        (row, column)
        for row in range(row_length)
        for column in range(column_length)
        if matrix[row][column] == "*"
    }


def read_input(file_path):
    with open(file_path) as file:
        return file.read()


def get_result(case: str, file_path: str):
    content = read_input(file_path)
    matrix = content.split("\n")
    row_length = len(matrix)
    column_length = len(matrix[0])

    number_locations = get_number_locations(matrix)

    if case == "first":
        return sum(
            int(matrix[row_index][first_column_index : last_column_index + 1])
            for row_index, first_column_index, last_column_index in number_locations
            if is_next_to_symbol(
                matrix, (row_index, first_column_index, last_column_index)
            )
        )

    gear_locations = get_gear_locatio(matrix)
    gear_numbers = {}
    for number_location in number_locations:
        row_index, first_column_index, last_column_index = number_location
        valid_coordinates = get_valid_coordinates(
            row_index, first_column_index, last_column_index, row_length, column_length
        )
        valid_gear = gear_locations.intersection(valid_coordinates)
        for gear in valid_gear:
            if gear in gear_numbers:
                gear_numbers[gear].append(
                    int(matrix[row_index][first_column_index : last_column_index + 1])
                )
            else:
                gear_numbers[gear] = [
                    int(matrix[row_index][first_column_index : last_column_index + 1])
                ]
    return sum(
        gear_numbers[gear_location][0] * gear_numbers[gear_location][1]
        for gear_location in gear_numbers
        if len(gear_numbers[gear_location]) == 2
    )


if __name__ == "__main__":
    print(get_result("first", "data/2023/day03/gear_ratios/sample.txt"))
    print(get_result("first", "data/2023/day03/gear_ratios/input1.txt"))
    print(get_result("second", "data/2023/day03/gear_ratios/sample.txt"))
    print(get_result("second", "data/2023/day03/gear_ratios/input1.txt"))
