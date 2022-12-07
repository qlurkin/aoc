import sys

def parse(filename):
    with open(filename) as file:
        content = file.read()
    return content

def part1(filename):
    buffer = []
    for i, char in enumerate(parse(filename)):
        buffer.append(char)
        if len(buffer) > 4:
            buffer.pop(0)
        if len(set(buffer)) == 4:
            return i+1
    return None

def part2(filename):
    buffer = []
    for i, char in enumerate(parse(filename)):
        buffer.append(char)
        if len(buffer) > 14:
            buffer.pop(0)
        if len(set(buffer)) == 14:
            return i+1
    return None


if __name__ == "__main__":
    part = int(sys.argv[1])
    filename = sys.argv[2]
    if part == 1:
        print(part1(filename))
    if part == 2:
        print(part2(filename))

