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
        with open("08.txt") as f:
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
                for antinode_point in a.get_antinotes(b, self):
                    antinode_points.add(antinode_point)
        return len(antinode_points)

    def is_valid(self, point):
        return point in self.all


class Point(collections.namedtuple("Point", ["x", "y"])):

    def get_antinotes(self, other, antennas):
        x_diff = self.x - other.x
        y_diff = self.y - other.y
        antinodes = []
        left = self
        while antennas.is_valid(left):
            antinodes.append(left)
            left = left.move(dx=x_diff, dy=y_diff)
        right = other
        while antennas.is_valid(right):
            antinodes.append(right)
            right = right.move(dx=-x_diff, dy=-y_diff)
        return antinodes

    def move(self, dx, dy):
        return Point(x=self.x + dx, y=self.y + dy)


doctest.testmod()
print(Antennas.read_contents(EXAMPLE).count_unique_antinodes())
print(Antennas.read().count_unique_antinodes())
