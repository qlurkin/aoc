import re
import sys

filename = sys.argv[1]


def load(filename):
    pattern = re.compile(r"\d+")
    map = []
    matches = []
    with open(filename) as file:
        for i, line in enumerate(file):
            line = line.strip()
            matches.extend([(i, match) for match in pattern.finditer(line)])
            map.append(list(line))
    return map, matches


def around(line, match):
    res = []
    res.append((line, match.start() - 1))
    res.append((line, match.end()))
    for j in range(match.start() - 1, match.end() + 1):
        res.append((line - 1, j))
        res.append((line + 1, j))
    return res


def part1():
    map, matches = load(filename)
    sum = 0
    for match in matches:
        for i, j in around(*match):
            if i >= 0 and i < len(map):
                if j >= 0 and j < len(map[i]):
                    if map[i][j] not in "0123456789.":
                        print((i, j), map[i][j], match[1].group())
                        sum += int(match[1].group())
                        break

    print(sum)


def part2():
    map, matches = load(filename)
    sum = 0
    gears = {}
    for match in matches:
        for i, j in around(*match):
            if i >= 0 and i < len(map):
                if j >= 0 and j < len(map[i]):
                    if map[i][j] == "*":
                        if (i, j) not in gears:
                            gears[i, j] = []
                        gears[i, j].append(int(match[1].group()))

    for gear in gears.values():
        if len(gear) == 2:
            sum += gear[0] * gear[1]
    print(sum)


part2()
