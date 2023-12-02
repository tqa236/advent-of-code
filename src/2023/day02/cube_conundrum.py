MAX_GAME_LOAD = {"blue": 14, "green": 13, "red": 12}


def get_game_id(game):
    return int(game.split(":")[0].split(" ")[1])


def get_game_load(game):
    game_load = {"blue": 0, "green": 0, "red": 0}
    game_content = game.split(":")[1].strip()
    all_colors = [
        color_quantity.strip()
        for content in game_content.split(";")
        for color_quantity in content.split(",")
    ]
    all_choices = [
        (int(color.split(" ")[0]), color.split(" ")[1]) for color in all_colors
    ]
    for choice in all_choices:
        game_load[choice[1]] = max(game_load[choice[1]], choice[0])
    return game_load


def is_game_feasible(game):
    game_load = get_game_load(game)
    return all(game_load[color] <= MAX_GAME_LOAD[color] for color in game_load)


def read_input():
    file_path = "data/2023/day02/cube_conundrum/input1.txt"
    with open(file_path) as file:
        return file.read()


def get_result(case: str):
    content = read_input()
    games = content.split("\n")
    if case == "first":
        return sum(get_game_id(game) for game in games if is_game_feasible(game))
    game_loads = [get_game_load(game) for game in games]
    return sum(
        game_load["blue"] * game_load["green"] * game_load["red"]
        for game_load in game_loads
    )


if __name__ == "__main__":
    print(get_result("first"))
    print(get_result("second"))
