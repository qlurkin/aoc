import sys
import json
from functools import cmp_to_key

def parse_pair(pair):
    items = pair.strip().split('\n')
    items = [json.loads(item) for item in items]
    return items


def parse(filename):
    with open(filename) as file:
        content = file.read()

    pairs = content.strip().split('\n\n')
    pairs = [parse_pair(pair) for pair in pairs]

    return pairs

def cmp(L, R):
    if isinstance(L, int) and isinstance(R, int):
        if L < R:
            return 1
        elif L > R:
            return -1
        else:
            return 0
    if isinstance(L, list) and isinstance(R, list):
        for i in range(min(len(L), len(R))):
            if cmp(L[i], R[i]) == 1:
                return 1
            elif cmp(L[i], R[i]) == -1:
                return -1
        if len(L) < len(R):
            return 1
        elif len(L) > len(R):
            return -1
        return 0
    if isinstance(L, int) and isinstance(R, list):
        return cmp([L], R)
    if isinstance(L, list) and isinstance(R, int):
        return cmp(L, [R])
    raise NotImplemented('Incompatible types for cmp: ({}, {})'.format(type(L), type(R)))

def pairs_to_list(pairs):
    res = []
    for pair in pairs:
        res.extend(pair)
    return res


def part1(filename):
    pairs = parse(filename)
    cmps = [cmp(L, R) for L, R in pairs]
    print(pairs)
    print(cmps)
    res = sum(i+1 for i, v in enumerate(cmps) if v == 1)
    return res

def part2(filename):
    pairs = parse(filename)
    packets = pairs_to_list(pairs)
    packets.append([[2]])
    packets.append([[6]])
    print(packets)
    packets.sort(key=cmp_to_key(lambda L, R: cmp(R, L)))
    return (packets.index([[2]])+1)*(packets.index([[6]])+1)


if __name__ == "__main__":
    part = int(sys.argv[1])
    filename = sys.argv[2]
    if part == 1:
        print(part1(filename))
    if part == 2:
        print(part2(filename))

