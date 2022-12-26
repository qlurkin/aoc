import sys
from dataclasses import dataclass
from functools import cache

@dataclass(frozen=True)
class Blizzard:
    pos: tuple[int, int]
    dir: tuple[int, int]


class Queue:
	def __init__(self):
		self.data = []

	def enqueue(self, value):
		self.data.append(value)

	def dequeue(self):
		return self.data.pop(0)

def BFS(start, successors, is_goal):
	q = Queue()
	parent = {}
	parent[start] = None
	node = start
	while not is_goal(node):
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

def make_successors(get_blizzards, width, height):
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (0, 0)]
    
    @cache
    def get_occupancy(time):
        blizzards = get_blizzards(time)
        return {blizzard.pos for blizzard in blizzards}

    def successors(node):
        res = []
        pos, time = node
        l, c = pos
        for dl, dc in directions:
            nl = l + dl
            nc = c + dc
            if (nl >= 0 and nl < height and nc >= 0 and nc < width) or (nl, nc) == (-1, 0) or (nl, nc) == (height, width-1):
                if (nl, nc) not in get_occupancy(time+1):
                    res.append(((nl, nc), time+1))
        return res
    return successors

def parse(filename):
    lines = []
    with open(filename) as file:
        for line in file:
            line = line.strip()
            if len(line) > 0:
                lines.append(line[1:-1])
    lines = lines[1:-1]
    blizzards = []
    for i in range(len(lines)):
        for j in range(len(lines[i])):
            if lines[i][j] != '.':
                blizzards.append(Blizzard((i, j), directions[lines[i][j]]))    
    return blizzards, len(lines[0]), len(lines)

def add(A, B):
    return tuple(a+b for a, b in zip(A, B))

directions = {
    '<': (0, -1),
    '>': (0, 1),
    'v': (1, 0),
    '^': (-1, 0),
}

def make_get_blizzards(blizzards0, width, height):
    @cache
    def get_blizzards(time):
        # if time < len(cache):
            # return cache[time]
        if time == 0:
            return blizzards0

        prev = get_blizzards(time-1)
        next = []
        for blizzard in prev:
            next_pos = add(blizzard.pos, blizzard.dir)
            next_pos = (next_pos[0]%height, next_pos[1]%width)
            next.append(Blizzard(next_pos, blizzard.dir))

        # cache[time] = next
        return next
    return get_blizzards

def part1(filename):
    blizzards, width, height = parse(filename)
    print(blizzards)

    get_blizzards = make_get_blizzards(blizzards, width, height)

    return BFS(((-1, 0), 0), make_successors(get_blizzards, width, height), lambda n: n[0][0] == height and n[0][1] == width-1)

def part2(filename):
    blizzards, width, height = parse(filename)
    print(blizzards)

    get_blizzards = make_get_blizzards(blizzards, width, height)

    first = BFS(((-1, 0), 0), make_successors(get_blizzards, width, height), lambda n: n[0][0] == height and n[0][1] == width-1)
    second = BFS(first[-1], make_successors(get_blizzards, width, height), lambda n: n[0][0] == -1 and n[0][1] == 0)
    return BFS(second[-1], make_successors(get_blizzards, width, height), lambda n: n[0][0] == height and n[0][1] == width-1)


if __name__ == "__main__":
    part = int(sys.argv[1])
    filename = sys.argv[2]
    if part == 1:
        print(part1(filename))
    if part == 2:
        print(part2(filename))

