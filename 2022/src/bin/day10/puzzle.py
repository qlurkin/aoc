import sys

def parse(filename):
    instructions = []
    with open(filename) as file:
        for line in file:
            line = line.strip()
            if len(line) > 0:
                if line.startswith("noop"):
                    instructions.append(("noop", None))
                else:
                    amount = int(line.split(' ')[1])
                    instructions.append(("addx", amount))
    return instructions

def execute(instructions):
    timeline = []
    X = 1
    for instruction, amount in instructions:
        if instruction == 'noop':
            timeline.append(X)
        else:
            timeline.append(X)
            timeline.append(X)
            X += amount
    return timeline

def sprite(X):
    return [X-1, X, X+1]

def part1(filename):
    instructions = parse(filename)
    timeline = execute(instructions)
    L = [20, 60, 100, 140, 180, 220]
    res = sum([timeline[i-1]*i for i in L])

    return res

def part2(filename):
    instructions = parse(filename)
    timeline = execute(instructions)
    print(len(timeline))
    screen = ''
    for i, X in enumerate(timeline):
        i = i%40

        if i in sprite(X):
            screen+='#'
        else:
            screen+='.'

        if i == 39:
            screen+='\n'

    return screen


if __name__ == "__main__":
    part = int(sys.argv[1])
    filename = sys.argv[2]
    if part == 1:
        print(part1(filename))
    if part == 2:
        print(part2(filename))

