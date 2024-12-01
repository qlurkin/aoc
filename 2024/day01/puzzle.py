import sys
from collections import defaultdict


def parse(filename):
    with open(filename) as file:
        L1 = []
        L2 = []

        for line in file:
            item1, item2 = line.strip().split("   ")
            item1, item2 = int(item1), int(item2)
            L1.append(item1)
            L2.append(item2)

        return L1, L2


def part1(filename):
    L1, L2 = parse(filename)
    res = 0
    for v1, v2 in zip(sorted(L1), sorted(L2)):
        res += abs(v1 - v2)

    return res


def part2(filename):
    L1, L2 = parse(filename)
    counters = defaultdict(lambda: 0)

    for item in L2:
        counters[item] += 1

    res = 0
    for item in L1:
        res += item * counters[item]

    return res


if __name__ == "__main__":
    part = int(sys.argv[1])
    filename = sys.argv[2]
    if part == 1:
        print(part1(filename))
    if part == 2:
        print(part2(filename))
