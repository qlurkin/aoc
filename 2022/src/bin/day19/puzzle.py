import sys
import re
from dataclasses import dataclass, field
from enum import Enum
from copy import deepcopy
import time
from types import MappingProxyType
from functools import cache as caca

class Type(Enum):
    ORE = 0
    CLAY = 1
    OBSIDIAN = 2
    GEODE = 3

@dataclass(frozen=True)
class Cost:
    price: MappingProxyType
    
    @staticmethod
    def new(ore=0, clay=0, obsidian=0, geode=0):
        return Cost(MappingProxyType({Type.ORE: ore, Type.CLAY: clay, Type.OBSIDIAN: obsidian, Type.GEODE: geode}))

    @staticmethod
    def from_dict(D):
        D = deepcopy(D)
        return Cost(MappingProxyType(D))

    def hash(self):
        return tuple(self.price[t] for t in Type)
        
        
@dataclass(frozen=True)
class Factory:
    id: int
    robots: MappingProxyType

    @staticmethod
    def new(id: int, ore: Cost, clay: Cost, obsidian: Cost, geode: Cost):
        robots = {Type.ORE: ore, Type.CLAY: clay, Type.OBSIDIAN: obsidian, Type.GEODE: geode}
        return Factory(id, MappingProxyType(robots))

    def hash(self):
        return (id, tuple(self.robots[t].hash() for t in Type))

@dataclass(frozen=True)
class State:
    factory: Factory
    robots: MappingProxyType = field(default_factory=lambda : MappingProxyType({t: 0 if t != Type.ORE else 1 for t in Type}))
    ressources: MappingProxyType = field(default_factory=lambda : MappingProxyType({t: 0 for t in Type}))

    def hash(self):
        return (self.factory.hash(), tuple(self.robots[t] for t in Type), tuple(self.ressources[t] for t in Type))

    def can_produce(self, type: Type | None):
        if type is None:
            return True
        return all(self.ressources[t] >= self.factory.robots[type].price[t] for t in Type)

    def apply(self, cost: Cost):
        ressources = self.ressources
        for t in Type:
            ressources = MappingProxyType(ressources | {t: ressources[t] - cost.price[t]})
        return State(self.factory, self.robots, ressources)

    def produce(self, type: Type | None):
        if type is None:
            return self
        if not self.can_produce(type):
            return self
        new_state = self.apply(self.factory.robots[type])
        robots = self.robots
        robots = MappingProxyType(robots | {type: robots[type]+1})
        return State(self.factory, robots, new_state.ressources)

    def update(self, type: Type | None):
        new_ressources = {}
        for t in Type:
            new_ressources[t] = -self.robots[t]
        new_state = self.produce(type)
        new_state = new_state.apply(Cost.from_dict(new_ressources))
        return new_state

def parse(filename):
    pattern = re.compile(r'Blueprint ([^:]+): Each ore robot costs ([^ ]+) ore. Each clay robot costs ([^ ]+) ore. Each obsidian robot costs ([^ ]+) ore and ([^ ]+) clay. Each geode robot costs ([^ ]+) ore and ([^ ]+) obsidian.')
    factories = []
    with open(filename) as file:
        for line in file:
            line = line.strip()
            if len(line) > 0:
                res = pattern.match(line)
                if res is None:
                    print('Line Parsing Failed')
                    continue
                id, ore_ore, clay_ore, obsidian_ore, obsidian_clay, geode_ore, geode_obsidian = (int(x) for x in res.groups())
                factories.append(Factory.new(id,
                    ore=Cost.new(ore=ore_ore),
                    clay=Cost.new(ore=clay_ore),
                    obsidian=Cost.new(ore=obsidian_ore, clay=obsidian_clay),
                    geode=Cost.new(ore=geode_ore, obsidian=geode_obsidian)
                ))
    return factories

