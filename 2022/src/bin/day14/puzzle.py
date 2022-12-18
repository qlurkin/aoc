import sys

def parse(filename):
    with open(filename) as file:
        rocks = set()
        for line in file:
            line = line.strip()
            if len(line) > 0:
                points = [[int(x) for x in point.split(',')] for point in line.split(' -> ')]
                for i in range(len(points)-1):
                    cx, cy = points[i]
                    print(cx, cy)
                    nx, ny = points[i+1]
                    print(nx, ny)
                    print()
                    for x in range(min(cx, nx), max(cx, nx)+1):
                        for y in range(min(cy, ny), max(cy, ny)+1):
                            rocks.add((x, y))
    return rocks

def add(A, B):
    return tuple(a + b for a, b in zip(A, B))

class Abyss(Exception):
    def __init__(self, pos):
        self.pos = pos

def simulate(start, rocks, sands):
    limit = max(y for _, y in rocks)
    print(rocks)
    print(limit)
    pos = start
    rest = False
    dirs = [(0, 1), (-1, 1), (1, 1), (0, 0)]
    while not rest:
        for dir in dirs:
            next = add(pos, dir)
            if next not in rocks and next not in sands:
                break
        print(pos, next)
        rest = pos == next
        pos = next
        if pos[1] > limit:
            raise Abyss(pos)
    sands.add(pos)

def part1(filename):
    rocks = parse(filename)
    sands = set()
    count = 0
    try:
        while True:
            simulate((500, 0), rocks, sands)
            count += 1
    except Abyss:
        pass

    return count

def part2(filename):
    rocks = parse(filename)
    sands = set()
    count = 0
    while True:
        try:
            simulate((500, 0), rocks, sands)
            count += 1
        except Abyss as e:
            count += 1
            sands.add(e.pos)
        if (500, 0) in sands:
            break

    return count


if __name__ == "__main__":
    part = int(sys.argv[1])
    filename = sys.argv[2]
    if part == 1:
        print(part1(filename))
    if part == 2:
        print(part2(filename))

