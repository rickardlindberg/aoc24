"""
>>> CodeParser().parse().complexity()
1356
"""

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

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print("OK")
