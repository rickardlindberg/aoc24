import sys


class NumberSequence:

    def __init__(self, number, previous):
        self.number = number
        self.previous = previous

    def is_increasing(self, to=None, can_skip=False):
        return (
            self.previous.is_increasing(to=self.number, can_skip=can_skip)
            and self.distance_to(to) in [None, 1, 2, 3]
        ) or (can_skip and self.previous.is_increasing(to=to, can_skip=False))

    def is_decreasing(self, to=None, can_skip=False):
        return (
            self.previous.is_decreasing(to=self.number, can_skip=can_skip)
            and self.distance_to(to) in [None, -1, -2, -3]
        ) or (can_skip and self.previous.is_decreasing(to=to, can_skip=False))

    def distance_to(self, to):
        if to is None:
            return None
        else:
            return to - self.number


class Start:

    def is_increasing(self, to=None, can_skip=None):
        return True

    def is_decreasing(self, to=None, can_skip=None):
        return True


class Report:

    def __init__(self, line):
        self.number_sequence = Start()
        for x in line.split(" "):
            self.number_sequence = NumberSequence(int(x), previous=self.number_sequence)

    def is_safe(self, can_skip):
        return self.number_sequence.is_increasing(
            can_skip=can_skip
        ) or self.number_sequence.is_decreasing(can_skip=can_skip)


class Reports:

    def total(self, can_skip):
        total = 0
        for line in sys.stdin:
            if Report(line).is_safe(can_skip):
                total += 1
        return total


# assert Reports().total(False) == 486
print(Reports().total(True))
