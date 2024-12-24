"""
Examples:

>>> solution = MazeParser().parse_lines(small).solve()
>>> len(solution.trail)
45
>>> solution.cost
7036

Part 1/2 common:

>>> solution = MazeParser().parse().solve()

Part 1:

>>> solution.cost
65436

Part 2:

>>> len(solution.trail)
489
"""

small = [
    "###############",
    "#.......#....E#",
    "#.#.###.#.###.#",
    "#.....#.#...#.#",
    "#.###.#####.#.#",
    "#.#.#.......#.#",
    "#.#.#####.###.#",
    "#...........#.#",
    "###.#.#####.#.#",
    "#...#.....#.#.#",
    "#.#.#.###.#.#.#",
    "#.....#...#.#.#",
    "#.###.#.#.#.#.#",
    "#S..#.....#...#",
    "###############",
]

empty = [
    "###############",
    "#............E#",
    "#.............#",
    "#.............#",
    "#.............#",
    "#.............#",
    "#.............#",
    "#.............#",
    "#.............#",
    "#.............#",
    "#.............#",
    "#.............#",
    "#.............#",
    "#S............#",
    "###############",
]

import collections
import sys
import time

class MazeParser:

    def parse(self):
        with open("16.txt") as f:
            return self.parse_lines(f.read().splitlines())

    def parse_lines(self, lines):
        maze = Maze()
        for y, row in enumerate(lines):
            for x, tile in enumerate(row):
                point = Point(x=x, y=y)
                if tile == "#":
                    maze.add_wall(point)
                elif tile == "S":
                    maze.mark_start(point, Direction.east())
                elif tile == "E":
                    maze.mark_end(point)
                else:
                    assert tile == "."
        return maze

class Maze:

    def __init__(self):
        self.start = None
        self.end = None
        self.walls = set()

    def add_wall(self, point):
        self.walls.add(point)

    def mark_start(self, point, direction):
        self.start = Reindeer(point=point, direction=direction)

    def mark_end(self, point):
        self.end = point

    def is_free(self, point):
        return point not in self.walls

    def is_end(self, point):
        return point == self.end

    def print(self, trail=[]):
        for row in self.max_point().rows():
            line = []
            for point in row.columns():
                if point in trail:
                    line.append(".")
                elif point in self.walls:
                    line.append("#")
                elif point == self.end:
                    line.append("E")
                elif point == self.start.point:
                    line.append("S")
                else:
                    line.append(" ")
            print("".join(line))

    def max_point(self):
        max_point = Point(x=0, y=0)
        for point in list(self.walls) + [self.start.point, self.end]:
            max_point = max_point.max(point)
        return max_point

    def solve(self, interactive=False):
        assert self.start is not None
        assert self.end is not None
        return ReindeerSearch(
            maze=self,
            reindeer=self.start,
        ).find_all(interactive)

class Reindeer(collections.namedtuple("Reindeer", ["point", "direction"])):

    def moves(self, maze):
        return [
            move
            for move in [
                Move(cost=1000, reindeer=self.rotate_clockwise()),
                Move(cost=1000, reindeer=self.rotate_counterclockwise()),
                Move(cost=1, reindeer=self.walk()),
            ]
            if move.is_possible(maze)
        ]

    def is_end(self, maze):
        return maze.is_end(self.point)

    def on_free_spot(self, maze):
        return maze.is_free(self.point)

    def rotate_clockwise(self):
        return self._replace(
            direction=self.direction.rotate_clockwise(),
        )

    def rotate_counterclockwise(self):
        return self._replace(
            direction=self.direction.rotate_counterclockwise(),
        )

    def walk(self):
        return self._replace(
            point=self.direction.move(self.point),
        )

class Move:

    def __init__(self, cost, reindeer):
        self.cost = cost
        self.reindeer = reindeer

    def is_possible(self, maze):
        return self.reindeer.on_free_spot(maze)

class ReindeerSearch:

    GOAL = None

    def __init__(self, maze, reindeer):
        self.maze = maze
        self.fringe = [reindeer]
        self.cost = {reindeer: 0}
        self.came_from = {reindeer: []}

    def find_all(self, interactive):
        while self.fringe:
            reindeer = self.fringe.pop(0)
            if interactive:
                self.maze.print(trail=self.trail(reindeer))
                time.sleep(0.1)
            self.process(reindeer)
        if interactive:
            self.maze.print(trail=self.trail(self.GOAL))
        return Solution(
            trail=self.trail(self.GOAL),
            cost=self.cost[self.GOAL],
        )

    def process(self, reindeer):
        if reindeer == self.GOAL:
            pass
        else:
            if reindeer.is_end(self.maze):
                moves = [Move(cost=0, reindeer=self.GOAL)]
            else:
                moves = reindeer.moves(self.maze)
            for move in moves:
                neighbour = move.reindeer
                move_cost = self.cost[reindeer] + move.cost
                if self.GOAL in self.cost and move_cost > self.cost[self.GOAL]:
                    pass
                elif neighbour not in self.cost:
                    self.came_from[neighbour] = [reindeer]
                    self.cost[neighbour] = move_cost
                    self.fringe.append(neighbour)
                    self.fringe.sort(key=lambda x: self.cost[x])
                elif move_cost < self.cost[neighbour]:
                    self.came_from[neighbour].append(reindeer)
                    self.cost[neighbour] = move_cost
                    self.fringe.append(neighbour)
                    self.fringe.sort(key=lambda x: self.cost[x])
                elif move_cost <= self.cost[neighbour]:
                    self.came_from[neighbour].append(reindeer)

    def trail(self, reindeer):
        trail = set()
        if reindeer != self.GOAL:
            trail.add(reindeer.point)
        for previous in self.came_from.get(reindeer, []):
            trail |= self.trail(previous)
        return trail

class Solution:

    def __init__(self, trail, cost):
        self.trail = trail
        self.cost = cost

class Point(collections.namedtuple("Point", ["x", "y"])):

    def max(self, other):
        return Point(x=max(self.x, other.x), y=max(self.y, other.y))

    def move(self, dx, dy):
        return self._replace(x=self.x+dx, y=self.y+dy)

    def rows(self):
        for y in range(self.y+1):
            yield Point(x=self.x, y=y)

    def columns(self):
        for x in range(self.x+1):
            yield Point(x=x, y=self.y)

class Direction(collections.namedtuple("Direction", ["direction"])):

    EAST = 0
    SOUTH = 1
    WEST = 2
    NORTH = 3

    @classmethod
    def east(cls):
        return cls(cls.EAST)

    def rotate_clockwise(self):
        return self._replace(direction=(self.direction+1)%4)

    def rotate_counterclockwise(self):
        return self._replace(direction=(self.direction-1)%4)

    def move(self, point):
        dx = {self.EAST: 1, self.WEST: -1}.get(self.direction, 0)
        dy = {self.SOUTH: 1, self.NORTH: -1}.get(self.direction, 0)
        return point.move(dx=dx, dy=dy)

if __name__ == "__main__":
    if "interactive" in sys.argv[1:]:
        MazeParser().parse_lines(small).solve(interactive=True)
    import doctest
    doctest.testmod()
    print("OK")
