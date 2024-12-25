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
Finish(score=84, cheat1=None, cheat2=None)
>>> example.race(allow_cheat=True)
Finish(score=20, cheat1=Point(x=6, y=7), cheat2=Point(x=5, y=7))
>>> example.count_cheats_that_would_save(picoseconds=1)
44

>>> RaceTrackParser().parse().race(allow_cheat=False)
Finish(score=9416, cheat1=None, cheat2=None)
>>> RaceTrackParser().parse().race(allow_cheat=True)
Finish(score=80, cheat1=Point(x=43, y=72), cheat2=Point(x=43, y=71))

Part 1:

>>> RaceTrackParser().parse().count_cheats_that_would_save(picoseconds=100)
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
        return race_track

class RaceTrack:

    def __init__(self):
        self.walls = set()

    def add_wall(self, point):
        self.walls.add(point)

    def set_start(self, point):
        self.start = point

    def set_end(self, point):
        self.end = point

    def can_be_at(self, point):
        return point not in self.walls

    def count_cheats_that_would_save(self, picoseconds):
        return len(list(self.yield_race(
            allow_cheat=True,
            max_score=self.race(allow_cheat=False).score-picoseconds
        )))

    def race(self, allow_cheat):
        for finish in self.yield_race(allow_cheat):
            return finish
        raise ValueError("no solution found")

    def yield_race(self, allow_cheat, max_score=None):
        start = Program(point=self.start, cheat1=None, cheat2=None)
        cost = {start: 0}
        fringe = [start]
        while fringe:
            program = fringe.pop(0)
            if max_score is not None and (cost[program]+program.point.manhattan_to(self.end)) > max_score:
                continue
            if program.point == self.end:
                yield program.finish(cost[program])
            else:
                for next_program in program.moves(self, allow_cheat):
                    next_program_cost = cost[program] + 1
                    if next_program not in cost or next_program_cost < cost[program]:
                        cost[next_program] = next_program_cost
                        fringe.append(next_program)

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
            yield self._replace(y=self.y+dy)
        for dx in [-1, 1]:
            yield self._replace(x=self.x+dx)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print("OK")
