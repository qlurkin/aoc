import sys


def parse(filename):
    with open(filename) as file:
        grid = []
        for line in file:
            grid.append(list(line.strip()))
    return grid


def part1(filename):
    word = "XMAS"
    dirs = [(1, 1), (-1, -1), (1, 0), (-1, 0), (0, 1), (0, -1), (1, -1), (-1, 1)]
    grid = parse(filename)
    res = 0
    height = len(grid)
    width = len(grid[0])
    for y in range(height):
        for x in range(width):
            if grid[y][x] == word[0]:
                for dir in dirs:
                    xc, yc = x, y
                    dx, dy = dir
                    ok = True
                    for char in word[1:]:
                        xc, yc = xc + dx, yc + dy
                        if 0 <= xc < width and 0 <= yc < height:
                            if char != grid[yc][xc]:
                                ok = False
                                break
                        else:
                            ok = False
                            break
                    if ok:
                        res += 1
    return res


def part2(filename):
    dirs = [(1, 1), (-1, -1), (-1, 1), (1, -1)]
    grid = parse(filename)
    height = len(grid)
    width = len(grid[0])
    res = 0
    for y in range(height):
        for x in range(width):
            if grid[y][x] == "A":
                ok = True
                countM = 0
                countS = 0
                for dir in dirs:
                    dx, dy = dir
                    xc, yc = x + dx, y + dy
                    if 0 <= xc < width and 0 <= yc < height:
                        if grid[yc][xc] == "M":
                            countM += 1
                        if grid[yc][xc] == "S":
                            countS += 1
                    else:
                        ok = False
                        break
                if not ok:
                    continue
                if countM != 2 or countS != 2:
                    continue
                if grid[y - 1][x - 1] == grid[y + 1][x + 1]:
                    continue
                res += 1

    return res


if __name__ == "__main__":
    part = int(sys.argv[1])
    filename = sys.argv[2]
    if part == 1:
        print(part1(filename))
    if part == 2:
        print(part2(filename))
