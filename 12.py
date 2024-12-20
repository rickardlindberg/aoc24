"""
Example:

>>> example = Garden.load_text("\\n".join([
...     "AAAA",
...     "BBCD",
...     "BBCC",
...     "EEEC",
... ]))
>>> example.regions().count()
5

+-+-+-+-+
|A A A A|
+-+-+-+-+     +-+
              |D|
+-+-+   +-+   +-+
|B B|   |C|
+   +   + +-+
|B B|   |C C|
+-+-+   +-+ +
          |C|
+-+-+-+   +-+
|E E E|
+-+-+-+

Part 1:

>>> Garden.load().regions().total_price()
1396562

Part 2:

>>> Garden.load().regions().discount_price()
844132
"""

import collections
import doctest


class Garden:

    @classmethod
    def load(cls):
        with open("12.txt") as f:
            return cls.load_text(f.read())

    @classmethod
    def load_text(cls, text):
        garden = cls()
        for y, row in enumerate(text.splitlines()):
            for x, plant in enumerate(row):
                garden.add(x, y, plant)
        return garden

    def __init__(self):
        self.plants = {}

    def add(self, x, y, plant):
        point = Point(x, y)
        self.plants[point] = Plant(point=point, plant=plant, garden=self)

    def get(self, point):
        return self.plants.get(point, NoPlant())

    def regions(self):
        regions = Regions()
        visited = set()
        for point, plant in self.plants.items():
            if point not in visited:
                region = plant.region()
                region.mark_visited(visited)
                regions.add(region)
        return regions


class Regions:

    def __init__(self, regions=[]):
        self.regions = list(regions)

    def add(self, region):
        self.regions.append(region)

    def count(self):
        return len(self.regions)

    def total_price(self):
        return sum(region.price() for region in self.regions)

    def discount_price(self):
        return sum(region.discount_price() for region in self.regions)


class Region:

    def __init__(self, plants=[]):
        self.plants = list(plants)

    def add(self, plant):
        self.plants.append(plant)

    def mark_visited(self, visited):
        for plant in self.plants:
            plant.mark_visited(visited)

    def price(self):
        return self.area() * self.perimiter()

    def discount_price(self):
        return self.area() * self.number_of_sides()

    def area(self):
        return len(self.plants)

    def perimiter(self):
        return sum(plant.perimiter_contribution() for plant in self.plants)

    def number_of_sides(self):
        left = (-1, 0)
        right = (1, 0)
        up = (0, -1)
        down = (0, 1)
        directions = {
            "left": Sides(up, down),
            "right": Sides(up, down),
            "up": Sides(left, right),
            "down": Sides(left, right),
        }
        for plant in self.plants:
            for direction, point in plant.perimiter():
                directions[direction].add(point)
        return sum(sides.count() for sides in directions.values())


class Sides:

    def __init__(self, back, forward):
        self.points = []
        self.back = back
        self.forward = forward

    def add(self, point):
        self.points.append(point)

    def count(self):
        left = list(self.points)
        count = 0
        while left:
            point = left.pop(0)
            back = point.move(*self.back)
            while back in left:
                left.remove(back)
                back = back.move(*self.back)
            forward = point.move(*self.forward)
            while forward in left:
                left.remove(forward)
                forward = forward.move(*self.forward)
            count += 1
        return count


class Plant:

    def __init__(self, point, plant, garden):
        self.point = point
        self.plant = plant
        self.garden = garden

    def perimiter_contribution(self):
        return len(self.perimiter())

    def perimiter(self):
        return [
            (direction, self.point)
            for direction, point in self.point.all_directions()
            if not self.garden.get(point).is_plant(self.plant)
        ]

    def mark_visited(self, visited):
        visited.add(self.point)

    def is_plant(self, plant):
        return self.plant == plant

    def region(self):
        region = Region()
        to_visit = [self.point]
        visited = set()
        while to_visit:
            point = to_visit.pop()
            if point not in visited:
                region.add(self.garden.get(point))
                visited.add(point)
                to_visit.extend(
                    [
                        point
                        for direction, point in point.all_directions()
                        if self.garden.get(point).is_plant(self.plant)
                    ]
                )
        return region


class NoPlant:

    def is_plant(self, plant):
        return False


class Point(collections.namedtuple("Point", ["x", "y"])):

    def move(self, dx=0, dy=0):
        return Point(x=self.x + dx, y=self.y + dy)

    def all_directions(self):
        return self.vertical_directions() + self.horizontal_directions()

    def vertical_directions(self):
        return [
            ("down", self.move(dy=1)),
            ("up", self.move(dy=-1)),
        ]

    def horizontal_directions(self):
        return [
            ("right", self.move(dx=1)),
            ("left", self.move(dx=-1)),
        ]


doctest.testmod()
print("OK")
