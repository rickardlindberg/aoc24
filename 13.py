"""
Part 1:

>>> ClawMachines.load(price_addition=0).total_token_prices_for_wins()
39748

Part 2:

>>> ClawMachines.load(price_addition=10000000000000).total_token_prices_for_wins()
74478585072604
"""

import collections
import doctest
import re


class ClawMachines:

    @classmethod
    def load(cls, price_addition):
        with open("13.txt") as f:
            return cls.load_text(f.read(), price_addition)

    @classmethod
    def load_text(cls, text, price_addition):
        claw_machines = cls()
        lines = text.splitlines()
        while lines:
            claw_machines.add(ClawMachine.from_lines(lines, price_addition))
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
    def from_lines(cls, lines, price_addition):
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
            prize=Point.from_re_match(prize_match).add_both(price_addition),
        )

    def __init__(self, a, b, prize):
        self.a = a
        self.b = b
        self.prize = prize
        self.cache = {}

    def token_prizes_for_win(self):
        """
        Equation 1:

        a*self.a.x + b*self.b.x == self.price.x

        a = (self.price.x - b*self.b.x) / self.a.x

        Equation 2:

        a*self.a.y + b*self.b.y == self.price.y

        b = (self.price.y - a*self.a.y) / self.b.y
        """
        b_top = self.prize.y * self.a.x - self.prize.x * self.a.y
        b_bottom = self.a.x * self.b.y - self.b.x * self.a.y
        if b_top % b_bottom == 0:
            b = b_top // b_bottom
            a_top = self.prize.x - b * self.b.x
            a_bottom = self.a.x
            if a_top % a_bottom == 0:
                a = a_top // a_bottom
                if a >= 0 and b >= 0:
                    return a * 3 + b
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

    def add_both(self, distance):
        return Point(x=self.x + distance, y=self.y + distance)


doctest.testmod()
print("OK")

# 59004 too high
