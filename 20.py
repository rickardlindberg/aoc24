"""
Examples:

>>> race_results = RaceTrackParser().parse_text(example).race()

>>> race_results.print(
...     maximum_cheat_duration=2,
...     minimum_picoseconds_saved=1,
... )
Best score = 84
Best cheat score = 20
Cheats:
- 14 save 2 picoseconds
- 14 save 4 picoseconds
- 2 save 6 picoseconds
- 4 save 8 picoseconds
- 2 save 10 picoseconds
- 3 save 12 picoseconds
- 1 save 20 picoseconds
- 1 save 36 picoseconds
- 1 save 38 picoseconds
- 1 save 40 picoseconds
- 1 save 64 picoseconds
Total: 44

>>> race_results.print(
...     maximum_cheat_duration=20,
...     minimum_picoseconds_saved=50,
... )
Best score = 84
Best cheat score = 8
Cheats:
- 32 save 50 picoseconds
- 31 save 52 picoseconds
- 29 save 54 picoseconds
- 39 save 56 picoseconds
- 25 save 58 picoseconds
- 23 save 60 picoseconds
- 20 save 62 picoseconds
- 19 save 64 picoseconds
- 12 save 66 picoseconds
- 14 save 68 picoseconds
- 12 save 70 picoseconds
- 22 save 72 picoseconds
- 4 save 74 picoseconds
- 3 save 76 picoseconds
Total: 285

Part 1:

>>> RaceTrackParser().parse().race().count_cheats(
...     maximum_cheat_duration=2,
...     minimum_picoseconds_saved=100,
... )
1286

Part 2:

>>> RaceTrackParser().parse().race().count_cheats(
...     maximum_cheat_duration=20,
...     minimum_picoseconds_saved=100,
... )
989316
"""

example = """\
###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############
"""

import collections

class RaceTrackParser:

    def parse(self):
        with open("20.txt") as f:
            return self.parse_text(f.read())

    def parse_text(self, text):
        race_track = RaceTrack()
        for y, row in enumerate(text.splitlines()):
            for x, tile in enumerate(row):
                point = Point(x=x, y=y)
                if tile == "#":
                    race_track.add_wall(point)
                elif tile == "S":
                    race_track.set_start(point)
                elif tile == "E":
                    race_track.set_end(point)
                else:
                    assert tile == "."
                    race_track.add_free(point)
        return race_track

class RaceTrack:

    def __init__(self):
        self.walls = set()
        self.free = set()

    def add_wall(self, point):
        self.walls.add(point)

    def add_free(self, point):
        self.free.add(point)

    def set_start(self, point):
        self.start = point
        self.add_free(point)

    def set_end(self, point):
        self.end = point
        self.add_free(point)

    def can_be_at(self, point):
        return point in self.free

    def draw(self, context, path):
        offset = 3
        size = 5
        for point in self.walls:
            context.rectangle((point.x+offset)*size, (point.y+offset)*size, size, size)
        context.set_source_rgb(0, 0, 0)
        context.fill()
        for point in path:
            context.rectangle((point.x+offset)*size, (point.y+offset)*size, size, size)
        context.set_source_rgb(1, 0, 0)
        context.fill()

    def race(self):
        return RaceResults(self.map_cost_search().run(), self.start)

    def map_cost_search(self):
        return MapCostSearch(
            start=self.start,
            end=self.end,
            race_track=self
        )

class MapCostSearch:

    def __init__(self, start, end, race_track):
        self.fringe = set([start])
        self.costs = {start: 0}
        self.came_from = {start: None}
        self.end = end
        self.race_track = race_track
        self.last_point = None

    def draw(self, context):
        path = set()
        point = self.last_point
        while point in self.came_from:
            path.add(point)
            point = self.came_from[point]
        self.race_track.draw(context, path)
        context.move_to(10, 10)
        context.set_source_rgb(0, 0, 0)
        context.show_text(f"{len(self.fringe)}")

    def run(self):
        while self.can_step():
            result = self.step()
            if result is not None:
                return result
        raise ValueError("no map cost found")

    def can_step(self):
        return self.fringe

    def step(self):
        self.last_point = point = self.fringe.pop()
        if point == self.end:
            for free in self.race_track.free:
                assert free in self.costs
            costs_to_end = {}
            cost = 0
            point = self.end
            while point is not None:
                costs_to_end[point] = cost
                point = self.came_from[point]
                cost += 1
            return costs_to_end
        for neighbour in point.moves():
            if self.race_track.can_be_at(neighbour):
                neighbour_cost = self.costs[point] + 1
                if neighbour not in self.costs or neighbour_cost < self.costs[neighbour]:
                    self.costs[neighbour] = neighbour_cost
                    self.came_from[neighbour] = point
                    self.fringe.add(neighbour)

class RaceResults:

    def __init__(self, costs_to_end, start):
        self.costs_to_end = costs_to_end
        self.start = start

    def print(self, **kwargs):
        cheat_scores = self.cheat_scores(**kwargs)
        print(f"Best score = {self.score()}")
        print(f"Best cheat score = {self.score()-cheat_scores.best()}")
        print("Cheats:")
        cheat_scores.print()

    def score(self):
        return self.costs_to_end[self.start]

    def count_cheats(self, **kwargs):
        return self.cheat_scores(**kwargs).count()

    def cheat_scores(self, maximum_cheat_duration, minimum_picoseconds_saved):
        cheat_scores = CheatScores()
        for start in self.costs_to_end:
            for end in self.costs_to_end:
                manhattan = start.manhattan_to(end)
                if 1 <= manhattan <= maximum_cheat_duration:
                    save = self.costs_to_end[start] - (self.costs_to_end[end]+manhattan)
                    if save >= minimum_picoseconds_saved:
                        cheat_scores.add(save)
        return cheat_scores

class CheatScores:

    def __init__(self):
        self.scores = {}

    def print(self):
        for saved in sorted(self.scores.keys()):
            print(f"- {self.scores[saved]} save {saved} picoseconds")
        print(f"Total: {self.count()}")

    def add(self, points_saved):
        if points_saved not in self.scores:
            self.scores[points_saved] = 1
        else:
            self.scores[points_saved] += 1

    def best(self):
        return max(self.scores.keys())

    def count(self):
        return sum(self.scores.values())

class Point(collections.namedtuple("Point", ["x", "y"])):

    def manhattan_to(self, other):
        return abs(self.x-other.x) + abs(self.y-other.y)

    def moves(self):
        for dy in [-1, 1]:
            yield self.move(dy=dy)
        for dx in [-1, 1]:
            yield self.move(dx=dx)

    def move(self, dx=0, dy=0):
        return self._replace(x=self.x+dx, y=self.y+dy)

class Animation:

    def __init__(self, state):
        self.state = state

    def run(self):
        window = Gtk.Window()
        window.connect("destroy", Gtk.main_quit)
        canvas = Gtk.DrawingArea()
        canvas.connect("draw", self.draw)
        window.add(canvas)
        window.show_all()
        Gtk.main()

    def draw(self, widget, context):
        context.set_source_rgb(1, 0.7, 1)
        context.paint()
        context.set_source_rgb(0, 0, 0)
        self.state.draw(context)
        if self.state.can_step():
            self.state.step()
            widget.queue_draw()

if __name__ == "__main__":
    import sys
    if "interactive" in sys.argv[1:]:
        import gi
        gi.require_version("Gtk", "3.0")
        from gi.repository import Gtk
        Animation(RaceTrackParser().parse().map_cost_search()).run()
    else:
        import doctest
        doctest.testmod()
        print("OK")
