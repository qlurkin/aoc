import sys
from dataclasses import dataclass
from typing import List

@dataclass
class Directory:
    parent: List['Directory']
    name: str
    content: list

@dataclass
class File:
    parent: Directory
    name: str
    size: int

def get_size(obj):
    if isinstance(obj, File):
        return obj.size
    if isinstance(obj, Directory):
        size = 0
        for child in obj.content:
            size += get_size(child)
        return size

def is_command(tokens):
    return tokens[0] == '$'

def is_directory(tokens):
    return tokens[0] == 'dir'

def is_file(tokens):
    try:
        int(tokens[0])
        return True
    except ValueError:
        return False

def process_command(cmd, params, current: Directory, root):
    if cmd == 'ls':
        pass
    elif cmd == 'cd':
        arg = params[0]
        if arg == '/':
            current = root
        elif arg == '..':
            current = current.parent
        else:
            for child in current.content:
                if child.name == arg:
                    current = child
                    break
    return current

def parse(filename):
    root = Directory(None, '/', [])
    current = root
    with open(filename) as file:
        for line in file:
            line = line.strip()
            if len(line) > 0:
                tokens = line.split(' ')
                if is_command(tokens):
                    current = process_command(tokens[1], tokens[2:], current, root)
                elif is_directory(tokens):
                    obj = Directory(current, tokens[1], [])
                    current.content.append(obj)
                elif is_file(tokens):
                    obj = File(current, tokens[1], int(tokens[0]))
                    current.content.append(obj)
                else:
                    raise Exception('Input Parsing Failed: Tokens = {}'.format(tokens))
    return root

def traverse(root, fun, init):
    res = fun(init, root)
    if isinstance(root, Directory):
        for child in root.content:
            res = traverse(child, fun, res)
    return res

def fun(acc, obj):
    if isinstance(obj, Directory):
        size = get_size(obj)
        if size <= 100_000:
            return acc + size
    return acc

def fun2(acc, obj):
    if isinstance(obj, Directory):
        size = get_size(obj)
        acc.append(size)
    return acc 

def part1(filename):
    root = parse(filename)
    return traverse(root, fun, 0)

def part2(filename):
    root = parse(filename)
    total = get_size(root)
    directories = traverse(root, fun2, [])
    directories.sort()
    for size in directories:
        if size >= total - 40_000_000:
            return size

if __name__ == "__main__":
    part = int(sys.argv[1])
    filename = sys.argv[2]
    if part == 1:
        print(part1(filename))
    if part == 2:
        print(part2(filename))

