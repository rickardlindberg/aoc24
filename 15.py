"""
Part 1:

>>> Warehouse.load().move_robot().gps()
1463512

Part 2:

>>> Warehouse.load(double=True).move_robot().gps()
1486520

Examples:

>>> lines = [
...     "#####",
...     "#...#",
...     "#.O.#",
...     "#.O.#",
...     "#.@.#",
...     "#####",
...     "",
...     "^",
... ]
>>> warehouse = Warehouse.load_text("\\n".join(lines), double=True)
>>> warehouse.print()
##########
##......##
##..[]..##
##..[]..##
##..@...##
##########
>>> warehouse.move_robot().print()
##########
##..[]..##
##..[]..##
##..@...##
##......##
##########
"""

import collections

class Warehouse:

    @classmethod
    def load(cls, double=False):
        with open("15.txt") as f:
            return cls.load_text(f.read(), double)

    @classmethod
    def load_text(cls, text, double=False):
        warehouse = cls()
        items, movements = text.split("\n\n")
        for y, line in enumerate(items.splitlines()):
            for x, item_type in enumerate(line):
                if double:
                    warehouse.add_double_item(x, y, item_type)
                else:
                    warehouse.add_item(x, y, item_type)
        for movement in movements:
            if movement.strip():
                warehouse.add_robot_movement(movement)
        return warehouse

    def __init__(self):
        self.items = {}
        self.robot = None

    def print(self):
        for y in range(max(point.y for point in self.items)+1):
            line = []
            for x in range(max(point.x for point in self.items)+1):
                line.append(self.get(Point(x, y)).grid_representation())
            print("".join(line))

    def get(self, point):
        if point == self.robot.point:
            return self.robot
        else:
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

    def add_double_item(self, x, y, item_type):
        point = Point(x*2, y)
        point_right = point.move(">")
        if item_type == "@":
            self.robot = Robot(point, self)
        elif item_type == "#":
            self.items[point] = Wall()
            self.items[point_right] = Wall()
        elif item_type == "O":
            self.items[point] = LeftStone(point, self)
            self.items[point_right] = RightStone(point_right, self)
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

    def grid_representation(self):
        return "@"

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
        try:
            pushed = set()
            next_point = self.point.move(movement)
            for item_point in self.warehouse.get(next_point).push(movement):
                if item_point not in pushed:
                    pushed.add(item_point)
                    self.warehouse.get(item_point).move(movement)
            self.point = next_point
        except InvalidPush:
            pass

class Stone:

    def __init__(self, point, warehouse):
        self.point = point
        self.warehouse = warehouse

    def gps(self):
        return self.point.gps()

    def push(self, movement):
        return self.warehouse.get(self.point.move(movement)).push(movement)+[self.point]

    def move(self, movement):
        next_point = self.point.move(movement)
        self.warehouse.move_item(self, self.point, next_point)
        self.point = next_point

class LeftStone:

    def __init__(self, point, warehouse):
        self.point = point
        self.warehouse = warehouse

    def grid_representation(self):
        return "["

    def gps(self):
        return self.point.gps()

    def push(self, movement):
        push_point = self.point.move(movement)
        stone_points = []
        stone_points.extend(self.warehouse.get(push_point).push(movement))
        if movement in "^v":
            stone_points.extend(self.warehouse.get(push_point.move(">")).push(movement))
        stone_points.extend([self.point, self.point.move(">")])
        return stone_points

    def move(self, movement):
        next_point = self.point.move(movement)
        self.warehouse.move_item(self, self.point, next_point)
        self.point = next_point

class RightStone:

    def __init__(self, point, warehouse):
        self.point = point
        self.warehouse = warehouse

    def grid_representation(self):
        return "]"

    def gps(self):
        return 0

    def push(self, movement):
        push_point = self.point.move(movement)
        stone_points = []
        stone_points.extend(self.warehouse.get(push_point).push(movement))
        if movement in "^v":
            stone_points.extend(self.warehouse.get(push_point.move("<")).push(movement))
        stone_points.extend([self.point, self.point.move("<")])
        return stone_points

    def move(self, movement):
        next_point = self.point.move(movement)
        self.warehouse.move_item(self, self.point, next_point)
        self.point = next_point

class Wall:

    def grid_representation(self):
        return "#"

    def gps(self):
        return 0

    def push(self, movement):
        raise InvalidPush()

class Free:

    def grid_representation(self):
        return "."

    def push(self, movement):
        return []

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

class InvalidPush(Exception):
    pass

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print("OK")
