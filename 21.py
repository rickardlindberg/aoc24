"""
>>> CodeParser().parse().complexity()
1356
"""

import collections

class CodeParser:

    def parse(self):
        with open("21.txt") as f:
            return self.parse_text(f.read())

    def parse_text(self, text):
        codes = Codes()
        for line in text.splitlines():
            assert len(line) == 4
            codes.add(Code(line))
        return codes

class Codes:

    def __init__(self):
        self.codes = []

    def add(self, code):
        self.codes.append(code)

    def complexity(self):
        return sum(code.complexity() for code in self.codes)

class Code:

    def __init__(self, code):
        self.code = code

    def complexity(self):
        return self.numeric_part() * self.button_presses()

    def numeric_part(self):
        """
        >>> Code("029A").numeric_part()
        29
        """
        return int(self.code.replace("A", ""))

    def button_presses(self):
        return 1

class NumericKeypad:

    """
    >>> NumericKeypad().print_state()
     7  8  9
     4  5  6
     1  2  3
        0 (A)
    """

    def __init__(self):
        self.grid = Grid.from_lines("A", [
            "789",
            "456",
            "123",
            " 0A",
        ])

    def print_state(self):
        self.grid.print()

class DirectionalKeypad:

    """
    >>> DirectionalKeypad().print_state()
        ^ (A)
     <  v  >
    """

    def __init__(self):
        self.grid = Grid.from_lines("A", [
            " ^A",
            "<v>",
        ])

    def print_state(self):
        self.grid.print()

class Grid:

    @classmethod
    def from_lines(cls, initial_state, lines):
        grid = Grid()
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                point = Point(x=x, y=y)
                if char.strip():
                    grid.add(point=point, char=char)
                if char == initial_state:
                    grid.set_state(point)
        return grid

    def __init__(self):
        self.states = {}
        self.state = None

    def print(self):
        for y in range(0, max(point.y for point in self.states)+1):
            line = []
            for x in range(0, max(point.x for point in self.states)+1):
                point = Point(x=x, y=y)
                char = self.states.get(point, " ")
                if point == self.state:
                    line.append(f"({char})")
                else:
                    line.append(f" {char} ")
            print("".join(line).rstrip())

    def set_state(self, point):
        assert point in self.states
        self.state = point

    def add(self, point, char):
        self.states[point] = char

class Point(collections.namedtuple("Point", ["x", "y"])):
    pass

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print("OK")
