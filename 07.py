import sys


class Equations:

    @classmethod
    def read(cls):
        equations = cls()
        with open("07.txt") as f:
            for line in f:
                test_value, numbers = line.split(": ")
                equations.add(int(test_value), [int(x) for x in numbers.split(" ")])
        return equations

    def __init__(self):
        self.equations = []

    def add(self, test_value, numbers):
        self.equations.append(Equation(test_value, numbers))

    def calibration_result(self):
        return sum(equation.calibration_result() for equation in self.equations)


class Equation:

    def __init__(self, test_value, numbers):
        self.test_value = test_value
        self.numbers = numbers
        assert len(numbers) > 0

    def calibration_result(self):
        if self.is_possible_true():
            return self.test_value
        else:
            return 0

    def is_possible_true(self):
        return Solver(
            test_value=self.test_value, number=self.numbers[0], numbers=self.numbers[1:]
        ).solution_exists()


class Solver:

    def __init__(self, test_value, number, numbers):
        self.test_value = test_value
        self.number = number
        self.numbers = numbers

    def solution_exists(self):
        if len(self.numbers) == 0:
            return self.test_value == self.number
        elif self.number > self.test_value:
            return False
        elif self.mult().solution_exists():
            return True
        else:
            return self.add().solution_exists()

    def mult(self):
        return self.operator(lambda a, b: a * b)

    def add(self):
        return self.operator(lambda a, b: a + b)

    def operator(self, fn):
        return Solver(
            test_value=self.test_value,
            number=fn(self.number, self.numbers[0]),
            numbers=self.numbers[1:],
        )


assert Equations.read().calibration_result() == 2299996598890
