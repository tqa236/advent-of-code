DIGIT_LETTERS = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]


def get_digit(digit_letter):
    return DIGIT_LETTERS.index(digit_letter) + 1


def get_calibration_value(calibration_document: str) -> int:
    digits = [int(char) for char in calibration_document if char.isdigit()]
    return digits[0] * 10 + digits[-1]


def find_digit_with_letter(calibration_document: str, index):
    if calibration_document[index].isdigit():
        return int(calibration_document[index])
    if calibration_document[index : index + 3] in DIGIT_LETTERS:
        return get_digit(calibration_document[index : index + 3])
    if calibration_document[index : index + 4] in DIGIT_LETTERS:
        return get_digit(calibration_document[index : index + 4])
    if calibration_document[index : index + 5] in DIGIT_LETTERS:
        return get_digit(calibration_document[index : index + 5])


def get_calibration_value_with_letter(calibration_document: str) -> int:
    digits = [
        digit
        for index in range(len(calibration_document))
        if (digit := find_digit_with_letter(calibration_document, index)) is not None
    ]
    return digits[0] * 10 + digits[-1]


def read_input():
    file_path = "data/2023/day01/trebuchet/input1.txt"
    with open(file_path) as file:
        return file.read()


def get_result(case: str):
    content = read_input()
    calibration_documents = content.split("\n")
    if case == "first":
        return sum(
            get_calibration_value(document) for document in calibration_documents
        )
    return sum(
        get_calibration_value_with_letter(document)
        for document in calibration_documents
    )


if __name__ == "__main__":
    print(get_result("first"))
    print(get_result("second"))
