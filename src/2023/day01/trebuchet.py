def get_calibration_value(calibration_document: str) -> int:
    digits = [int(char) for char in calibration_document if char.isdigit()]
    return digits[0] * 10 + digits[-1]


def read_input():
    file_path = "data/2023/day01/trebuchet/input1.txt"
    with open(file_path) as file:
        return file.read()
    pass


def get_result():
    content = read_input()
    calibration_documents = content.split("\n")
    return sum(get_calibration_value(document) for document in calibration_documents)


if __name__ == "__main__":
    print(get_result())
