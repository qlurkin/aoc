import re

values = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
    "1": "1",
    "2": "2",
    "3": "3",
    "4": "4",
    "5": "5",
    "6": "6",
    "7": "7",
    "8": "8",
    "9": "9",
    "0": "0",
}


def find_first_digit(s):
    pattern = re.compile(
        r"(?=(0|1|2|3|4|5|6|7|8|9|one|two|three|four|five|six|seven|eight|nine))"
    )
    res = pattern.findall(s)
    return res[0], res[-1]


res = 0
with open("puzzle") as file:
    for line in file:
        c1, c2 = find_first_digit(line)
        v = int(values[c1] + values[c2])
        print(line, c1, c2, v)
        # res += int(c1 + c2)
        res += v
print(res)
