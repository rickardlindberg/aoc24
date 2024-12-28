import doctest
import sys


FREE = True
OCCUPIED = False


class Position:

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def add(self, other):
        return Position(x=self.x + other.x, y=self.y + other.y)

    def as_tuple(self):
        return (self.x, self.y)


class Guard:

    DIRECTIONS = {
        "^": Position(y=-1),
        ">": Position(x=1),
        "v": Position(y=1),
        "<": Position(x=-1),
    }

    def __init__(self, position, direction):
        self.position = position
        self.direction = direction

    def visit(self, visited):
        key = (self.position.x, self.position.y, self.direction)
        if key in visited:
            return True
        else:
            visited.add(key)
            return False

    def see_obsticle(self, map_):
        return map_.is_obsticle(self.walk().position)

    def is_outside(self, map_):
        return map_.is_outside(self.position)

    def turn_right(self):
        turns = "^>v<"
        return Guard(self.position, turns[(turns.index(self.direction) + 1) % 4])

    def walk(self):
        return Guard(self.position.add(self.DIRECTIONS[self.direction]), self.direction)


class Map:

    def __init__(self):
        self.positions = {}

    def is_obsticle(self, position):
        return self.positions.get(position.as_tuple()) == OCCUPIED

    def is_outside(self, position):
        return position.as_tuple() not in self.positions

    def add(self, x, y, char):
        position = Position(x, y)
        if char == "#":
            self.positions[position.as_tuple()] = OCCUPIED
        elif char == ".":
            self.positions[position.as_tuple()] = FREE
        elif char in ["^", ">", "v", "<"]:
            self.guard = Guard(position, char)
            self.positions[position.as_tuple()] = FREE
        else:
            assert char == "\n"

    def walk_count(self):
        return len(self.walk_path())

    def walk_path(self):
        guard = self.guard
        visited = set([guard.position.as_tuple()])
        while True:
            if guard.see_obsticle(self):
                guard = guard.turn_right()
            else:
                guard = guard.walk()
                if guard.is_outside(self):
                    return visited
                else:
                    visited.add(guard.position.as_tuple())

    def walk_in_loop(self):
        guard = self.guard
        visited = set()
        guard.visit(visited)
        while True:
            if guard.see_obsticle(self):
                guard = guard.turn_right()
            else:
                guard = guard.walk()
                if guard.is_outside(self):
                    return False
                elif guard.visit(visited):
                    return True

    def alter_count(self):
        count = 0
        for key in self.walk_path():
            if self.guard.position.as_tuple() != key:
                self.positions[key] = OCCUPIED
                if self.walk_in_loop():
                    # print(f"found {key}")
                    count += 1
                self.positions[key] = FREE
        return count


map_ = Map()
for y, line in enumerate(sys.stdin):
    for x, char in enumerate(line):
        map_.add(x, y, char)
print(map_.alter_count())
doctest.testmod()

assert map_.walk_count() == 5030
assert map_.alter_count() == 1928
