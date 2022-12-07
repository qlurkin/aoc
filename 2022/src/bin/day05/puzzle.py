import sys
import re
from dataclasses import dataclass
from copy import copy

@dataclass
class Move:
    count: int
    src: int
    to: int

def squarify(T):
    width = max([len(line) for line in T])
    return [line + [' ']*(width-len(line)) for line in T]

def remove_pretty(L):
    return [elem for i, elem in enumerate(L) if (i-1)%4==0]

def transpose(T):
    return [[L[i] for L in T] for i in range(len(T[0]))]

def parse_start(S):
    lines = S.split('\n')
    lines = [list(line.rstrip()) for line in lines]
    lines = squarify(lines)
    lines = [remove_pretty(line) for line in lines]
    lines = transpose(lines)
    lines = [line[:-1] for line in lines]
    lines = [''.join(line).strip() for line in lines]
    lines = {i+1: value for i, value in enumerate(lines)}
    return lines

pattern = re.compile(r'move (\d+) from (\d+) to (\d+)')

def parse_moves(S):
    moves = pattern.findall(S)
    moves = [tuple(int(x) for x in move) for move in moves]
    moves = [Move(count, src, to) for count, src, to in moves]
    return moves

def parse(filename):
    with open(filename) as file:
        content = file.read()

    start, moves = content.split('\n\n')
    return parse_start(start), parse_moves(moves)

def do_move(state, move: Move):
    state = copy(state)
    for i in range(move.count):
        crate = state[move.src][0]
        state[move.src] = state[move.src][1:]
        state[move.to] = crate + state[move.to]
    return state

def do_move_9001(state, move: Move):
    state = copy(state)
    crate = state[move.src][:move.count]
    state[move.src] = state[move.src][move.count:]
    state[move.to] = crate + state[move.to]
    return state

def part1(filename):
    state, moves = parse(filename)

    for move in moves:
        state = do_move(state, move)

    return ''.join(state[i+1][0] for i in range(len(state)))

def part2(filename):
    state, moves = parse(filename)

    for move in moves:
        state = do_move_9001(state, move)

    return ''.join(state[i+1][0] for i in range(len(state)))


if __name__ == "__main__":
    part = int(sys.argv[1])
    filename = sys.argv[2]
    if part == 1:
        print(part1(filename))
    if part == 2:
        print(part2(filename))

