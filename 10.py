"""
"""

import collections
import doctest


class TopographicMap:

    @classmethod
    def load(cls):
        with open("10.txt") as f:
            return cls.load_text(f.read())

    @classmethod
    def load_text(cls, text):
        topographic_map = cls()
        for y, row in enumerate(text.splitlines()):
            for x, height in enumerate(row):
                topographic_map.add(x, y, int(height))
        return topographic_map

    def __init__(self):
        self.cells = {}

    def get(self, point):
        return self.cells.get(point, OutOfMapCell())

    def add(self, x, y, height):
        point = Point(x, y)
        self.cells[point] = Cell(point, height, self)

    def trailhead_scores(self):
        return sum(cell.get_score() for cell in self.get_trailheads())

    def get_trailheads(self):
        return [cell for cell in self.cells.values() if cell.is_trailhead()]


class OutOfMapCell:

    def is_height(self, height):
        return False


class Cell:

    def __init__(self, point, height, topographic_map):
        self.point = point
        self.height = height
        self.topographic_map = topographic_map

    def is_trailhead(self):
        return self.height == 0

    def is_height(self, height):
        return self.height == height

    def get_score(self):
        return len(self.get_tops())

    def get_tops(self):
        if self.height == 9:
            return {self.point}
        else:
            result = set()
            for cell in [
                self.topographic_map.get(point) for point in self.point.directions()
            ]:
                if cell.is_height(self.height + 1):
                    result |= cell.get_tops()
            return result

    def __repr__(self):
        return f"Cell(point={self.point!r}, height={self.height!r})"


class Point(collections.namedtuple("Point", ["x", "y"])):

    def directions(self):
        return [
            self.move(dx=-1),
            self.move(dx=1),
            self.move(dy=-1),
            self.move(dy=1),
        ]

    def move(self, dx=0, dy=0):
        return Point(x=self.x + dx, y=self.y + dy)


print("OK")
print(TopographicMap.load().trailhead_scores())
doctest.testmod()

# 1344 too high
