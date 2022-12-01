import sys

def parse(filename):
    with open(filename) as file:
        elves = []
        elve = 0
        for line in file:
            line = line.strip()
            if len(line) == 0:
                elves.append(elve)
                elve = 0
            else:
                elve += int(line)
    return elves

def part1(filename):
    return max(parse(filename))

def part2(filename):
    return sum(list(reversed(sorted(parse(filename))))[:3])


if __name__ == "__main__":
    part = int(sys.argv[1])
    filename = sys.argv[2]
    if part == 1:
        print(part1(filename))
    if part == 2:
        print(part2(filename))

