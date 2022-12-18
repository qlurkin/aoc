import sys
from dataclasses import dataclass
from types import FunctionType

@dataclass
class Monkey:
    id: int
    items: list
    operation: FunctionType
    test: FunctionType
    count: int
    cache: dict
    test_value: int

def parse_monkey(txt):
    txt = txt.strip()
    id, items, operation, test, true, false = txt.split('\n')
    id = int(id.split(' ')[1][:-1])
    items = [int(x) for x in items.strip()[len('Starting items: '):].split(', ')]
    operation = operation.strip()[len('Operation: new = '):]
    #if operation == 'old * old':
    #    operation = 'old'
    operation_fun = lambda x: eval(operation, {'old': x})
    test = int(test.strip()[len('Test: divisible by '):])
    true = int(true.strip()[len('If true: throw to monkey '):])
    false = int(false.strip()[len('If false: throw to monkey '):])
    test_fun = lambda x: true if x%test==0 else false
    return Monkey(id, items, operation_fun, test_fun, 0, {}, test)
    

def parse(filename):
    with open(filename) as file:
        content = file.read()
    monkeys = [parse_monkey(monkey) for monkey in content.split('\n\n')]
    return monkeys

def part1(filename):
    monkeys = parse(filename)
    for i in range(20):
        for monkey in monkeys:
            for item in monkey.items:
                item = monkey.operation(item)
                monkey.count += 1
                item //= 3
                target = monkey.test(item)
                monkeys[target].items.append(item)
            monkey.items = []
    res = 1
    for elem in sorted([monkey.count for monkey in monkeys])[-2:]:
        res *= elem
    return res

def part2(filename):
    monkeys = parse(filename)
    for i in range(10000):
        print(i)
        for monkey in monkeys:
            for item in monkey.items:
                new_item = monkey.operation(item)
                monkey.count += 1
                target = monkey.test(new_item)
                # monkeys[target].items.append(new_item%(23*19*13*17))
                monkeys[target].items.append(new_item%(2*7*13*3*19*17*11*5))
            monkey.items = []
        #print([monkey.items for monkey in monkeys])
    print([monkey.count for monkey in monkeys])
    res = 1
    for elem in sorted([monkey.count for monkey in monkeys])[-2:]:
        res *= elem
    return res


if __name__ == "__main__":
    part = int(sys.argv[1])
    filename = sys.argv[2]
    if part == 1:
        print(part1(filename))
    if part == 2:
        print(part2(filename))

