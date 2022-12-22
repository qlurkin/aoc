import sys

def parse(filename):
    with open(filename) as file:
        pass

def part1(filename):
    return ''

def part2(filename):
    return ''


if __name__ == "__main__":
    part = int(sys.argv[1])
    filename = sys.argv[2]
    if part == 1:
        print(part1(filename))
    if part == 2:
        print(part2(filename))

