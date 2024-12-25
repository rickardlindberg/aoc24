"""
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

Part 1:

>>> OnsenParser().parse().count_possible_towel_designs()
367
"""

class OnsenParser:

    def parse(self):
        with open("19.txt") as f:
            return self.parse_lines(f)

    def parse_lines(self, lines):
        onsen = Onsen()
        for index, line in enumerate(lines):
            if index == 0:
                for towel in line.split(", "):
                    onsen.add_towel(Towel(towel))
            elif index > 1:
                onsen.add_design(line.strip())
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

class Onsen:

    def __init__(self):
        self.towels = []
        self.designs = []
        self.cache = {}

    def add_towel(self, towel):
        self.towels.append(towel)
        self.cache = {}

    def add_design(self, design):
        self.designs.append(design)

    def count_possible_towel_designs(self):
        count = 0
        for design in self.designs:
            if self.is_possible(design):
                count += 1
        return count

    def is_possible(self, design):
        if design not in self.cache:
            self.cache[design] = self.calculate_is_possible(design)
        return self.cache[design]

    def calculate_is_possible(self, design):
        if design:
            for towel in self.towels:
                try:
                    if self.is_possible(towel.design(design)):
                        return True
                except DesignNotPossible:
                    pass
            return False
        else:
            return True

class DesignNotPossible(Exception):
    pass

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print("OK")
