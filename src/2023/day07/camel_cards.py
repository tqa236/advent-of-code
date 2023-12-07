from dataclasses import dataclass
from collections import Counter
from functools import total_ordering

CARD_TYPES = [str(i) for i in range(2, 10)] + ["T", "J", "Q", "K", "A"]
CARD_TYPES2 = ["J"] + [str(i) for i in range(2, 10)] + ["T", "Q", "K", "A"]
HAND_TYPES = [
    "high_card",
    "one_pair",
    "two_pair",
    "three_of_a_kind",
    "full_house",
    "five_of_a_kind",
]


@total_ordering
@dataclass
class Game:
    hand: Counter
    bid: int
    hand_str: tuple
    case: str

    def __eq__(self, other):
        return (
            get_hand_signature(self.hand, self.case)
            == get_hand_signature(other.hand, self.case)
            and self.hand_str == other.hand_str
        )

    def __lt__(self, other):
        if compare_quantity(
            get_hand_signature(self.hand, self.case),
            get_hand_signature(other.hand, self.case),
        ):
            return compare_hand_str(self.hand_str, other.hand_str, self.case)
        return compare_signature(
            get_hand_signature(self.hand, self.case),
            get_hand_signature(other.hand, self.case),
        )


def read_input(file_path):
    with open(file_path) as file:
        return file.read()


def parse_input(case, content):
    games = [
        Game(
            Counter(game.split(" ")[0]),
            int(game.split(" ")[1]),
            tuple(game.split(" ")[0]),
            case,
        )
        for game in content.split("\n")
    ]
    return games


def get_hand_signature(hand, case):
    signature = []
    joker = 0
    for card, count in hand.items():
        if case == "second":
            if card == "J":
                joker = count
                continue
        signature.append((count, CARD_TYPES.index(card)))
    if not signature:
        return ((5, CARD_TYPES.index("A")),)
    signature = sorted(signature, reverse=True)
    signature[0] = (signature[0][0] + joker, signature[0][1])
    return tuple(signature)


def compare_signature(left, right):
    left_quantity = tuple([i[0] for i in left])
    right_quantity = tuple([i[0] for i in right])
    return left_quantity < right_quantity


def compare_quantity(left, right):
    left_quantity = sorted([i[0] for i in left])
    right_quantity = sorted([i[0] for i in right])
    return left_quantity == right_quantity


def compare_hand_str(left, right, case):
    if case == "first":
        card_types = CARD_TYPES
    else:
        card_types = CARD_TYPES2
    for i, j in zip(left, right):
        if card_types.index(i) < card_types.index(j):
            return True
        elif card_types.index(i) > card_types.index(j):
            return False


def get_result(case: str, file_path: str):
    content = read_input(file_path)
    games = parse_input(case, content)
    games = sorted(games)
    return sum((i + 1) * game.bid for i, game in enumerate(games))


if __name__ == "__main__":
    print(get_result("first", "data/2023/day07/camel_cards/sample.txt"))
    print(get_result("first", "data/2023/day07/camel_cards/input1.txt"))
    print(get_result("second", "data/2023/day07/camel_cards/sample.txt"))
    print(get_result("second", "data/2023/day07/camel_cards/input1.txt"))
