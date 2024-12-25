"""
Examples:

>>> memory_space = BytePositionParser().parse_lines([
...     "5,4",
...     "4,2",
...     "4,5",
...     "3,0",
...     "2,1",
...     "6,3",
...     "2,4",
...     "1,5",
...     "0,6",
...     "3,3",
...     "2,6",
...     "5,1",
...     "1,2",
...     "5,5",
...     "2,5",
...     "6,5",
...     "1,4",
...     "0,4",
...     "6,4",
...     "1,1",
...     "6,1",
...     "1,0",
...     "0,5",
...     "1,6",
...     "2,0",
... ], size=6)
>>> memory_space.simulate_fall(12).print()
___#___
__#__#_
____#__
___#__#
__#__#_
_#__#__
#_#____
>>> memory_space.find_path().print()
OO_#OOO
_O#OO#O
_OOO#OO
___#OO#
__#OO#_
_#_O#__
#_#OOOO
>>> memory_space.steps()
22

Part 1:

>>> memory_space = BytePositionParser().parse()
>>> memory_space.simulate_fall(1024).find_path().steps()
294

Part 2:

>>> print(memory_space.simulate_until_blocked().aoc_format())
31,22
"""

import collections

class BytePositionParser:

    def parse(self):
        with open("18.txt") as f:
            return self.parse_lines(lines=f, size=70)

    def parse_lines(self, lines, size):
        memory_space = MemorySpace(size=size)
        for line in lines:
            x, y = [int(x) for x in line.split(",")]
            memory_space.add_incoming_byte(x, y)
        return memory_space

class MemorySpace:

    def __init__(self, size):
        self.size = size
        self.corrupted = set()
        self.path = set()
        self.byte_locations = []

    def add_incoming_byte(self, x, y):
        self.byte_locations.append(Point(x=x, y=y))

    def print(self):
        for y in range(self.size+1):
            line = []
            for x in range(self.size+1):
                point = Point(x=x, y=y)
                if point in self.corrupted:
                    line.append("#")
                elif point in self.path:
                    line.append("O")
                else:
                    line.append("_")
            print("".join(line))

    def simulate_fall(self, number_of_bytes):
        for _ in range(number_of_bytes):
            self.fall_single()
        return self

    def simulate_until_blocked(self):
        while True:
            location = self.fall_single()
            if location in self.path:
                try:
                    self.find_path()
                except NoSolution:
                    return location

    def fall_single(self):
        location = self.byte_locations.pop(0)
        self.corrupted.add(location)
        return location

    def find_path(self):
        self.path = set()
        start = Point(x=0, y=0)
        goal = Point(x=self.size, y=self.size)
        fringe = [start]
        costs = {start: 0}
        came_from = {start: None}
        while fringe:
            point = fringe.pop(0)
            if point == goal:
                point = goal
                while point is not None:
                    self.path.add(point)
                    point = came_from[point]
                return self
            else:
                for neighbour in point.neighbours():
                    if self.can_be_at(neighbour):
                        neighbour_cost = costs[point] + 1
                        if neighbour not in costs or neighbour_cost < costs[neighbour]:
                            fringe.append(neighbour)
                            costs[neighbour] = neighbour_cost
                            came_from[neighbour] = point
                fringe.sort(key=lambda point: costs[point])
        raise NoSolution("found no path")

    def can_be_at(self, point):
        return (
            point not in self.corrupted and
            0 <= point.x <= self.size and
            0 <= point.y <= self.size
        )

    def steps(self):
        return len(self.path) - 1

class NoSolution(Exception):
    pass

class Point(collections.namedtuple("Point", ["x", "y"])):

    def neighbours(self):
        for dx in [-1, 1]:
            yield self._replace(x=self.x+dx)
        for dy in [-1, 1]:
            yield self._replace(y=self.y+dy)

    def aoc_format(self):
        return f"{self.x},{self.y}"

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print("OK")
