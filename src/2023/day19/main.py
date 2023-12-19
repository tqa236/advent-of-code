from copy import deepcopy

MIN_VALUE = 1
MAX_VALUE = 4001


def read_input(file_path):
    with open(file_path) as file:
        return file.read()


def parse_input(content):
    workflows, parts = content.split("\n\n")
    workflows = {
        parse_workflow(workflow)[0]: parse_workflow(workflow)[1]
        for workflow in workflows.split("\n")
    }
    parts = [parse_part(part) for part in parts.split("\n")]
    return workflows, parts


def parse_workflow(workflow):
    name = workflow.split("{")[0]
    rules = workflow.split("{")[1][:-1].split(",")
    return name, parse_rule(rules)


def parse_part(part):
    variables = part[1:-1].split(",")
    return {value.split("=")[0]: int(value.split("=")[1]) for value in variables}


def parse_rule(rules):
    parsed_rules = []
    for i, rule in enumerate(rules[:-1]):
        condition = rule.split(":")[0]
        destination = rule.split(":")[1]
        parsed_rules.append((condition, destination))
    parsed_rules.append(rules[-1])
    return parsed_rules


def evaluate_rule(part, rules):
    for rule in rules[:-1]:
        if eval(rule[0], {}, part):
            return rule[1]
    return rules[-1]


def evaluate_part(part, workflows):
    outcome = None
    workflow_name = "in"
    while outcome not in ("A", "R"):
        outcome = evaluate_rule(part, workflows[workflow_name])
        workflow_name = outcome
    return outcome


def split_range(valid_range, workflows, workflow_name, rule_id):
    rule = workflows[workflow_name][rule_id]
    valid_range1 = deepcopy(valid_range)
    valid_range2 = deepcopy(valid_range)
    if isinstance(rule, str):
        return rule
    destination = rule[1]
    rule = rule[0]
    if "<" in rule:
        category = rule.split("<")[0]
        value = int(rule.split("<")[1])
        valid_range1[category] = (valid_range1[category][0], value)
        valid_range2[category] = (value, valid_range2[category][1])
        full_range1 = (valid_range1, destination, 0)
        full_range2 = (valid_range2, workflow_name, rule_id + 1)
    if ">" in rule:
        category = rule.split(">")[0]
        value = int(rule.split(">")[1])
        valid_range1[category] = (valid_range1[category][0], value + 1)
        valid_range2[category] = (value + 1, valid_range2[category][1])
        full_range1 = (valid_range1, workflow_name, rule_id + 1)
        full_range2 = (valid_range2, destination, 0)
    return [full_range1, full_range2]


def count_range(valid_range):
    count = 1
    for value in valid_range.values():
        count *= max(value[1] - value[0], 0)
    return count


def get_result(case: str, file_path: str):
    content = read_input(file_path)
    workflows, parts = parse_input(content)
    if case == "first":
        return sum(
            sum(part.values())
            for part in parts
            if evaluate_part(part, workflows) == "A"
        )
    valid_range = {
        "x": (MIN_VALUE, MAX_VALUE),
        "m": (MIN_VALUE, MAX_VALUE),
        "a": (MIN_VALUE, MAX_VALUE),
        "s": (MIN_VALUE, MAX_VALUE),
    }
    valid_ranges = []

    workflow_name = "in"
    rule_id = 0
    all_ranges = [(valid_range, workflow_name, rule_id)]
    while all_ranges:
        current_range, workflow_name, rule_id = all_ranges.pop(0)
        current_range = deepcopy(current_range)
        result = split_range(current_range, workflows, workflow_name, rule_id)
        if not isinstance(result, list):
            result = [(current_range, result, 0)]
        for i in result:
            if i[1] == "A":
                valid_ranges.append(i[0])
            elif i[1] != "R":
                all_ranges.append(i)
    return sum(count_range(valid_range) for valid_range in valid_ranges)


if __name__ == "__main__":
    print(get_result("first", "data/2023/day19/sample.txt"))
    print(get_result("first", "data/2023/day19/input1.txt"))
    print(get_result("second", "data/2023/day19/sample.txt"))
    print(get_result("second", "data/2023/day19/input1.txt"))
