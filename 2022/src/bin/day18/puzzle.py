import sys

def parse(filename):
    res = []
    with open(filename) as file:
        for line in file:
            line = line.strip()
            if len(line) > 0:
                res.append(tuple(int(v) for v in line.split(',')))
    return res

def add(A, B):
    return tuple(a+b for a, b in zip(A, B))
    
directions = [
    (1, 0, 0),
    (-1, 0, 0),
    (0, 1, 0),
    (0, -1, 0),
    (0, 0, 1),
    (0, 0, -1),
]

def part1(filename):
    cubes = parse(filename)
    faces = {}
    for cube in cubes:
        faces[cube] = 6

    for cube in cubes:
        for dir in directions:
            other = add(cube, dir)
            if other in faces:
                faces[cube] -= 1

    return sum(x for x in faces.values())

def part2(filename):
    sys.setrecursionlimit(10000)
    cubes = parse(filename)
    xmin = min(cube[0] for cube in cubes) - 1
    xmax = max(cube[0] for cube in cubes) + 1
    ymin = min(cube[1] for cube in cubes) - 1
    ymax = max(cube[1] for cube in cubes) + 1
    zmin = min(cube[2] for cube in cubes) - 1
    zmax = max(cube[2] for cube in cubes) + 1

    print("Steam Cube:", xmax-xmin, ymax-ymin, zmax-zmin)

    steams = set()

    def expand(steam):
        steams.add(steam)
        for dir in directions:
            other = add(steam, dir)
            x, y, z = other
            if x >= xmin and x <= xmax and y >= ymin and y <= ymax and z >= zmin and z <= zmax:
                if other not in steams and other not in cubes:
                    expand(other)



    expand((xmin, ymin, zmin))

    faces = {}
    for cube in cubes:
        faces[cube] = 0

    for cube in cubes:
        for dir in directions:
            other = add(cube, dir)
            if other in steams:
                faces[cube] += 1

    return sum(x for x in faces.values())


if __name__ == "__main__":
    part = int(sys.argv[1])
    filename = sys.argv[2]
    if part == 1:
        print(part1(filename))
    if part == 2:
        print(part2(filename))

