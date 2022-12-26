import sys
import math
from collections import defaultdict

def snafu2int(snafu):
    base = 5
    value = 0
    for i, c in enumerate(reversed(snafu)):
        value += math.pow(base, i)*values[c]
    return int(value)


def int2snafu(value):
    b5 = []
    while value > 0:
        value, r = divmod(value, 5)
        b5.append(r)
    res = ''
    # b5 = list(reversed(b5))
    b5 = defaultdict(lambda : 0, {i:v for i, v in enumerate(b5)})
    i = 0
    while i < len(b5):
        v = b5[i]
        if v == 1:
            res += '1'
        elif v == 2:
            res += '2'
        elif v == 0:
            res += '0'
        elif v == 3:
            b5[i+1] += 1
            res += '='
        elif v == 4:
            b5[i+1] += 1
            res += '-'
        elif v == 5:
            b5[i+1] += 1
            res += '0'
        else:
            raise Exception('CACA')
        i += 1
    return ''.join(reversed(res))


def parse(filename):
    res = []
    with open(filename) as file:
        for line in file:
            line = line.strip()
            if len(line) > 0:
                res.append(line)
    return res

values = {
    '1': 1,
    '2': 2,
    '0': 0,
    '-': -1,
    '=': -2,
}

def part1(filename):
    print(snafu2int('1=-0-2'))
    print(int2snafu(1747))
    print(int2snafu(906))
    snafus = parse(filename)
    return int2snafu(sum(snafu2int(v) for v in snafus))

def part2(filename):
    return ''


if __name__ == "__main__":
    part = int(sys.argv[1])
    filename = sys.argv[2]
    if part == 1:
        print(part1(filename))
    if part == 2:
        print(part2(filename))

