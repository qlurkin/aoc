import sys
import re
from scipy import sparse as sp
from dataclasses import dataclass
import numpy as np
import itertools

@dataclass
class Valve:
    name: str
    rate: int
    neighbours: list
    index: int

    def __hash__(self):
        return id(self)

def parse(filename):
    pattern = re.compile(r'Valve ([^ ]+) has flow rate=([^;]+); tunnels? leads? to valves? (.+)$')
    valves = []
    index = {}
    with open(filename) as file:
        for line in file:
            line = line.strip()
            if len(line) > 0:
                res = pattern.match(line)
                name, rate, neighbours = res.groups()
                rate = int(rate)
                neighbours = neighbours.split(', ')
                valve = Valve(name, rate, neighbours, len(valves))
                valves.append(valve)
                index[name] = valve
    for valve in valves:
        neighbours = []
        for neighbour in valve.neighbours:
            neighbours.append(index[neighbour])
        valve.neighbours = neighbours
    return valves, index


def graph_matrix(valves):
    size = len(valves)
    matrix = np.zeros((size, size))
    for valve in valves:
        for neighbour in valve.neighbours:
            matrix[valve.index, neighbour.index] = 1
    return matrix

def get_subgraph(graph, subset):
    size = len(subset)
    matrix = np.zeros((size, size))
    for i, valve_i in enumerate(subset):
        for j, valve_j in enumerate(subset):
            matrix[i, j] = graph[valve_i.index, valve_j.index]
    return matrix

def simplify_graph(valves, graph, AA_index):
    simple_valves = [valves[AA_index]] + [valve for valve in valves if valve.rate != 0]
    simple_graph = get_subgraph(graph, simple_valves)
    return simple_valves, simple_graph
    
def explore(graph, valves, current, remaining, opened, released, path):
    max = released
    best_path = path
    for i, time in enumerate(graph[current]):
        if i != current:
            if not opened[i]:
                next_remaining = remaining-time-1
                if next_remaining >= 0:
                    next_opened = list(opened)
                    next_opened[i] = True
                    next_released = released + next_remaining * valves[i].rate 
                    res, next_path = explore(graph, valves, i, next_remaining, next_opened, next_released, '{} {}({}*{})'.format(path, valves[i].name, next_remaining, valves[i].rate))
                    if res > max:
                        max = res
                        best_path = next_path
    return max, best_path


def part1(filename):
    valves, index = parse(filename)
    graph = graph_matrix(valves)
    res = sp.csgraph.dijkstra(graph)
    start = index['AA']
    simple_valves, simple_graph = simplify_graph(valves, res, start.index)
    print(simple_graph)
    print([(valve.name, valve.rate) for valve in simple_valves])
    max, path = explore(simple_graph, simple_valves, 0, 30, [False]*len(simple_valves), 0, "AA")
    return max, path

def all_subset(valves):
    subsets = []
    for s in range(len(valves)-1):
        subsets.extend(itertools.combinations(valves, s+1))
    return subsets

def find_complementary(subsets, i_subset, valves):
    valves = set(valves)
    subset = set(subsets[i_subset])
    for i, other in enumerate(subsets):
        other = set(other)
        if other != subset:
            # print([valve.name for valve in subset], [valve.name for valve in other])
            if other | subset == valves:
                return i
    return None

def part2(filename):
    valves, index = parse(filename)
    graph = graph_matrix(valves)
    graph = sp.csgraph.dijkstra(graph)
    start = index['AA']
    simple_valves, simple_graph = simplify_graph(valves, graph, start.index)
    print(simple_graph)
    print([(valve.name, valve.rate) for valve in simple_valves])
    subsets = all_subset(simple_valves[1:])
    releaseds = []
    n = len(subsets)
    for i, subset in enumerate(subsets):
        subset = [simple_valves[0]] + list(subset)
        # print([valve.name for valve in subset])
        subgraph = get_subgraph(graph, subset)
        max, path = explore(subgraph, subset, 0, 26, [False]*len(subset), 0, "AA")
        releaseds.append(max)
        print('{}/{}'.format(i, n))

    max = 0
    for i_subset in range(len(subsets)):
        i_other =  find_complementary(subsets, i_subset, simple_valves[1:])
        value = releaseds[i_subset] + releaseds[i_other]

        print('{} <-> {}: {} + {} = {}'.format(
            [valve.name for valve in subsets[i_subset]],
            [valve.name for valve in subsets[i_other]],
            releaseds[i_subset],
            releaseds[i_other],
            value
        ))

        if value > max:
            max = value


    return max


if __name__ == "__main__":
    part = int(sys.argv[1])
    filename = sys.argv[2]
    if part == 1:
        print(part1(filename))
    if part == 2:
        print(part2(filename))

