def read_input(file_path):
    with open(file_path) as file:
        return file.read()


def parse_input(content):
    cards = content.split("\n")
    all_numbers = [parse_card(card) for card in cards]
    return all_numbers


def parse_card(card):
    winning_numbers = [
        int(number)
        for number in card.split(":")[1].strip().split("|")[0].strip().split(" ")
        if number != ""
    ]
    my_numbers = [
        int(number)
        for number in card.split(":")[1].strip().split("|")[1].strip().split(" ")
        if number != ""
    ]
    return winning_numbers, my_numbers


def count_winning_numbers(winning_numbers, my_numbers):
    return len(set(my_numbers).intersection(set(winning_numbers)))


def calculate_score(winning_numbers, my_numbers):
    num_winning_numbers = count_winning_numbers(winning_numbers, my_numbers)
    if num_winning_numbers == 0:
        return 0
    return 2 ** (num_winning_numbers - 1)


def get_result(case: str, file_path: str):
    content = read_input(file_path)
    all_numbers = parse_input(content)
    if case == "first":
        return sum(
            calculate_score(winning_numbers, my_numbers)
            for winning_numbers, my_numbers in all_numbers
        )
    card_counters = {i: 1 for i in range(1, len(all_numbers) + 1)}
    for i, card in enumerate(all_numbers):
        card_index = i + 1
        winning_numbers, my_numbers = card
        num_winning_numbers = count_winning_numbers(winning_numbers, my_numbers)
        for j in range(
            card_index + 1,
            min(card_index + 1 + num_winning_numbers, len(all_numbers) + 1),
        ):
            card_counters[j] += card_counters[card_index]
    return sum(card_counters.values())


if __name__ == "__main__":
    print(get_result("first", "data/2023/day04/scratchcards/sample.txt"))
    print(get_result("first", "data/2023/day04/scratchcards/input1.txt"))
    print(get_result("second", "data/2023/day04/scratchcards/sample.txt"))
    print(get_result("second", "data/2023/day04/scratchcards/input1.txt"))
