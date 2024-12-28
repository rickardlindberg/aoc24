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

    def turn_right(self):
        turns = "^>v<"
        return Guard(self.position, turns[(turns.index(self.direction) + 1) % 4])

    def walk(self):
        return Guard(self.position.add(self.DIRECTIONS[self.direction]), self.direction)


class Map:

    def __init__(self):
        self.positions = {}

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
        guard = self.guard
        visited = set([guard.position.as_tuple()])
        while True:
            next_guard = guard.walk()
            if next_guard.position.as_tuple() not in self.positions:
                return len(visited)
            elif self.positions[next_guard.position.as_tuple()] == OCCUPIED:
                guard = guard.turn_right()
            else:
                guard = next_guard
                visited.add(guard.position.as_tuple())


map_ = Map()
for y, line in enumerate(sys.stdin):
    for x, char in enumerate(line):
        map_.add(x, y, char)
print(map_.walk_count())
doctest.testmod()

# 5553 too high
# 5029 too low
# 5030 OK
