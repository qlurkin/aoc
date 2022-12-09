import sys
from dataclasses import dataclass

def parse(filename):
    moves = []
    with open(filename) as file:
        for line in file:
            line = line.strip()
            if len(line) > 0:
                direction, count = line.split(' ')
                for i in range(int(count)):
                    moves.append(direction)
    return moves

directions = {
    'R': (0, 1),
    'L': (0, -1),
    'U': (-1, 0),
    'D': (1, 0)
}

def add(A, B):
    return tuple(a + b for a, b in zip(A, B))

def is_touching(A, B):
    return sum((a - b)**2 for a, b in zip(A, B)) < 2.25

def tail_catch_up(head, tail):
    head_line, head_column = head
    tail_line, tail_column = tail

    if is_touching(head, tail):
        return tail

    if tail_line < head_line:
        tail_line += 1
    elif tail_line > head_line:
        tail_line -= 1

    if tail_column < head_column:
        tail_column += 1
    elif tail_column > head_column:
        tail_column -= 1

    tail = (tail_line, tail_column)
    return tail

def part1(filename):
    moves = parse(filename)
    head = (0, 0)
    tail = (0, 0)
    positions = { tail }
    for move in moves:
        head = add(head, directions[move])
        tail = tail_catch_up(head, tail)
        positions.add(tail)
    return len(positions)

def part2(filename):
    moves = parse(filename)
    rope = [(0, 0)]*10
    positions = { rope[-1] }
    for move in moves:
        rope[0] = add(rope[0], directions[move])
        for i in range(1, len(rope)):
            rope[i] = tail_catch_up(rope[i-1], rope[i])
        positions.add(rope[-1])
    return len(positions)


if __name__ == "__main__":
    part = int(sys.argv[1])
    filename = sys.argv[2]
    if part == 1:
        print(part1(filename))
    if part == 2:
        print(part2(filename))

