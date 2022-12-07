import sys
import string

def parse(filename):
    with open(filename) as file:
        res = []
        for line in file:
            line = line.strip()
            if len(line) > 0:
                half = len(line)//2
                part1 = line[:half]
                part2 = line[half:]
                res.append((part1, part2))
        return res

def value(char):
    if char >= 'a' and char <= 'z':
        return ord(char) - ord('a') + 1
    if char >= 'A' and char <= 'Z':
        return ord(char) - ord('A') + 27


def part1(filename):
    res = 0
    for part1, part2 in parse(filename):
        part1 = set(part1)
        part2 = set(part2)
        common = part1 & part2
        common = common.pop()
        res += value(common)
    return res

def triplet(L):
    i = 0
    while i < len(L):
        yield (L[i], L[i+1], L[i+2])
        i+=3

def part2(filename):
    res = 0
    for T in triplet(parse(filename)):
        common = set(string.ascii_letters)
        for x in T:
            x = x[0] + x[1]
            x = set(x)
            common &= x
        res += value(common.pop())
    return res


if __name__ == "__main__":
    part = int(sys.argv[1])
    filename = sys.argv[2]
    if part == 1:
        print(part1(filename))
    if part == 2:
        print(part2(filename))

