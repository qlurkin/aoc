import sys

N = 0
S = 1
W = 2
E = 3

order = [N, S, W, E]

directions = {
    N: (-1, 0),
    S: (1, 0),
    W: (0, -1),
    E: (0, 1),
}

sides = {
    N: [(-1, -1), (-1, 0), (-1, 1)],
    S: [(1, -1), (1, 0), (1, 1)],
    W: [(-1, -1), (0, -1), (1, -1)],
    E: [(-1, 1), (0, 1), (1, 1)],
}

opposite = {
    N: S,
    S: N,
    W: E,
    E: W
}

neighbours = [(-1, -1), (-1, 0), (-1, 1), (1, -1), (1, 0), (1, 1), (0, -1), (0, 1)]

def add(A, B):
    return tuple(a+b for a, b in zip(A, B))

def parse(filename):
    with open(filename) as file:
        elves = set()
        for i, line in enumerate(file):
            line = line.strip()
            for j, c in enumerate(line):
                if c == '#':
                    elves.add((i, j))
    return elves
        
def to_matrix(elves):
    lmin = min(l for l, c in elves)
    lmax = max(l for l, c in elves)
    cmin = min(c for l, c in elves)
    cmax = max(c for l, c in elves)

    matrix = []
    for l in range(lmin, lmax+1):
        matrix.append([])
        for c in range(cmin, cmax+1):
            if (l, c) in elves:
                matrix[l-lmin].append('#')
            else:
                matrix[l-lmin].append('.')
    return matrix

def print_matrix(matrix):
    print('\n'.join(''.join(line) for line in matrix))


def part1(filename):
    elves = parse(filename)
    print(elves)
    print_matrix(to_matrix(elves))
    for _ in range(10):
        propositions = {}
        elves_proposition = {}
        for elve in elves:
            proposition = None
            if len({add(elve, p) for p in neighbours} & elves) > 0:
                for dir in order:
                    if len({add(elve, p) for p in sides[dir]} & elves) == 0:
                        proposition = add(elve, directions[dir])
                        break
            if proposition is not None:
                elves_proposition[elve] = proposition
                if proposition not in propositions:
                    propositions[proposition] = set()
                propositions[proposition].add(elve)
        for elve, proposition in elves_proposition.items():
            if len(propositions[proposition]) == 1:
                elves.remove(elve)
                elves.add(proposition)
        dir = order.pop(0)
        order.append(dir)
    print(elves)
    matrix = to_matrix(elves)
    print_matrix(matrix)
    return sum(line.count('.') for line in matrix)

def part2(filename):
    elves = parse(filename)
    print(elves)
    print_matrix(to_matrix(elves))
    count = None
    rounds = 0
    while count != 0:
        count = 0
        propositions = {}
        elves_proposition = {}
        for elve in elves:
            proposition = None
            if len({add(elve, p) for p in neighbours} & elves) > 0:
                for dir in order:
                    if len({add(elve, p) for p in sides[dir]} & elves) == 0:
                        proposition = add(elve, directions[dir])
                        break
            if proposition is not None:
                elves_proposition[elve] = proposition
                if proposition not in propositions:
                    propositions[proposition] = set()
                propositions[proposition].add(elve)
        for elve, proposition in elves_proposition.items():
            if len(propositions[proposition]) == 1:
                elves.remove(elve)
                elves.add(proposition)
                count += 1
        dir = order.pop(0)
        order.append(dir)
        rounds += 1
    print(elves)
    matrix = to_matrix(elves)
    print_matrix(matrix)
    return rounds


if __name__ == "__main__":
    part = int(sys.argv[1])
    filename = sys.argv[2]
    if part == 1:
        print(part1(filename))
    if part == 2:
        print(part2(filename))

