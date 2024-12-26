"""
Examples:

>>> example = RaceTrackParser().parse_text("\\n".join([
...     "###############",
...     "#...#...#.....#",
...     "#.#.#.#.#.###.#",
...     "#S#...#.#.#...#",
...     "#######.#.#.###",
...     "#######.#.#...#",
...     "#######.#.###.#",
...     "###..E#...#...#",
...     "###.#######.###",
...     "#...###...#...#",
...     "#.#####.#.###.#",
...     "#.#...#.#.#...#",
...     "#.#.#.#.#.#.###",
...     "#...#...#...###",
...     "###############",
... ]))
>>> example.race(allow_cheat=False)
84
>>> example.race(allow_cheat=True)
20
>>> example.count_cheats_that_would_save(picoseconds=1, cheat_size=2)
44

>>> example.count_cheats_that_would_save(picoseconds=50, cheat_size=20)
285

>>> RaceTrackParser().parse().race(allow_cheat=False)
9416
>>> RaceTrackParser().parse().race(allow_cheat=True)
80

Part 1:

>>> RaceTrackParser().parse().count_cheats_that_would_save(picoseconds=100, cheat_size=2)
1286

Part 2:

>>> RaceTrackParser().parse().count_cheats_that_would_save(picoseconds=100, cheat_size=20)
989316
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
        self.cheats = set()

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
        return point in self.cheats or point in self.free

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

    def count_cheats_that_would_save(self, picoseconds, cheat_size):
        costs_to_end = self.map_costs()
        max_cost = costs_to_end[self.start]
        count = 0
        cheats = set()
        for start in costs_to_end:
            for end in costs_to_end:
                manhattan = start.manhattan_to(end)
                if 1 <= manhattan <= cheat_size:
                    cheats.add((manhattan, start, end))
        saves = {}
        for cheat_len, start, end in sorted(cheats, key=lambda x: x[0]):
            save = costs_to_end[start] - (costs_to_end[end]+cheat_len)
            if save >= picoseconds:
                if save not in saves:
                    saves[save] = 1
                else:
                    saves[save] += 1
                count += 1
        return count

    def map_costs(self):
        fringe = set([self.start])
        costs = {self.start: 0}
        came_from = {self.start: None}
        while fringe:
            point = fringe.pop()
            if point == self.end:
                for free in self.free:
                    assert free in costs
                costs_to_end = {}
                cost = 0
                point = self.end
                while point is not None:
                    costs_to_end[point] = cost
                    point = came_from[point]
                    cost += 1
                return costs_to_end
            for neighbour in point.moves():
                if self.can_be_at(neighbour):
                    neighbour_cost = costs[point] + 1
                    if neighbour not in costs or neighbour_cost < costs[neighbour]:
                        costs[neighbour] = neighbour_cost
                        came_from[neighbour] = point
                        fringe.add(neighbour)
        raise ValueError("no map cost found")

    def race(self, allow_cheat):
        if not allow_cheat:
            return self.map_costs()[self.start]
        for finish in self.yield_race(allow_cheat):
            return finish.score
        raise ValueError("no solution found")

    def yield_race(self, allow_cheat, max_score=None):
        yield from self.get_search(
            allow_cheat=allow_cheat,
            max_score=max_score
        ).run()

    def get_search(self, allow_cheat, max_score):
        return Search(
            allow_cheat=allow_cheat,
            start=self.start,
            end=self.end,
            max_score=max_score,
            race_track=self
        )

class Search:

    def __init__(self, allow_cheat, start, end, max_score, race_track):
        self.allow_cheat = allow_cheat
        self.race_track = race_track
        self.max_score = max_score
        initial = Program(point=start, cheat1=None, cheat2=None)
        self.cost = {initial: 0}
        self.came_from = {initial: None}
        self.fringe = [initial]
        self.end = end
        self.last_program = start

    def draw(self, context):
        path = set()
        node = self.last_program
        while node in self.came_from:
            path.add(node.point)
            node = self.came_from[node]
        self.race_track.draw(context, path)
        context.move_to(10, 10)
        context.set_source_rgb(0, 0, 0)
        context.show_text(f"{len(self.fringe)}")

    def run(self):
        while self.fringe:
            value = self.step()
            if value is not None:
                yield value

    def step(self):
        if self.fringe:
            program = self.fringe.pop(0)
            self.last_program = program
            if self.max_score is not None and self.cost[program] > self.max_score:
                return
            if program.point == self.end:
                return program.finish(self.cost[program])
            else:
                for next_program in program.moves(self.race_track, self.allow_cheat):
                    next_program_cost = self.cost[program] + 1
                    if next_program not in self.cost or next_program_cost < self.cost[program]:
                        self.cost[next_program] = next_program_cost
                        self.fringe.append(next_program)
                        self.came_from[next_program] = program

class Program(collections.namedtuple("Program", ["point", "cheat1", "cheat2"])):

    def finish(self, score):
        return Finish(score=score, cheat1=self.cheat1, cheat2=self.cheat2)

    def moves(self, race_track, allow_cheat):
        for point in self.point.moves():
            if allow_cheat and self.cheat1 is None and not race_track.can_be_at(point):
                yield self._replace(point=point, cheat1=point)
            if race_track.can_be_at(point):
                if self.cheat1 and not self.cheat2:
                    cheat2 = point
                else:
                    cheat2 = self.cheat2
                yield self._replace(point=point, cheat2=cheat2)

class Finish(collections.namedtuple("Finish", ["score", "cheat1", "cheat2"])):
    pass

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
        self.state.step()
        widget.queue_draw()

if __name__ == "__main__":
    import sys
    if "interactive" in sys.argv[1:]:
        import gi
        gi.require_version("Gtk", "3.0")
        from gi.repository import Gtk
        Animation(RaceTrackParser().parse().get_search(
            allow_cheat=False,
            max_score=9416
        )).run()
    else:
        import doctest
        doctest.testmod()
        print("OK")
