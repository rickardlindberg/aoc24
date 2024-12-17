"""
>>> list(itertools.combinations([1,2,3], 2))
[(1, 2), (1, 3), (2, 3)]
"""

import collections
import doctest
import itertools
import sys


EXAMPLE = """\
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
"""


class Antennas:

    @classmethod
    def read(cls):
        with open("8.txt") as f:
            return cls.read_contents(f.read())

    @classmethod
    def read_contents(cls, contents):
        antennas = cls()
        for y, line in enumerate(contents.splitlines()):
            for x, char in enumerate(line):
                antennas.add(x, y, char)
        return antennas

    def __init__(self):
        self.all = {}
        self.types = {}

    def add(self, x, y, char):
        point = Point(x, y)
        self.all[point] = char
        if char != ".":
            if char not in self.types:
                self.types[char] = []
            self.types[char].append(point)

    def count_unique_antinodes(self):
        antinode_points = set()
        for char, points in self.types.items():
            for a, b in itertools.combinations(points, 2):
                for antinode_point in a.get_antinotes(b):
                    if antinode_point in self.all:
                        antinode_points.add(antinode_point)
        return len(antinode_points)


class Point(collections.namedtuple("Point", ["x", "y"])):
    """
    >>> Point(0, 0).get_antinotes(Point(2, 2))
    [Point(x=-2, y=-2), Point(x=4, y=4)]
    """

    def get_antinotes(self, other):
        x_diff = self.x - other.x
        y_diff = self.y - other.y
        return [
            self.move(dx=x_diff, dy=y_diff),
            other.move(dx=-x_diff, dy=-y_diff),
        ]

    def move(self, dx, dy):
        return Point(x=self.x + dx, y=self.y + dy)


doctest.testmod()
example = Antennas.read_contents(EXAMPLE)
print(example.types)
print(example.count_unique_antinodes())
# 2500 too high
assert Antennas.read().count_unique_antinodes() == 259
