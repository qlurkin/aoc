import sys
from functools import partial

def parse(filename):
    start = None
    end = None

    def find(elem, l, c):
        nonlocal start
        nonlocal end
        if elem == -14:
            start = (l, c)
            return 0
        if elem == -28:
            end = (l, c)
            return 25
        return elem

    with open(filename) as file:
        grid = file.readlines()
        grid = tuple(tuple(find(ord(char)-ord('a'), l, c) for c, char in enumerate(line.strip())) for l, line in enumerate(grid))

    return grid, start, end

class Queue:
    def __init__(self):
	    self.data = []

    def enqueue(self, value):
        self.data.append(value)

    def dequeue(self):
        return self.data.pop(0)

def BFS(start, successors, goals):
    q = Queue()
    parent = {}
    parent[start] = None
    node = start
    while node not in goals:
        for successor in successors(node):
            if successor not in parent:
                parent[successor] = node
                q.enqueue(successor)
        node = q.dequeue()
    res = []
    while node is not None:
        res.append(node)
        node = parent[node]
    return list(reversed(res))

def successors(grid, node):
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    res = []
    l, c = node
    for dl, dc in directions:
        nl = l + dl
        nc = c + dc
        if nl >= 0 and nl < len(grid) and nc >= 0 and nc < len(grid[nl]):
            if grid[nl][nc] - grid[l][c] < 2:
                res.append((nl, nc))
    return res

def part1(filename):
    grid, start, end = parse(filename)
    path = BFS(start, partial(successors, grid), [end])
    for case in path:
        print(case, grid[case[0]][case[1]])
    return len(path)-1

def part2(filename):
    grid, _, end = parse(filename)
    starts = []
    for l in range(len(grid)):
        for c in range(len(grid[l])):
            if grid[l][c] == 0:
                starts.append((l, c))
    lengths = []
    for start in starts:
        try:
            path = BFS(start, partial(successors, grid), [end])
            lengths.append(len(path)-1)
        except IndexError:
            pass
    return min(lengths)


if __name__ == "__main__":
    part = int(sys.argv[1])
    filename = sys.argv[2]
    if part == 1:
        print(part1(filename))
    if part == 2:
        print(part2(filename))

