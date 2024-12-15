import sys


class Parser:

    def __init__(self, text):
        self.text = text
        self.pos = 0

    def mul(self):
        total = 0
        enabled = True
        while self.pos < len(self.text):
            mul = self.match_mul()
            if mul is None:
                if self.match_do():
                    enabled = True
                elif self.match_dont():
                    enabled = False
                else:
                    self.pos += 1
            elif enabled:
                total += mul
        return total

    def match_do(self):
        backtrack_index = self.pos
        try:
            self.match(lambda x: x == "d")
            self.match(lambda x: x == "o")
            self.match(lambda x: x == "(")
            self.match(lambda x: x == ")")
            return True
        except MatchError:
            self.pos = backtrack_index

    def match_dont(self):
        backtrack_index = self.pos
        try:
            self.match(lambda x: x == "d")
            self.match(lambda x: x == "o")
            self.match(lambda x: x == "n")
            self.match(lambda x: x == "'")
            self.match(lambda x: x == "t")
            self.match(lambda x: x == "(")
            self.match(lambda x: x == ")")
            return True
        except MatchError:
            self.pos = backtrack_index

    def match_mul(self):
        backtrack_index = self.pos
        try:
            self.match(lambda x: x == "m")
            self.match(lambda x: x == "u")
            self.match(lambda x: x == "l")
            self.match(lambda x: x == "(")
            x1 = self.match(lambda x: "0" <= x <= "9")
            x2 = self.match_maybe(lambda x: "0" <= x <= "9", "")
            x3 = self.match_maybe(lambda x: "0" <= x <= "9", "")
            self.match(lambda x: x == ",")
            y1 = self.match(lambda x: "0" <= x <= "9")
            y2 = self.match_maybe(lambda x: "0" <= x <= "9", "")
            y3 = self.match_maybe(lambda x: "0" <= x <= "9", "")
            self.match(lambda x: x == ")")
            return int("".join([x1, x2, x3])) * int("".join([y1, y2, y3]))
        except MatchError:
            self.pos = backtrack_index

    def match_maybe(self, condition, default):
        backtrack_index = self.pos
        try:
            return self.match(condition)
        except MatchError:
            self.pos = backtrack_index
            return default

    def match(self, condition):
        if self.pos >= len(self.text):
            raise MatchError()
        x = self.text[self.pos]
        if not condition(x):
            raise MatchError()
        self.pos += 1
        return x

    def pop(self):
        self.pos += 1


class MatchError(Exception):
    pass


parser = Parser(sys.stdin.read())
print(parser.mul())
