import sys


def parse(filename):
    part1 = True
    wrongs = set()
    updates = []
    with open(filename) as file:
        for line in file:
            if len(line.strip()) == 0:
                part1 = False
                continue
            if part1:
                a, b = line.strip().split("|")
                wrongs.add((b, a))
            else:
                updates.append(line.strip().split(","))
    return wrongs, updates


def sort(update, wrongs):
    res = list(update)
    for j in range(len(res)):
        for i in range(len(res) - 1 - j):
            if (res[i], res[i + 1]) in wrongs:
                res[i], res[i + 1] = res[i + 1], res[i]
    return res


def part1(filename):
    wrongs, updates = parse(filename)

    res = 0
    for update in updates:
        if sort(update, wrongs) == update:
            res += int(update[len(update) // 2])
    return res


def part2(filename):
    wrongs, updates = parse(filename)

    res = 0
    for update in updates:
        sorted = sort(update, wrongs)
        if sorted != update:
            res += int(sorted[len(sorted) // 2])
    return res


if __name__ == "__main__":
    part = int(sys.argv[1])
    filename = sys.argv[2]
    if part == 1:
        print(part1(filename))
    if part == 2:
        print(part2(filename))