def best_possible(deep, state):
    geode_robots = state.robots[Type.GEODE]
    obsidian_robots = state.robots[Type.OBSIDIAN]
    clay_robots = state.robots[Type.CLAY]
    ore_robots = state.robots[Type.ORE]
    geode = state.ressources[Type.GEODE]
    obsidian = state.ressources[Type.OBSIDIAN]
    clay = state.ressources[Type.CLAY]
    ore = state.ressources[Type.ORE]
   
    ore_robots_cost = state.factory.robots[Type.ORE].price[Type.ORE]
    clay_robots_cost = state.factory.robots[Type.ORE].price[Type.ORE]
    
    max_ore_robots = ore_robots + deep//ore_robots_cost
    max_clay_robots = clay_robots + deep//clay_robots_cost

    return (geode + deep*geode_robots + (deep-1)*deep//2)

def key(state):
    geode_robots = state.robots[Type.GEODE]
    obsidian_robots = state.robots[Type.OBSIDIAN]
    clay_robots = state.robots[Type.CLAY]
    ore_robots = state.robots[Type.ORE]
    geode = state.ressources[Type.GEODE]
    obsidian = state.ressources[Type.OBSIDIAN]
    clay = state.ressources[Type.CLAY]
    ore = state.ressources[Type.ORE]
    return 10000000*geode_robots+1000000*obsidian_robots+100000*clay_robots+10000*ore_robots+1000*geode+100*obsidian+10*clay+ore

def part1(filename):
    moves = list(Type) + [None]
    factories = parse(filename)
    res = 0
    for factory in factories:
        max_geode = 0
        cache = {}
        max_robots_needed = {type: max(factory.robots[t].price[Type.OBSIDIAN] for t in Type) for type in Type}
        max_robots_needed[Type.GEODE] = float('inf')
       
        def explore(state: State, deep):
            nonlocal max_geode
            # print(max_geode)
            state_hash = state.hash()
            if state_hash in cache:
                if cache[state_hash] >= deep:
                    return

            if deep < 0:
                return

            if best_possible(deep, state) < max_geode:
                return

            geode = state.ressources[Type.GEODE]
            if geode > max_geode:
                max_geode = geode


            possible_state = []
            for move in moves:
                if move is None:
                    new_state = state.update(move)
                    possible_state.append(new_state)
                    continue
                if state.robots[move] < max_robots_needed[move]:
                    if state.can_produce(move):
                        new_state = state.update(move)
                        possible_state.append(new_state)
            possible_state.sort(key=key, reverse=True)
            for next_state in possible_state:
                explore(next_state, deep-1)
            cache[state_hash] = deep

        state = State(factory)
        the_start = time.time()
        explore(state, 24)
        print('(Blueprint {}) Max Geode = {} (time: {})'.format(factory.id, max_geode, time.time()-the_start))
        res += factory.id * max_geode
    return res

def part2(filename):
    moves = list(Type) + [None]
    factories = parse(filename)
    res = 1
    for factory in factories[:3]:
        max_geode = 0
        cache = {}
        max_robots_needed = {type: max(factory.robots[t].price[Type.OBSIDIAN] for t in Type) for type in Type}
        max_robots_needed[Type.GEODE] = float('inf')
        def explore(state: State, deep):
            nonlocal max_geode
            # print(max_geode)
            state_hash = state.hash()
            if state_hash in cache:
                if cache[state_hash] >= deep:
                    return

            if deep < 0:
                return

            if best_possible(deep, state) < max_geode:
                return

            geode = state.ressources[Type.GEODE]
            if geode > max_geode:
                max_geode = geode


            possible_state = []
            for move in moves:
                if move is None:
                    new_state = state.update(move)
                    possible_state.append(new_state)
                    continue
                if state.robots[move] < max_robots_needed[move]:
                    if state.can_produce(move):
                        new_state = state.update(move)
                        possible_state.append(new_state)
            possible_state.sort(key=key, reverse=True)
            for next_state in possible_state:
                explore(next_state, deep-1)
            cache[state_hash] = deep

        state = State(factory)
        the_start = time.time()
        explore(state, 32)
        print('(Blueprint {}) Max Geode = {} (time: {})'.format(factory.id, max_geode, time.time()-the_start))
        res *= max_geode
    return res

if __name__ == "__main__":
    part = int(sys.argv[1])
    filename = sys.argv[2]
    if part == 1:
        print(part1(filename))
    if part == 2:
        print(part2(filename))

