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
        items, movements = text.split("\n\n")
        for y, line in enumerate(items.splitlines()):
            for x, item_type in enumerate(line):
                warehouse.add_item(x, y, item_type)
        for movement in movements:
            if movement.strip():
                warehouse.add_robot_movement(movement)
        return warehouse

    def __init__(self):
        self.items = {}
        self.robot = None

    def get(self, point):
        return self.items.get(point, Free())

    def add_item(self, x, y, item_type):
        point = Point(x, y)
        if item_type == "@":
            self.robot = Robot(point, self)
        elif item_type == "#":
            self.items[point] = Wall()
        elif item_type == "O":
            self.items[point] = Stone(point, self)
        else:
            assert item_type == "."

    def add_robot_movement(self, movement):
        self.robot.add_movement(movement)

    def move_robot(self):
        self.robot.move()
        return self

    def gps(self):
        return sum(item.gps() for item in self.items.values())

    def move_item(self, item, old_point, new_point):
        del self.items[old_point]
        self.items[new_point] = item

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
        if self.warehouse.get(next_point).can_push(movement):
            self.warehouse.get(next_point).push(movement)
            self.point = next_point

class Stone:

    def __init__(self, point, warehouse):
        self.point = point
        self.warehouse = warehouse

    def gps(self):
        return self.point.gps()

    def can_push(self, movement):
        for point in self.get_push_points(movement):
            if not self.warehouse.get(point).can_push(movement):
                return False
        return True

    def push(self, movement):
        if self.can_push(movement):
            for point in self.get_push_points(movement):
                self.warehouse.get(point).push(movement)
            next_point = self.point.move(movement)
            self.warehouse.move_item(self, self.point, next_point)
            self.point = next_point

    def get_push_points(self, movement):
        return [self.point.move(movement)]

class Wall:

    def gps(self):
        return 0

    def can_push(self, movement):
        return False

class Free:

    def can_push(self, movement):
        return True

    def push(self, movement):
        pass

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
