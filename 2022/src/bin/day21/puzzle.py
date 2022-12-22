import sys
from scipy import optimize
from matplotlib import pyplot as plt
import numpy as np

operation = {
    '+': lambda a, b: a+b,
    '-': lambda a, b: a-b,
    '*': lambda a, b: a*b,
    '/': lambda a, b: a/b,
}

def make_value(value):
    def fun(x=0):
        return value
    return fun

def make_operation(v1, op, v2, vars):
    def fun(x=0):
        return operation[op](vars[v1](x), vars[v2](x))
    return fun

def make_variable():
    def fun(x=0):
        return x
    return fun

def parse(filename):
    vars = {}
    with open(filename) as file:
        for line in file:
            line = line.strip()
            if len(line) > 0:
                name, expression = line.split(': ')
                try:
                    value = int(expression)
                    expression = make_value(value)
                except ValueError:
                    op1, op, op2 = expression.split(' ')
                    expression = make_operation(op1, op, op2, vars)
                vars[name] = expression
    return vars

def parse2(filename):
    vars = {}
    with open(filename) as file:
        for line in file:
            line = line.strip()
            if len(line) > 0:
                name, expression = line.split(': ')
                if name == 'humn':
                    expression = make_variable()
                else:
                    try:
                        value = int(expression)
                        expression = make_value(value)
                    except ValueError:
                        op1, op, op2 = expression.split(' ')
                        if name == 'root':
                            op = '-'
                        expression = make_operation(op1, op, op2, vars)
                vars[name] = expression
    return vars

def part1(filename):
    vars = parse(filename)
    return vars['root']()

def part2(filename):
    vars = parse2(filename)
    return optimize.newton(vars['root'], 300)


if __name__ == "__main__":
    part = int(sys.argv[1])
    filename = sys.argv[2]
    if part == 1:
        print(part1(filename))
    if part == 2:
        print(part2(filename))

