"""
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

Part 1:

>>> Warehouse.load().move_robot().gps()
1463512

Part 2:

>>> Warehouse.load(double=True).move_robot().gps()
1486520
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
        next_point = self.point.move(movement)
        stones = self.warehouse.get(next_point).stones_to_push(movement)
        if stones is not None:
            pushed = set()
            for stone_point in stones:
                if stone_point not in pushed:
                    pushed.add(stone_point)
                    self.warehouse.get(stone_point).move(movement)
            self.point = next_point

class Stone:

    def __init__(self, point, warehouse):
        self.point = point
        self.warehouse = warehouse

    def gps(self):
        return self.point.gps()

    def stones_to_push(self, movement):
        stone_points = []
        for point in self.get_push_points(movement):
            sub = self.warehouse.get(point).stones_to_push(movement)
            if sub is None:
                return None
            else:
                stone_points.extend(sub)
        for point in self.get_my_points():
            stone_points.append(point)
        return stone_points

    def get_my_points(self):
        return [self.point]

    def move(self, movement):
        next_point = self.point.move(movement)
        self.warehouse.move_item(self, self.point, next_point)
        self.point = next_point

    def get_push_points(self, movement):
        return [self.point.move(movement)]

class LeftStone(Stone):

    def grid_representation(self):
        return "["

    def get_my_points(self):
        return [self.point, self.point.move(">")]

    def get_push_points(self, movement):
        points = [self.point.move(movement)]
        if movement in "^v":
            points.append(points[0].move(">"))
        return points

class RightStone(Stone):

    def grid_representation(self):
        return "]"

    def get_my_points(self):
        return [self.point, self.point.move("<")]

    def get_push_points(self, movement):
        points = [self.point.move(movement)]
        if movement in "^v":
            points.append(points[0].move("<"))
        return points

    def gps(self):
        return 0

class Wall:

    def grid_representation(self):
        return "#"

    def stones_to_push(self, movement):
        return None

    def gps(self):
        return 0

class Free:

    def grid_representation(self):
        return "."

    def stones_to_push(self, movement):
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

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print("OK")
