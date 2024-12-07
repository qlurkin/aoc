import sys

operations = [
    lambda a, b: a + b,
    lambda a, b: a * b,
]

operations2 = [
    lambda a, b: a + b,
    lambda a, b: a * b,
    lambda a, b: int(str(a) + str(b)),
]


def parse(filename):
    equations = []
    with open(filename) as file:
        for line in file:
            result, numbers = line.strip().split(": ")
            result = int(result)
            numbers = numbers.split(" ")
            numbers = list(map(int, numbers))
            equations.append((result, numbers))
    return equations


def is_ok(res, state, nums, operations):
    if len(nums) == 0:
        return res == state
    ok = False
    for op in operations:
        ok = ok or is_ok(res, op(state, nums[0]), nums[1:], operations)
        if ok:
            break
    return ok


def part1(filename):
    equations = parse(filename)
    out = 0
    for eq in equations:
        res, nums = eq
        state = nums[0]
        if is_ok(res, state, nums[1:], operations):
            out += res
    return out


def part2(filename):
    equations = parse(filename)
    out = 0
    for eq in equations:
        res, nums = eq
        state = nums[0]
        if is_ok(res, state, nums[1:], operations2):
            out += res
    return out


if __name__ == "__main__":
    part = int(sys.argv[1])
    filename = sys.argv[2]
    if part == 1:
        print(part1(filename))
    if part == 2:
        print(part2(filename))
