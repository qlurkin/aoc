import sys


def new_set():
    return {
        "red": 0,
        "green": 0,
        "blue": 0,
    }


def parse(line):
    game, sets_str = line.split(":")
    game = int(game.split(" ")[1])
    sets = []
    for set_str in sets_str.split(";"):
        Set = new_set()
        for kind in set_str.split(","):
            kind = kind.strip()
            n_str, kind = kind.split(" ")
            Set[kind] = int(n_str)
        sets.append(Set)
    return game, sets


filename = sys.argv[1]

with open(filename) as file:
    res = 0
    for line in file:
        line = line.rstrip()
        game, sets = parse(line)
        max_red = 0
        max_green = 0
        max_blue = 0
        for s in sets:
            if s["red"] > max_red:
                max_red = s["red"]
            if s["green"] > max_green:
                max_green = s["green"]
            if s["blue"] > max_blue:
                max_blue = s["blue"]
        power = max_blue * max_green * max_red
        res += power
    print(res)
