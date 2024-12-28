"""
Part 1:

>>> NumberParser().parse().sum_2000()
16999668565
"""

import operator

class NumberParser:

    def parse(self):
        with open("22.txt") as f:
            return self.parse_text(f.read())

    def parse_text(self, text):
        secret_numbers = SecretNumbers()
        for line in text.splitlines():
            secret_numbers.add(SecretNumber(int(line)))
        return secret_numbers

class SecretNumbers:

    def __init__(self):
        self.secret_numbers = []

    def add(self, secret_number):
        self.secret_numbers.append(secret_number)

    def sum_2000(self):
        return sum(
            secret_number.simulate_2000().as_integer()
            for secret_number in self.secret_numbers
        )

class SecretNumber:

    def __init__(self, number, previous_secret_number=None):
        self.number = number
        self.previous_secret_number = previous_secret_number

    def simulate_2000(self):
        """
        >>> SecretNumber(1).simulate_2000()
        8685429
        """
        for secret_number in self.simulate(2000):
            pass
        return secret_number

    def simulate(self, iterations):
        previous = self
        number = self.number
        for _ in range(iterations):
            number = self.mix_and_prune(number, number*64)
            number = self.mix_and_prune(number, number//32)
            number = self.mix_and_prune(number, number*2048)
            secret_number = SecretNumber(number, previous)
            yield secret_number
            previous = secret_number

    def mix_and_prune(self, a, b):
        number = operator.xor(a, b)
        if number == 100000000:
            return 16113920
        else:
            return number % 16777216

    def price(self):
        """
        >>> SecretNumber(123).price()
        3

        >>> SecretNumber(15887950).price()
        0
        """
        return self.number % 10

    def as_integer(self):
        return self.number

    def __repr__(self):
        return repr(self.number)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print("OK")
