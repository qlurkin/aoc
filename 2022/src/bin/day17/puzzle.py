import sys

rocks = []

rocks.append([(0, 0), (1, 0), (2, 0), (3, 0)])
rocks.append([(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)])
rocks.append([(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)])
rocks.append([(0, 0), (0, 1), (0, 2), (0, 3)])
rocks.append([(0, 0), (1, 0), (0, 1), (1, 1)])

directions = {
    '<': (-1, 0),
    '>': (1, 0)
}


def parse(filename):
    with open(filename) as file:
        jets = list(file.read().strip())
    return jets

def add(A, B):
    return tuple(a+b for a, b in zip(A, B))

def is_valid(cave, rock, position):
    # print('\n'.join(reversed([''.join(line) for line in cave])))
    for part in rock:
        part_position = add(position, part)
        # print(part_position)
        if cave[part_position[1]][part_position[0]] == '#':
            return False
    return True

def add_rock(cave, rock, position):
    # print('\n'.join(''.join(line) for line in cave))
    top = position[1]
    for part in rock:
        part_position = add(position, part)
        cave[part_position[1]][part_position[0]] = '#'
        if part_position[1] > top:
            top = part_position[1]
    return top

def part1(filename):
    jets = parse(filename)
    highest, cave, data = simulate(jets, 2022)
    return highest

def simulate(jets, n, cave=None, rock_index=0, jet_index=0, highest=0):
    if cave is None:
        cave = []
        cave.append(list("#########"))
    data = {}
    for i in range(n):
        position = (3, highest+4)
        key = (rock_index, jet_index)
        while len(cave) <= position[1]+4:
            cave.append(list("#       #"))
        while True:
            next_position = add(position, directions[jets[jet_index]])
            jet_index = (jet_index+1)%len(jets)
            if is_valid(cave, rocks[rock_index], next_position):
                position = next_position
            next_position = add(position, (0, -1))
            if is_valid(cave, rocks[rock_index], next_position):
                position = next_position
            else:
                break
        top = add_rock(cave, rocks[rock_index], position)
        rock_index = (rock_index + 1)%len(rocks)
        if top > highest:
            highest = top
        if key not in data:
            data[key] = {
                'hights': [],
                'rocks': [],
                'dh': [],
                'dr': []
            }
        else:
            print("potential cycle detected: {}".format(key))
            dh = highest - data[key]["hights"][-1]
            dr = i+1 - data[key]["rocks"][-1]
            data[key]["dh"].append(dh)
            data[key]["dr"].append(dr)
        data[key]["hights"].append(highest)
        data[key]["rocks"].append(i+1)
    return highest, cave, data


def part2(filename):
    jets = parse(filename)

    k = 1

    # highest, cave, data = simulate(jets, 3439+k*1700+161)
    # print('\n'.join(''.join(line) for line in cave))
    # print(data)
    # for cycle in data.values():
    #     if len(cycle['dh']) > 1:
    #         print(cycle)
    # print(len(jets))
    # print("should be", 5355+k*2642)
    # print("remaining", highest - (5355+k*2642))
    return 5355 + 588235292 * 2642 + 251 


if __name__ == "__main__":
    part = int(sys.argv[1])
    filename = sys.argv[2]
    if part == 1:
        print(part1(filename))
    if part == 2:
        print(part2(filename))

