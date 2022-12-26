import sys
from dataclasses import dataclass

import re

def some_int(s):
    try:
        return int(s)
    except ValueError:
        return s


def parse(filename):
    pattern = re.compile(r'([RL]|[0-9]+)') 
    with open(filename) as file:
        content = file.read()

    Map, path = content.split('\n\n')
    Map = Map.split('\n')
    width = max(len(line) for line in Map)
    Map = list(map(lambda x: x+' '*(width-len(x)), Map))
    path = list(map(some_int, pattern.findall(path.strip())))

    Map = [' '*width] + Map + [' '*width]

    Map = list(map(lambda x: ' '+x+' ', Map))

    return Map, path

dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]

RIGHT = 0
DOWN = 1
LEFT = 2
UP = 3

opposite = {
    LEFT: RIGHT,
    RIGHT: LEFT,
    UP: DOWN,
    DOWN: UP,
}

def add(A, B):
    return tuple(a+b for a, b in zip(A, B))

def show_path(Map, pos, dir):
    c = ['>', 'v', '<', '^']
    Map[pos[0]] = Map[pos[0]][:pos[1]] + c[dir] +  Map[pos[0]][pos[1]+1:]
    return Map

def forward(Map, pos, dir):
    next = add(pos, dirs[dir])
    if Map[next[0]][next[1]] == '#':
        return pos
    if Map[next[0]][next[1]] == ' ':
        next = find_other_side(Map, next, dir)
        if Map[next[0]][next[1]] == '#':
            return pos
    return next

def turn(side, dir):
    if side == 'R':
        return (dir + 1) % 4
    elif side == 'L':
        return (dir - 1) % 4
    raise ValueError('CACA')

def find_other_side(Map, pos, dir):
    dir = turn('R', dir)
    dir = turn('R', dir)
    pos  = add(pos, dirs[dir])
    while Map[pos[0]][pos[1]] != ' ':
        pos  = add(pos, dirs[dir])
    dir = turn('R', dir)
    dir = turn('R', dir)
    pos  = add(pos, dirs[dir])
    return pos
        


def part1(filename):
    Map, path = parse(filename)
    print(path)
    start_j = None
    print('\n'.join(Map))
    for j, c in enumerate(Map[1]):
        if c == '.':
            start_j = j
            break
    if start_j is None:
        raise ValueError('PIPI')
    pos = (1, start_j)
    dir = RIGHT
    for item in path:
        if isinstance(item, int):
            for _ in range(item):
                pos = forward(Map, pos, dir)
                Map = show_path(Map, pos, dir)
        else:
            dir = turn(item, dir)
            Map = show_path(Map, pos, dir)
    with open('map', 'w') as file:
        file.write('\n'.join(Map))
    print(pos, dir)
    return 1000*pos[0]+4*pos[1]+dir

def distance(A, B):
    return sum(abs(a-b) for a, b in zip(A, B))

def unit(A, B):
    d = distance(A, B)
    return tuple((b-a)//d for a, b in zip(A, B))

def scale(k, A):
    return tuple(k*a for a in A)

def forward2(Map, pos, dir):
    portals = [
        ((50, 51), (1, 51), LEFT, 3),
        ((51, 51), (100, 51), LEFT, 2),
        ((101, 1), (101, 50), UP, 1),
        ((101, 1), (150, 1), LEFT, 0),
        ((151, 1), (200, 1), LEFT, 13),
        ((200, 50), (200, 1), DOWN, 12),
        ((200, 50), (151, 50), RIGHT, 7),
        ((150, 100), (150, 51), DOWN, 6),
        ((150, 100), (101, 100), RIGHT, 11),
        ((100, 100), (51, 100), RIGHT, 10),
        ((50, 150), (50, 101), DOWN, 9),
        ((1, 150), (50, 150), RIGHT, 8),
        ((1, 150), (1, 101), UP, 5),
        ((1, 51), (1, 100), UP, 4)
    ]
    
    ndir = dir
    next = add(pos, dirs[dir])
        
    for portal in portals:
        l, c = pos
        lmin = min(portal[0][0], portal[1][0])
        lmax = max(portal[0][0], portal[1][0])
        cmin = min(portal[0][1], portal[1][1])
        cmax = max(portal[0][1], portal[1][1])
        pdir = portal[2]

        if l>=lmin and l<=lmax and c>=cmin and c<=cmax and dir==pdir:
            dist = distance(portal[0], pos)
            pnext = portals[portal[3]]
            punit = unit(pnext[0], pnext[1])
            next = add(pnext[0], scale(dist, punit))
            ndir = opposite[pnext[2]]
            break

    if Map[next[0]][next[1]] == '#':
        return pos, dir
    return next, ndir

def part2(filename):
    Map, path = parse(filename)
    start_j = None
    for j, c in enumerate(Map[1]):
        if c == '.':
            start_j = j
            break
    if start_j is None:
        raise ValueError('PIPI')
    pos = (1, start_j)
    dir = RIGHT
    for item in path:
        if isinstance(item, int):
            for _ in range(item):
                pos, dir = forward2(Map, pos, dir)
                Map = show_path(Map, pos, dir)
        else:
            dir = turn(item, dir)
            Map = show_path(Map, pos, dir)
    with open('map', 'w') as file:
        file.write('\n'.join(Map))
    print(pos, dir)
    return 1000*pos[0]+4*pos[1]+dir


if __name__ == "__main__":
    part = int(sys.argv[1])
    filename = sys.argv[2]
    if part == 1:
        print(part1(filename))
    if part == 2:
        print(part2(filename))

