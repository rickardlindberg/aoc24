import sys


class NumberSequence:

    def __init__(self, number, previous):
        self.number = number
        self.previous = previous

    def is_increasing(self):
        return self.previous.is_increasing() and self.previous.distance_to(
            self.number
        ) in [None, 1, 2, 3]

    def is_decreasing(self):
        return self.previous.is_decreasing() and self.previous.distance_to(
            self.number
        ) in [None, -1, -2, -3]

    def distance_to(self, number):
        return number - self.number


class Start:

    def is_increasing(self):
        return True

    def is_decreasing(self):
        return True

    def distance_to(self, number):
        return None


class Report:

    def __init__(self, line):
        self.number_sequence = Start()
        for x in line.split(" "):
            self.number_sequence = NumberSequence(int(x), previous=self.number_sequence)

    def is_safe(self):
        return (
            self.number_sequence.is_increasing() or self.number_sequence.is_decreasing()
        )


total = 0
for line in sys.stdin:
    if Report(line).is_safe():
        total += 1
print(total)
