import sys

dirs = {
    "^": (-1, 0),
    ">": (0, 1),
    "<": (0, -1),
    "v": (1, 0),
}

turns = {
    "^": ">",
    ">": "v",
    "<": "^",
    "v": "<",
}


def findGuard(map):
    for r in range(len(map)):
        for c in range(len(map[r])):
            if map[r][c] in dirs:
                return (r, c), map[r][c]
    raise Exception("No gard")


def parse(filename):
    map = []
    with open(filename) as file:
        for line in file:
            map.append(list(line.strip()))
    return map


class GuardOut(Exception):
    pass


def next(pos, dir, map):
    front = pos[0] + dirs[dir][0], pos[1] + dirs[dir][1]
    if is_out(front, map):
        raise GuardOut()
    if map[front[0]][front[1]] == "#":
        return pos, turns[dir]
    return front, dir


def is_out(gardPos, map):
    height = len(map)
    width = len(map[0])
    r, c = gardPos
    return c < 0 or c >= width or r < 0 or r >= height


def show(map):
    for line in map:
        print(" ".join(line))


def trace(pos, dir, map):
    positions = set()
    while True:
        try:
            positions.add(pos)
            pos, dir = next(pos, dir, map)
        except GuardOut:
            break
    return positions


def part1(filename):
    map = parse(filename)
    pos, dir = findGuard(map)
    positions = trace(pos, dir, map)
    return len(positions)


def part2(filename):
    map = parse(filename)
    pos_initial, dir_initial = findGuard(map)
    positions = trace(pos_initial, dir_initial, map)
    loops = 0
    for obstacle in positions:
        map[obstacle[0]][obstacle[1]] = "#"
        states = set()
        pos = pos_initial
        dir = dir_initial
        while True:
            try:
                pos, dir = next(pos, dir, map)
                if (pos, dir) in states:
                    loops += 1
                    break
                states.add((pos, dir))
            except GuardOut:
                break

        map[obstacle[0]][obstacle[1]] = "."

    return loops


if __name__ == "__main__":
    part = int(sys.argv[1])
    filename = sys.argv[2]
    if part == 1:
        print(part1(filename))
    if part == 2:
        print(part2(filename))
