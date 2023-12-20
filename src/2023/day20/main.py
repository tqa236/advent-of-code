from collections import deque
from enum import Enum
from copy import deepcopy
import math


class ModuleName(Enum):
    BROADCASTER = "broadcaster"
    FLIP_FLOP = "flip-flop"
    CONJUNCTION = "conjunction"


class Pulse(Enum):
    HIGH = True
    LOW = False

    def inverse(self):
        if self == Pulse.HIGH:
            return Pulse.LOW
        elif self == Pulse.LOW:
            return Pulse.HIGH


class Broadcaster:
    def __init__(self, name, output) -> None:
        self.name = name
        self.output = output


class FlipFlop:
    def __init__(self, name, output) -> None:
        self.name = name
        self.on = False
        self.input = None
        self.output = output

    def new_pulse(self):
        if self.on:
            return Pulse.HIGH
        return Pulse.LOW


class Conjunction:
    def __init__(self, name, output) -> None:
        self.name = name
        self.input = {}
        self.output = output
        self.cycle = None

    def update_memory(self, pulse, module_name, i):
        if pulse == Pulse.LOW:
            self.cycle = i
        self.input[module_name] = pulse

    def is_all_pulses_high(self):
        return set(self.input.values()) == set([Pulse.HIGH])

    def new_pulse(self):
        if self.is_all_pulses_high():
            return Pulse.LOW
        return Pulse.HIGH


def read_input(file_path):
    with open(file_path) as file:
        return file.read()


def parse_input(content):
    rules = content.split("\n")
    return rules


def parse_rule(rule):
    input_module = rule.split("-")[0].strip()
    output_modules = [
        module.strip() for module in rule.split(">")[1].strip().split(",")
    ]
    return input_module, output_modules


def parse_module(input_module, output_modules):
    if input_module == "broadcaster":
        return input_module, Broadcaster(input_module, output_modules)

    module_name = input_module[1:]
    if input_module.startswith("%"):
        return module_name, FlipFlop(module_name, output_modules)
    return module_name, Conjunction(module_name, output_modules)


def get_module_name(input_module):
    return input_module if input_module == "broadcaster" else input_module[1:]


def push(case, i, modules):
    signals = deque([(None, Pulse.LOW, "broadcaster")])
    counter = {Pulse.LOW: 0, Pulse.HIGH: 0}
    while signals:
        input_name, pulse, module_name = signals.popleft()
        counter[pulse] += 1
        if module_name not in modules:
            continue
        module = modules[module_name]
        if isinstance(module, Broadcaster):
            new_pulse = pulse
        if isinstance(module, FlipFlop):
            if pulse == Pulse.HIGH:
                continue
            module.on = not module.on
            new_pulse = module.new_pulse()
        if isinstance(module, Conjunction):
            module.update_memory(pulse, input_name, i)
            new_pulse = module.new_pulse()
        for output_name in module.output:
            signals.append((module_name, new_pulse, output_name))

    if case == "second":
        finish = True
        for module_name, module in modules.items():
            if module_name in ("kd", "zf", "vg", "gs"):
                if module.cycle is None:
                    finish = False
        if finish:
            return True
    return counter


def get_state(modules):
    states = []
    for module in modules.values():
        if isinstance(module, FlipFlop):
            states.append((module.name, module.on))
        if isinstance(module, Conjunction):
            states.append((module.name, tuple(module.input.values())))
    return tuple(states)


def get_result(case: str, file_path: str):
    content = read_input(file_path)
    rules = parse_input(content)
    rules = [parse_rule(rule) for rule in rules]
    modules = {}

    for rule in rules:
        input_module, output_modules = rule
        module_name, module = parse_module(input_module, output_modules)
        modules[module_name] = module

    for rule in rules:
        input_module, output_modules = rule
        input_module = get_module_name(input_module)
        for module_name in output_modules:
            if module_name not in modules:
                continue
            if isinstance(modules[module_name], FlipFlop):
                modules[module_name].input = input_module
            if isinstance(modules[module_name], Conjunction):
                modules[module_name].input[input_module] = Pulse.LOW
    if case == "first":
        caches = {}
        n_push = 1000
        all_counters = {Pulse.LOW: 0, Pulse.HIGH: 0}
        for i in range(n_push):
            state = get_state(modules)
            if state in caches:
                counter, modules = caches[state]
            else:
                counter = push(case, i, modules)
                caches[state] = counter, deepcopy(modules)
            all_counters[Pulse.LOW] += counter[Pulse.LOW]
            all_counters[Pulse.HIGH] += counter[Pulse.HIGH]
        return all_counters[Pulse.LOW] * all_counters[Pulse.HIGH]
    i = 1
    caches = {}
    while True:
        counter = push(case, i, modules)
        i += 1
        if counter is True:
            return math.lcm(
                modules["kd"].cycle,
                modules["zf"].cycle,
                modules["vg"].cycle,
                modules["gs"].cycle,
            )


if __name__ == "__main__":
    print(get_result("first", "data/2023/day20/sample.txt"))
    print(get_result("first", "data/2023/day20/sample2.txt"))
    print(get_result("first", "data/2023/day20/input1.txt"))
    print(get_result("second", "data/2023/day20/input1.txt"))
