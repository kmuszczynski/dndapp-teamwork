import random
import re

def run_commands(string):
    print(type(string))
    if isinstance(string, str) and string.startswith('/'):
        m = re.match("/roll\D*(\d*)d(\d+)", string)
        dice_n = m.group(1)
        dice_t = m.group(2)
        rolls, rolls_sum = roll(dice_n, dice_t)
        return f"Rolling {dice_n}d{dice_t}: {rolls} SUM: {rolls_sum}"
    return string

def parse_int(string):
    if string == '':
        return 1
    return int(string)

def roll(n, d):
    n = parse_int(n)
    d = parse_int(d)
    rolls = []
    for i in range(n):
        rolls.append(random.randint(1,d))
    return rolls, sum(rolls)