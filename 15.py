"""
Part 1:

>>> Warehouse.load().move_robot().gps()
1463512
"""

import collections

class Warehouse:

    @classmethod
    def load(cls):
        with open("15.txt") as f:
            return cls.load_text(f.read())

    @classmethod
    def load_text(cls, text):
        warehouse = cls()
        objects, movements = text.split("\n\n")
        for y, line in enumerate(objects.splitlines()):
            for x, object_type in enumerate(line):
                warehouse.add_object(x, y, object_type)
        for movement in movements:
            if movement.strip():
                warehouse.add_robot_movement(movement)
        return warehouse

    def __init__(self):
        self.robot = None
        self.walls = set()
        self.stones = {}

    def get(self, point):
        if point in self.stones:
            return self.stones[point]
        elif point in self.walls:
            return Obstacle()
        else:
            return Free()

    def add_object(self, x, y, object_type):
        point = Point(x, y)
        if object_type == "@":
            self.robot = Robot(point, self)
        elif object_type == "#":
            self.walls.add(point)
        elif object_type == "O":
            self.stones[point] = Stone(point, self)
        else:
            assert object_type == "."

    def add_robot_movement(self, movement):
        self.robot.add_movement(movement)

    def move_robot(self):
        self.robot.move()
        return self

    def gps(self):
        return sum(stone.gps() for stone in self.stones.values())

    def move_stone(self, stone, old_point, new_point):
        del self.stones[old_point]
        self.stones[new_point] = stone

class Robot:

    def __init__(self, point, warehouse):
        self.point = point
        self.warehouse = warehouse
        self.movements = []

    def add_movement(self, movement):
        self.movements.append(movement)

    def move(self):
        while self.movements:
            self.eval_movement(self.movements.pop(0))

    def eval_movement(self, movement):
        next_point = self.point.move(movement)
        if self.warehouse.get(next_point).push(movement):
            self.point = next_point

class Stone:

    def __init__(self, point, warehouse):
        self.point = point
        self.warehouse = warehouse

    def gps(self):
        return self.point.gps()

    def push(self, movement):
        next_point = self.point.move(movement)
        if self.warehouse.get(next_point).push(movement):
            self.warehouse.move_stone(self, self.point, next_point)
            self.point = next_point
            return True
        else:
            return False

class Obstacle:

    def push(self, movement):
        return False

class Free:

    def push(self, movement):
        return True

class Point(collections.namedtuple("Point", ["x", "y"])):

    def move(self, movement):
        dx, dy = {
            "<": (-1, 0),
            ">": (1, 0),
            "^": (0, -1),
            "v": (0, 1),
        }[movement]
        return Point(x=self.x+dx, y=self.y+dy)

    def gps(self):
        return 100*self.y + self.x

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print("OK")
