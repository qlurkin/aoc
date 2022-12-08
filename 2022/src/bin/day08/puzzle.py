import sys

def parse(filename):
    grid = []
    with open(filename) as file:
        for line in file:
            line = line.strip()
            if len(line) > 0:
                grid.append([int(c) for c in line.strip()])
    return grid

def add(A, B):
    return tuple(a + b for a, b in zip(A, B))

def is_inside(grid, pos):
    l, c = pos
    if l < 0 or l >= len(grid) or c < 0 or c >= len(grid[0]):
        return False
    return True

def is_visible_from(grid, pos, dir):
    l, c = pos
    start_height = grid[l][c]
    pos = add(pos, dir)
    while is_inside(grid, pos):
        l, c = pos
        if grid[l][c] >= start_height:
            return False
        pos = add(pos, dir)
    return True

def is_visible(grid, pos):
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    for dir in directions:
        if is_visible_from(grid, pos, dir):
            return True
    return False

def part1(filename):
    grid = parse(filename)
    count = 0
    for l in range(len(grid)):
        for c in range(len(grid[l])):
            if is_visible(grid, (l, c)):
                count += 1
    return count

def count_tree_in_dir(grid, pos, dir):
    l, c = pos
    start_height = grid[l][c]
    pos = add(pos, dir)
    count = 0
    while is_inside(grid, pos):
        l, c = pos
        if grid[l][c] >= start_height:
            count += 1
            return count
        count += 1
        pos = add(pos, dir)
    return count

def scenic_score(grid, pos):
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    score = 1
    for dir in directions:
        score *= count_tree_in_dir(grid, pos, dir)
    return score

def part2(filename):
    grid = parse(filename)
    max = 0
    for l in range(len(grid)):
        for c in range(len(grid[l])):
            score = scenic_score(grid, (l, c))
            if score > max:
                max = score
    return max

if __name__ == "__main__":
    part = int(sys.argv[1])
    filename = sys.argv[2]
    if part == 1:
        print(part1(filename))
    if part == 2:
        print(part2(filename))

