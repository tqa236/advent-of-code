TYPE_ORDERS = [
    "seed",
    "soil",
    "fertilizer",
    "water",
    "light",
    "temperature",
    "humidity",
    "location",
]


def read_input(file_path):
    with open(file_path) as file:
        return file.read()


def parse_input(case, content):
    sections = content.split("\n\n")
    seeds = parse_seed(case, sections[0])
    maps = {}
    for section in sections[1:]:
        maps.update(parse_map(section))
    return seeds, maps


def parse_seed(case, section):
    all_numbers = [int(i) for i in section.split(":")[1].strip().split(" ")]
    if case == "first":
        return all_numbers
    seeds = []
    for i in range(len(all_numbers) // 2):
        seeds.append(
            (all_numbers[2 * i], all_numbers[2 * i] + all_numbers[2 * i + 1] - 1)
        )
    return seeds


def parse_map(section):
    rows = section.split("\n")
    from_type = rows[0].split(" ")[0].split("-")[0]
    to_type = rows[0].split(" ")[0].split("-")[-1]
    type_map = {}
    for row in rows[1:]:
        destination_range_start, source_range_start, range_length = [
            int(i) for i in row.split(" ")
        ]
        type_map[
            (
                source_range_start,
                source_range_start + range_length - 1,
            )
        ] = destination_range_start

    return {(from_type, to_type): type_map}


def get_location(seed, maps):
    current_id = seed
    for i in range(len(TYPE_ORDERS) - 1):
        current_types = (TYPE_ORDERS[i], TYPE_ORDERS[i + 1])
        current_map = maps[current_types]
        for (
            source_range_start,
            source_range_end,
        ), destination_range_start in current_map.items():
            if source_range_start <= current_id <= source_range_end:
                current_id = destination_range_start + current_id - source_range_start
                break
    return current_id


def get_location2(seeds, maps):
    current_ids = seeds
    for i in range(len(TYPE_ORDERS) - 1):
        next_ids = []
        current_types = (TYPE_ORDERS[i], TYPE_ORDERS[i + 1])
        current_map = maps[current_types]
        while current_ids:
            seed_start, seed_end = current_ids.pop(0)
            for (
                source_range_start,
                source_range_end,
            ), destination_range_start in current_map.items():
                overlapped_range = (
                    max(source_range_start, seed_start),
                    min(source_range_end, seed_end),
                )
                if overlapped_range[0] <= overlapped_range[1]:
                    next_ids.append(
                        (
                            destination_range_start
                            + overlapped_range[0]
                            - source_range_start,
                            destination_range_start
                            + overlapped_range[1]
                            - source_range_start,
                        )
                    )
                    if seed_start < source_range_start:
                        current_ids.append((seed_start, source_range_start - 1))
                    if seed_end > source_range_end:
                        current_ids.append((source_range_end + 1, seed_end))
                    break
            else:
                next_ids.append((seed_start, seed_end))
        current_ids = current_ids + next_ids
    return min(current_id[0] for current_id in current_ids)


def get_result(case: str, file_path: str):
    content = read_input(file_path)
    seeds, maps = parse_input(case, content)
    if case == "first":
        return min(get_location(seed, maps) for seed in seeds)
    return get_location2(seeds, maps)


if __name__ == "__main__":
    print(get_result("first", "data/2023/day05/fertilizer/sample.txt"))
    print(get_result("first", "data/2023/day05/fertilizer/input1.txt"))
    print(get_result("second", "data/2023/day05/fertilizer/sample.txt"))
    print(get_result("second", "data/2023/day05/fertilizer/input1.txt"))
