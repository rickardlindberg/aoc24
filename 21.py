"""
Part 1:

>>> CodeParser().parse().complexity(number_of_robot_keypads=2)
94426

Part 2:

#>>> CodeParser().parse().complexity(number_of_robot_keypads=25)
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

    def complexity(self, number_of_robot_keypads):
        return sum(
            code.complexity(number_of_robot_keypads=number_of_robot_keypads)
            for code in self.codes
        )

class Code:

    def __init__(self, code):
        self.code = code

    def complexity(self, number_of_robot_keypads):
        return self.numeric_part() * self.button_presses(number_of_robot_keypads)

    def numeric_part(self):
        """
        >>> Code("029A").numeric_part()
        29
        """
        return int(self.code.replace("A", ""))

    def button_presses(self, number_of_robot_keypads):
        return ButtonPressSearch().find_shortest_to(
            code=self.code,
            number_of_robot_keypads=number_of_robot_keypads,
        )

class ButtonPressSearch:

    """
    >>> ButtonPressSearch().find_shortest_to(code="A", number_of_robot_keypads=2)
    1
    """

    def find_shortest_to(self, code, number_of_robot_keypads):
        start = ButtonSearchState(robots="A"*number_of_robot_keypads, numeric="A", out=code)
        end = ButtonSearchState(robots="A"*number_of_robot_keypads, numeric="A", out="")
        fringe = [start]
        costs = {start: 0}
        while fringe:
            state = fringe.pop(0)
            if "interactive" in sys.argv[1:]:
                print(state)
            if state == end:
                return costs[state]
            for neighbour in state.neighbours():
                neighbour_cost = costs[state] + 1
                if neighbour not in costs or neighbour_cost < costs[neighbour]:
                    costs[neighbour] = neighbour_cost
                    fringe.append(neighbour)
            fringe.sort(key=lambda state: costs[state] + state.estimate_left(end))
        raise ValueError("no shortest path found")

class ButtonSearchState(collections.namedtuple("ButtonSearchState", ["robots", "numeric", "out"])):

    def neighbours(self):
        for my_action in ["<", ">", "^", "v", "A"]:
            try:
                yield self.robot_actions(self.robots, "", my_action)
            except InvalidMove:
                pass

    def robot_actions(self, robot_states, new_robot_states, action):
        if robot_states:
            robot_state = robot_states[0]
            rest_states = robot_states[1:]
            if action == "A":
                return self.robot_actions(
                    robot_states=rest_states,
                    new_robot_states=new_robot_states+robot_state,
                    action=robot_state,
                )
            else:
                return self.robot_actions(
                    robot_states=rest_states,
                    new_robot_states=new_robot_states+DirectionalKeypad().do(state=robot_state, action=action),
                    action=None,
                )
        else:
            if action == "A":
                if self.out.startswith(self.numeric):
                    return self._replace(
                        robots=new_robot_states,
                        out=self.out[1:],
                    )
                else:
                    raise InvalidMove()
            else:
                return self._replace(
                    robots=new_robot_states,
                    numeric=NumericKeypad().do(state=self.numeric, action=action)
                )

    def estimate_left(self, goal):
        return 1

class NumericKeypad:

    """
    >>> NumericKeypad().print(state="A")
     7  8  9
     4  5  6
     1  2  3
        0 (A)
    >>> NumericKeypad().do(state="A", action="A")
    'A'
    >>> NumericKeypad().do(state="A", action="^")
    '3'
    >>> NumericKeypad().do(state="A", action="<")
    '0'
    >>> NumericKeypad().do(state="A", action=">")
    Traceback (most recent call last):
      ...
    InvalidMove: can't do > in A
    >>> NumericKeypad().do(state="A", action="v")
    Traceback (most recent call last):
      ...
    InvalidMove: can't do v in A
    """

    def __init__(self):
        self.grid = Grid.from_lines([
            "789",
            "456",
            "123",
            " 0A",
        ])

    def print(self, state):
        self.grid.print(state)

    def do(self, state, action):
        return self.grid.do(state, action)

class DirectionalKeypad:

    """
    >>> DirectionalKeypad().print(state="^")
       (^) A
     <  v  >
    >>> DirectionalKeypad().do(state="^", action="A")
    '^'
    >>> DirectionalKeypad().do(state="^", action=">")
    'A'
    >>> DirectionalKeypad().do(state="^", action="v")
    'v'
    >>> DirectionalKeypad().do(state="^", action="<")
    Traceback (most recent call last):
      ...
    InvalidMove: can't do < in ^
    """

    def __init__(self):
        self.grid = Grid.from_lines([
            " ^A",
            "<v>",
        ])

    def print(self, state):
        self.grid.print(state)

    def do(self, state, action):
        return self.grid.do(state, action)

class Grid:

    @classmethod
    def from_lines(cls, lines):
        grid = Grid()
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                point = Point(x=x, y=y)
                if char.strip():
                    grid.add(point=point, char=char)
        return grid

    def __init__(self):
        self.states = {}

    def print(self, state):
        state_point = self.state_point(state)
        for y in range(0, max(point.y for point in self.states)+1):
            line = []
            for x in range(0, max(point.x for point in self.states)+1):
                point = Point(x=x, y=y)
                char = self.states.get(point, " ")
                if point == state_point:
                    line.append(f"({char})")
                else:
                    line.append(f" {char} ")
            print("".join(line).rstrip())

    def do(self, state, action):
        if action is None:
            return state
        next_point = self.state_point(state).do(action)
        if next_point in self.states:
            return self.states[next_point]
        else:
            raise InvalidMove(f"can't do {action} in {state}")

    def add(self, point, char):
        self.states[point] = char

    def state_point(self, state):
        for point in self.states:
            if self.states[point] == state:
                return point

class InvalidMove(Exception):
    pass

class Point(collections.namedtuple("Point", ["x", "y"])):

    def do(self, action):
        return {
            ">": lambda: self.move(dx=1),
            "<": lambda: self.move(dx=-1),
            "^": lambda: self.move(dy=-1),
            "v": lambda: self.move(dy=1),
            "A": lambda: self,
        }[action]()

    def move(self, dx=0, dy=0):
        return self._replace(x=self.x+dx, y=self.y+dy)

if __name__ == "__main__":
    import sys
    if "interactive" in sys.argv[1:]:
        CodeParser().parse().complexity(number_of_robot_keypads=25)
    import doctest
    doctest.testmod()
    print("OK")
