"""
Examples:

>>> onsen = OnsenParser().parse_lines([
...     "r, g, rg",
...     "",
...     "rg",
... ])
>>> onsen.count_ways_to_make_towel_designs()
2

>>> onsen = OnsenParser().parse_lines([
...     "r, wr, b, g, bwu, rb, gb, br",
...     "",
...     "brwrr",
...     "bggr",
...     "gbbr",
...     "rrbgbr",
...     "ubwu",
...     "bwurrg",
...     "brgr",
...     "bbrgwb",
... ])
>>> len(onsen.towels)
8
>>> len(onsen.designs)
8
>>> onsen.count_possible_towel_designs()
6
>>> onsen.count_ways_to_make_towel_designs()
16

Part 1:

>>> onsen = OnsenParser().parse()
>>> onsen.count_possible_towel_designs()
367

Part 2:

>>> onsen.count_ways_to_make_towel_designs()
724388733465031
"""

import pprint

class OnsenParser:

    def parse(self):
        with open("19.txt") as f:
            return self.parse_lines(f)

    def parse_lines(self, lines):
        onsen = Onsen()
        for index, line in enumerate(lines):
            if index == 0:
                for towel in line.split(", "):
                    onsen.add_towel(Towel(towel.strip()))
            elif index > 1:
                onsen.add_design(Design(line.strip()))
        return onsen

class Towel:

    def __init__(self, towel):
        self.towel = towel

    def design(self, design):
        """
        >>> Towel("foo").design("foobar")
        'bar'
        """
        if design.startswith(self.towel):
            return design[len(self.towel):]
        else:
            raise DesignNotPossible()

    def __repr__(self):
        return f"Towel({self.towel!r})"

class Design:

    def __init__(self, design):
        self.design = design
        self.cache = {}

    def is_possible(self, towels):
        return self.count_ways_to_make(towels) > 0

    def count_ways_to_make(self, towels):
        return self.count_ways_to_make_rest(self.design, towels)

    def count_ways_to_make_rest(self, rest_design, towels):
        if rest_design not in self.cache:
            if rest_design:
                self.cache[rest_design] = 0
                for towel in towels:
                    try:
                        self.cache[rest_design] += self.count_ways_to_make_rest(
                            towel.design(rest_design),
                            towels
                        )
                    except DesignNotPossible:
                        pass
            else:
                self.cache[rest_design] = 1
        return self.cache[rest_design]

class Onsen:

    def __init__(self):
        self.towels = []
        self.designs = []

    def add_towel(self, towel):
        self.towels.append(towel)

    def add_design(self, design):
        self.designs.append(design)

    def count_possible_towel_designs(self):
        count = 0
        for design in self.designs:
            if design.is_possible(self.towels):
                count += 1
        return count

    def count_ways_to_make_towel_designs(self):
        return sum(
            design.count_ways_to_make(self.towels)
            for design in self.designs
        )

class DesignNotPossible(Exception):
    pass

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print("OK")
