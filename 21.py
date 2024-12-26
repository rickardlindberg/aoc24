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
        return ButtonPressSearch().find_shortest_to(self.code)

class ButtonPressSearch:

    """
    >>> ButtonPressSearch().find_shortest_to("9")
    1
    """

    def find_shortest_to(self, numeric):
        start = ButtonSearchState(robot1="A", robot2="A", numeric="A", out="")
        end = ButtonSearchState(robot1="A", robot2="A", numeric="A", out=numeric)
        fringe = [start]
        costs = {start: 0}
        while fringe:
            state = fringe.pop(0)
            if state == end:
                return costs[state]
            for neighbour in state.neighbours():
                neighbour_cost = costs[state] + 1
                if neighbour not in costs or neighbour_cost < costs[neighbour]:
                    costs[neighbour] = neighbour_cost
                    fringe.append(neighbour)
            fringe.sort(key=lambda state: costs[state] + state.estimate_left(end))
        return 1 # TODO: raise exception

class ButtonSearchState(collections.namedtuple("ButtonSearchState", ["robot1", "robot2", "numeric", "out"])):

    """
    you -> robot1 -> robot2 -> numeric
    """

    def neighbours(self):
        return []
        #for my_press in ["<", ">", "^", "v"]:
        #    yield self._replace(you=my_press)
        #    yield self._replace(you="A")

        #numeric = NumericKeypad()
        #directional = DirectionalKeypad()

    def estimate_left(self, goal):
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

    def can_do(self, state, action):
        return action in {
            "7": "A>v",
            "8": "A<>v",
            "9": "A<v",
            "4": "A>^v",
            "5": "A<>^v",
            "6": "A<^v",
            "1": "A>^",
            "2": "A<>^v",
            "3": "A<^v",
            "0": "A>^",
            "A": "A<^",
        }[state]

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

    def can_do(self, state, action):
        return action in {
            "^": "A>v",
            "A": "A<v",
            "<": "A>",
            "v": "A<>^",
            ">": "A<^",
        }[state]

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

    def neighbours(self):
        for dx in [-1, 1]:
            yield self._replace(x=self.x+dx)
        for dy in [-1, 1]:
            yield self._replace(y=self.y+dy)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print("OK")
