import sys


class Pos:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def add(self, pos):
        return Pos(x=self.x + pos.x, y=self.y + pos.y)


class Grid:

    def __init__(self, data):
        self.entries = {}
        for y, line in enumerate(data.splitlines()):
            for x, char in enumerate(line):
                self.entries[(x, y)] = char

    def get(self, pos):
        return self.entries.get((pos.x, pos.y))

    def all_pos(self):
        return [Pos(x, y) for x, y in self.entries]

    def count_xmas(self):
        total = 0
        for pos in self.all_pos():
            if self.get(pos) == "X":
                for direction in self.directions():
                    if self.is_text(pos, direction, "MAS"):
                        total += 1
        return total

    def is_text(self, pos, direction, text):
        while text:
            pos = pos.add(direction)
            if self.get(pos) == text[0]:
                text = text[1:]
            else:
                return False
        return True

    def directions(self):
        return [
            Pos(-1, -1),
            Pos(0, -1),
            Pos(1, -1),
            Pos(-1, 0),
            Pos(1, 0),
            Pos(-1, 1),
            Pos(0, 1),
            Pos(1, 1),
        ]


print(Grid(sys.stdin.read()).count_xmas())
