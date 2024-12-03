import sys
import re


def parse(filename):
    with open(filename) as file:
        return file.read()


def part1(filename):
    content = parse(filename)
    pattern = re.compile(r"mul\(([0-9]{1,3},[0-9]{1,3})\)")
    res = 0
    for match in pattern.findall(content):
        a, b = match.split(",")
        res += int(a) * int(b)
    return res


def part2(filename):
    content = parse(filename)
    pattern = re.compile(r"do\(\)|don't\(\)|mul\([0-9]{1,3},[0-9]{1,3}\)")
    steps = pattern.findall(content)
    enabled = True
    res = 0
    for step in steps:
        if step == "do()":
            enabled = True
        elif step == "don't()":
            enabled = False
        else:
            if enabled:
                a, b = step[4:-1].split(",")
                res += int(a) * int(b)
    return res


if __name__ == "__main__":
    part = int(sys.argv[1])
    filename = sys.argv[2]
    if part == 1:
        print(part1(filename))
    if part == 2:
        print(part2(filename))
