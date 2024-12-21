"""
A*94=8400
A*34=5400
B*22=8400
B*67=5400

8400 = A*94 + B*22

B =

5400 = A*34 + B*67

5400 = A*34 + ((8400 - A*94) / 22)*67

>>> ClawMachines.load().total_token_prices_for_wins()
39748
"""

import collections
import doctest
import re
import sys

sys.setrecursionlimit(100000000)


class ClawMachines:

    @classmethod
    def load(cls):
        with open("13.txt") as f:
            return cls.load_text(f.read())

    @classmethod
    def load_text(cls, text):
        claw_machines = cls()
        lines = text.splitlines()
        while lines:
            claw_machines.add(ClawMachine.from_lines(lines))
            while lines and lines[0].strip() == "":
                lines.pop(0)
        return claw_machines

    def __init__(self):
        self.machines = []

    def add(self, claw_machine):
        self.machines.append(claw_machine)

    def total_token_prices_for_wins(self):
        return sum(machine.token_prizes_for_win() for machine in self.machines)


class ClawMachine:

    @classmethod
    def from_lines(cls, lines):
        a_regex = r"Button A: X[+](\d+), Y[+](\d+)"
        b_regex = r"Button B: X[+](\d+), Y[+](\d+)"
        prize_regex = r"Prize: X=(\d+), Y=(\d+)"
        a_line = lines.pop(0)
        b_line = lines.pop(0)
        price_line = lines.pop(0)
        a_match = re.match(a_regex, a_line)
        b_match = re.match(b_regex, b_line)
        prize_match = re.match(prize_regex, price_line)
        return ClawMachine(
            a=Point.from_re_match(a_match),
            b=Point.from_re_match(b_match),
            prize=Point.from_re_match(prize_match),
        )

    def __init__(self, a, b, prize):
        self.a = a
        self.b = b
        self.prize = prize
        self.cache = {}

    def token_prizes_for_win(self):
        tokens = self.minimize_win_from(Tokens.empty(), Point(0, 0))
        if tokens:
            return tokens.a * 3 + tokens.b
        else:
            return 0

    def minimize_win_from(self, tokens, point):
        def do():
            if self.prize == point:
                return tokens
            elif point.is_less_than(self.prize):
                sub_tokens = self.minimize_win_from(tokens.inc_a(), point.add(self.a))
                if sub_tokens:
                    return sub_tokens
                sub_tokens = self.minimize_win_from(tokens.inc_b(), point.add(self.b))
                if sub_tokens:
                    return sub_tokens
            return None

        key = (tokens, point)
        if key not in self.cache:
            self.cache[key] = do()
        return self.cache[key]


class Tokens(collections.namedtuple("Tokens", ["a", "b"])):

    @classmethod
    def empty(cls):
        return cls(0, 0)

    def inc_a(self):
        return self._replace(a=self.a + 1)

    def inc_b(self):
        return self._replace(b=self.b + 1)


class Point(collections.namedtuple("Point", ["x", "y"])):

    @classmethod
    def from_re_match(cls, re_match):
        return cls(*[int(x) for x in re_match.groups()])

    def is_less_than(self, other):
        return self.x < other.x and self.y < other.y

    def add(self, other):
        return Point(x=self.x + other.x, y=self.y + other.y)


doctest.testmod()
print("OK")

# 59004 too high
