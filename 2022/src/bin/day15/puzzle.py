import sys
import re

def parse(filename):
    sensors = []
    beacons = []
    pattern = re.compile(r'Sensor at x=(.+), y=(.+): closest beacon is at x=(.+), y=(.+)')
    with open(filename) as file:
        for line in file:
            line = line.strip()
            if len(line) > 0:
                res = pattern.match(line)
                sx, sy, bx, by = (int(x) for x in res.groups())
                sensors.append((sx, sy))
                beacons.append((bx, by))
    return sensors, beacons

def distance(A, B):
    return sum(abs(a-b) for a, b in zip(A, B))


def part1(filename):
    sensors, beacons = parse(filename)
    print(sensors)
    print(beacons)
    excluded = set()
    for sensor, beacon in zip(sensors, beacons):
        d = distance(sensor, beacon)
        for x in range(sensor[0]-d,sensor[0]+d+1):
            p = (x, 2_000_000)
            if distance(p, sensor) <= d:
                excluded.add(p)
    for beacon in beacons:
        if beacon in excluded:
            excluded.remove(beacon)
        
    return len(excluded)

SIZE = 4_000_000
# SIZE = 20

def remove_from_one_range(ran, to_remove):
    low, high = ran
    rlow, rhigh = to_remove

    if rlow > high or rhigh < low:
        return [ran]

    if rlow <= low:
        if rhigh >= high:
            return []
        else:
            return [[rhigh+1, high]]
    else:
        if rhigh >= high:
            return [[low, rlow-1]]
        else:
            return [[low, rlow-1], [rhigh+1, high]]

def remove_from_all_range(rans, to_remove):
    res = []
    for ran in rans:
        res.extend(remove_from_one_range(ran, to_remove))
    return res

def part2(filename):
    sensors, beacons = parse(filename)
    print(sensors)
    print(beacons)
    res = None
    for y in range(0, SIZE+1):
        print(y)
        included = [[0, SIZE]]
        for sensor, beacon in zip(sensors, beacons):
            d = distance(sensor, beacon)
            r = d-abs(y-sensor[1]) 
            # to_remove = set(x for x in range(max(sensor[0]-r, 0), min(sensor[0]+r+1, SIZE)))
            # included -= to_remove 
            included = remove_from_all_range(included, [sensor[0]-r, sensor[0]+r])


            # for x in list(included):
            #     p = (x, y)
            #     if distance(p, sensor) <= d:
            #         included.remove(x)
        if len(included) > 0:
            res = (included[0][0], y)
            break
        
    return res[0]*4_000_000+res[1]


if __name__ == "__main__":
    part = int(sys.argv[1])
    filename = sys.argv[2]
    if part == 1:
        print(part1(filename))
    if part == 2:
        print(part2(filename))

