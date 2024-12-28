import collections


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

    def add(self, x, y, height):
        point = Point(x, y)
        self.cells[point] = Cell(point, height, self)

    def get(self, point):
        return self.cells.get(point, CellOutsideMap())

    def get_trailheads(self):
        return Cells([cell for cell in self.cells.values() if cell.is_trailhead()])


class Cells:

    def __init__(self, cells):
        self.cells = cells

    def sum_scores(self):
        return sum(cell.get_score() for cell in self.cells)

    def sum_ratings(self):
        return sum(cell.get_rating() for cell in self.cells)


class Cell:

    def __init__(self, point, height, topographic_map):
        self.point = point
        self.height = height
        self.topographic_map = topographic_map

    def is_trailhead(self):
        return self.has_height(0)

    def has_height(self, height):
        return self.height == height

    def get_score(self):
        return len(self.get_reachable_tops())

    def get_reachable_tops(self):
        if self.has_height(9):
            return {self.point}
        else:
            result = set()
            for point in self.point.directions():
                cell = self.topographic_map.get(point)
                if cell.has_height(self.height + 1):
                    result |= cell.get_reachable_tops()
            return result

    def get_rating(self):
        if self.has_height(9):
            return 1
        else:
            result = 0
            for point in self.point.directions():
                cell = self.topographic_map.get(point)
                if cell.has_height(self.height + 1):
                    result += cell.get_rating()
            return result

    def __repr__(self):
        return f"Cell(point={self.point!r}, height={self.height!r})"


class CellOutsideMap:

    def has_height(self, height):
        return False


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


print(TopographicMap.load().get_trailheads().sum_scores())
print(TopographicMap.load().get_trailheads().sum_ratings())
print("OK")
