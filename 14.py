"""
Examples:

>>> Robot.load_text("p=41,24 v=-55,25")
Robot(position=Point(x=41, y=24), velocity=Point(x=-55, y=25)

>>> Point(2, 4).add(Point(2, -3)).add(Point(2, -3)).wrap(11, 7)
Point(x=6, y=5)

>>> Robots.load().count_repetitive()
{10403}

Part 1:

>>> Robots.load().elapse(100).safety_factor()
222901875

Part 2:

>>> Robots.load().elapse(6243).print()
"""

import collections
import doctest


class Robots:

    @classmethod
    def load(cls):
        with open("14.txt") as f:
            return cls.load_text(f.read(), 101, 103)

    @classmethod
    def load_text(cls, text, width, height):
        return cls(
            robots=[Robot.load_text(line) for line in text.splitlines()],
            width=width,
            height=height,
        )

    def __init__(self, robots, width, height):
        self.robots = list(robots)
        self.width = width
        self.height = height

    def find_christmas_tree_iterations(self):
        iterations = 0
        while not self.is_christmas_tree():
            self.elapse(1)
            iterations += 1
        self.print()
        return iterations

    def is_christmas_tree(self):
        return True

    def draw(self, context):
        size = 3
        counts = {}
        for robot in self.robots:
            counts[robot.position] = counts.get(robot.position, 0) + 1
        for y in range(self.height):
            chars = []
            for x in range(self.width):
                point = Point(x, y)
                if point in counts:
                    context.rectangle(x * size, y * size, size, size)
                    context.fill()

    def print(self):
        counts = {}
        for robot in self.robots:
            counts[robot.position] = counts.get(robot.position, 0) + 1
        for y in range(self.height):
            chars = []
            for x in range(self.width):
                point = Point(x, y)
                if point in counts:
                    if counts[point] <= 9:
                        chars.append(str(counts[point]))
                    else:
                        chars.append("X")
                else:
                    chars.append(".")
            print("".join(chars))

    def add(self, robot):
        self.robots.append(robot)

    def elapse(self, seconds):
        for robot in self.robots:
            robot.elapse(seconds, self.width, self.height)
        return self

    def count_repetitive(self):
        return set(
            [robot.count_repetitive(self.width, self.height) for robot in self.robots]
        )

    def quadrants(self):
        XXX = Rectangle(Point(0, 0), Point(self.width, self.height))
        quadrants = {}
        for quadrant in XXX.get_quadrants():
            quadrants[quadrant] = Robots([], self.width, self.height)
        for robot in self.robots:
            for quadrant, robots in quadrants.items():
                if robot.inside(quadrant):
                    robots.add(robot)
        return list(quadrants.values())

    def count_robots(self):
        return len(self.robots)

    def safety_factor(self):
        product = 1
        for quadrant in self.quadrants():
            product *= quadrant.count_robots()
        return product


class Robot:

    @classmethod
    def load_text(cls, text):
        position_part, velocity_part = text.split(" ")
        assert position_part.startswith("p=")
        assert velocity_part.startswith("v=")
        position_parts = position_part[2:].split(",")
        velocity_parts = velocity_part[2:].split(",")
        return cls(
            position=Point(*[int(x) for x in position_parts]),
            velocity=Point(*[int(x) for x in velocity_parts]),
        )

    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity

    def inside(self, quadrant):
        return quadrant.contains(self.position)

    def elapse(self, seconds, width, height):
        for _ in range(seconds):
            self.position = self.position.add(self.velocity).wrap(width, height)

    def count_repetitive(self, width, height):
        position = self.position
        count = 0
        while True:
            position = position.add(self.velocity).wrap(width, height)
            count += 1
            if position == self.position:
                return count

    def __repr__(self):
        return f"Robot(position={self.position}, velocity={self.velocity!r}"


class Rectangle(collections.namedtuple("Rectangle", ["start", "size"])):

    def contains(self, point):
        return (self.start.x <= point.x <= (self.start.x + self.size.x - 1)) and (
            self.start.y <= point.y <= (self.start.y + self.size.y - 1)
        )

    def get_quadrants(self):
        assert self.size.x % 2 == 1
        assert self.size.y % 2 == 1
        quadrant_size = Point(x=(self.size.x - 1) // 2, y=(self.size.y - 1) // 2)
        return [
            Rectangle(start=self.start, size=quadrant_size),
            Rectangle(
                start=self.start.move(dx=quadrant_size.x + 1), size=quadrant_size
            ),
            Rectangle(
                start=self.start.move(dy=quadrant_size.y + 1), size=quadrant_size
            ),
            Rectangle(
                start=self.start.move(dx=quadrant_size.x + 1, dy=quadrant_size.y + 1),
                size=quadrant_size,
            ),
        ]


class Point(collections.namedtuple("Point", ["x", "y"])):

    def add(self, other):
        return Point(x=self.x + other.x, y=self.y + other.y)

    def move(self, dx=0, dy=0):
        return Point(x=self.x + dx, y=self.y + dy)

    def wrap(self, x, y):
        new_x = self.x
        if new_x >= x:
            new_x -= x
        elif new_x < 0:
            new_x += x
        new_y = self.y
        if new_y >= y:
            new_y -= y
        elif new_y < 0:
            new_y += y
        return Point(x=new_x, y=new_y)


def simulate():
    x = {0: 0}

    def draw(widget, context):
        print(x[0])
        context.set_source_rgb(1, 0.7, 1)
        context.paint()
        context.set_source_rgb(0, 0, 0)
        robots.draw(context)
        robots.elapse(1)
        x[0] += 1
        canvas.queue_draw()
        import time

        time.sleep(4.9)

    import gi

    gi.require_version("Gtk", "3.0")
    from gi.repository import Gtk
    from gi.repository import Gdk

    robots = Robots.load()
    robots.elapse(6243)

    window = Gtk.Window()
    window.connect("destroy", Gtk.main_quit)
    canvas = Gtk.DrawingArea()
    canvas.connect("draw", draw)
    window.add(canvas)
    window.show_all()
    Gtk.main()


doctest.testmod()
print("OK")
# simulate()
