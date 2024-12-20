"""
Example:

>>> Garden.load_text("\\n".join([
...     "AAAA",
...     "BBCD",
...     "BBCC",
...     "EEEC",
... ])).regions().count()
5

Part 1:

>>> Garden.load().regions().total_price()
1396562
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

    def area(self):
        return len(self.plants)

    def perimiter(self):
        return sum(plant.perimiter_contribution() for plant in self.plants)


class Plant:

    def __init__(self, point, plant, garden):
        self.point = point
        self.plant = plant
        self.garden = garden

    def perimiter_contribution(self):
        return sum(
            1
            for point in self.point.all_directions()
            if not self.garden.get(point).is_plant(self.plant)
        )

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
                        for point in point.all_directions()
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
        return [
            self.move(dx=1),
            self.move(dx=-1),
            self.move(dy=1),
            self.move(dy=-1),
        ]


doctest.testmod()
print("OK")
