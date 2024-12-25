"""
>>> example = [
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
... ]
>>> memory_space = BytePositionParser().parse_lines(example, size=6).simulate_fall(12)
>>> memory_space.print()
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

    def simulate_fall(self, number_of_bytes):
        for i in range(number_of_bytes):
            self.corrupted.add(self.byte_locations.pop(0))
        return self

    def add_incoming_byte(self, x, y):
        self.byte_locations.append(Point(x=x, y=y))

    def steps(self):
        return len(self.path) - 1

    def find_path(self):
        start = Point(x=0, y=0)
        goal = Point(x=self.size, y=self.size)
        fringe = [start]
        costs = {start: 0}
        came_from = {start: None}
        while fringe:
            point = fringe.pop(0)
            if point == goal:
                self.path = set()
                node = goal
                while node is not None:
                    self.path.add(node)
                    node = came_from[node]
                return self
            else:
                for neighbour in point.neighbours():
                    if (neighbour in self.corrupted or
                        neighbour.x < 0 or
                        neighbour.x > self.size or
                        neighbour.y < 0 or
                        neighbour.y > self.size):
                        continue
                    neighbour_cost = costs[point] + 1
                    if neighbour not in costs or neighbour_cost < costs[neighbour]:
                        fringe.append(neighbour)
                        costs[neighbour] = neighbour_cost
                        came_from[neighbour] = point
                fringe.sort(key=lambda point: costs[point])
        raise ValueError(f"found no path: {costs}")

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

class Point(collections.namedtuple("Point", ["x", "y"])):

    def neighbours(self):
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            yield Point(x=self.x+dx, y=self.y+dy)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print("OK")
