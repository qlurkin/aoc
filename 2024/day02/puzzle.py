import sys


def parse(filename):
    reports = []
    with open(filename) as file:
        for line in file:
            line = line.strip().split()
            line = [int(e) for e in line]
            reports.append(line)
    return reports


def diff(report):
    res = [a - b for a, b in zip(report[:-1], report[1:])]
    return res


def inc_or_dec(diff):
    return all([diff[0] * d > 0 for d in diff[1:]])


def one_to_three(diff):
    return all([0 < abs(d) < 4 for d in diff])


def check(report):
    diffs = diff(report)
    return inc_or_dec(diffs) and one_to_three(diffs)


def part1(filename):
    reports = parse(filename)
    return sum(1 if check(report) else 0 for report in reports)


def check2(report):
    if check(report):
        return True
    for i in range(len(report)):
        cpy = list(report)
        del cpy[i]
        if check(cpy):
            return True
    return False


def part2(filename):
    reports = parse(filename)
    return sum(1 if check2(report) else 0 for report in reports)


if __name__ == "__main__":
    part = int(sys.argv[1])
    filename = sys.argv[2]
    if part == 1:
        print(part1(filename))
    if part == 2:
        print(part2(filename))
