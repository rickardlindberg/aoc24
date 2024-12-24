"""
Examples:

>>> MazeParser().parse_text(small).solve().score
7036

Part 1:

>>> MazeParser().parse().solve().score
65436
"""

small = "\n".join([
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
])

import collections

class MazeParser:

    def parse(self):
        with open("16.txt") as f:
            return self.parse_text(f.read())

    def parse_text(self, text):
        maze = Maze()
        for y, row in enumerate(text.splitlines()):
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
        self.walls = {}

    def add_wall(self, point):
        self.walls[point] = True

    def mark_start(self, point, direction):
        self.start = Reindeer(point=point, direction=direction, score=0)

    def mark_end(self, point):
        self.end = point

    def is_free(self, point):
        return point not in self.walls

    def is_finished(self, point):
        return point == self.end

    def print(self, mark=[]):
        for row in self.max_point().rows():
            line = []
            for point in row.columns():
                if point in mark:
                    line.append("*")
                elif point in self.walls:
                    line.append("#")
                elif point == self.end:
                    line.append("E")
                elif point == self.start.point:
                    line.append("S")
                else:
                    line.append(".")
            print("".join(line))

    def max_point(self):
        max_point = Point(x=0, y=0)
        for point in list(self.walls.keys()) + [self.start.point, self.end]:
            max_point = max_point.max(point)
        return max_point

    def solve(self):
        assert self.start is not None
        assert self.end is not None
        search_space = ReindeerSearchSpace.from_start_end(self.start, self.end)
        while True:
            reindeer = search_space.get_best()
            if reindeer.is_finished(self):
                return reindeer
            else:
                search_space.extend(reindeer.moves(self))

class ReindeerSearchSpace:

    @classmethod
    def from_start_end(cls, reindeer, end):
        return cls([reindeer], end)

    def __init__(self, reindeers, end):
        self.reindeers = []
        self.end = end
        self.states = {}
        self.extend(reindeers)

    def get_best(self):
        self.reindeers.sort(
            key=lambda reindeer: reindeer.optimal_score_to(self.end)
        )
        return self.reindeers.pop(0)

    def extend(self, reindeers):
        for reindeer in reindeers:
            state = (reindeer.point, reindeer.direction)
            score = reindeer.optimal_score_to(self.end)
            if state not in self.states or score < self.states[state]:
                self.states[state] = score
                self.reindeers.append(reindeer)

class Point(collections.namedtuple("Point", ["x", "y"])):

    def distance_to(self, other):
        return abs(self.x-other.x) + abs(self.y-other.y)

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

class Reindeer(collections.namedtuple("Reindeer", ["point", "direction", "score"])):

    def optimal_score_to(self, end):
        return self.score + self.point.distance_to(end)

    def moves(self, maze):
        return [
            reindeer
            for reindeer in [
                self.rotate_clockwise(),
                self.rotate_counterclockwise(),
                self.walk(),
            ]
            if reindeer.is_valid(maze)
        ]

    def is_valid(self, maze):
        return maze.is_free(self.point)

    def is_finished(self, maze):
        return maze.is_finished(self.point)

    def rotate_clockwise(self):
        return self._replace(
            direction=self.direction.rotate_clockwise(),
            score=self.score+1000,
        )

    def rotate_counterclockwise(self):
        return self._replace(
            direction=self.direction.rotate_counterclockwise(),
            score=self.score+1000,
        )

    def walk(self):
        return self._replace(
            point=self.direction.move(self.point),
            score=self.score+1,
        )

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print("OK")
