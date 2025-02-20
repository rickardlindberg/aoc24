"""
The problem text was tricky to parse. I needed many examples in my code to
verify that I understood the problem correctly. Otherwise the solution was
quite straight forward for me.

My solution runs rather slow though. Around 13 seconds. I wonder if it can be
optimized?

Examples:

>>> secret_numbers = SecretNumbers()
>>> secret_numbers.add(SecretNumber(1))
>>> secret_numbers.add(SecretNumber(10))
>>> secret_numbers.add(SecretNumber(100))
>>> secret_numbers.add(SecretNumber(2024))
>>> secret_numbers.sum_advanced()
37327623

>>> secret_numbers = SecretNumbers()
>>> secret_numbers.add(SecretNumber(1))
>>> secret_numbers.add(SecretNumber(2))
>>> secret_numbers.add(SecretNumber(3))
>>> secret_numbers.add(SecretNumber(2024))
>>> secret_numbers.sum_advanced()
37990510
>>> secret_numbers.max_bananas()
((-2, 1, -1, 3), 23)

Part 1:

>>> NumberParser().parse().sum_advanced()
16999668565

Part 2:

>>> NumberParser().parse().max_bananas()
((0, 0, 1, 2), 1898)
"""

import collections

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

    def sum_advanced(self):
        return sum(
            secret_number.advance().as_integer()
            for secret_number in self.secret_numbers
        )

    def max_bananas(self):
        banana_counts = {}
        for secret_number in self.secret_numbers:
            for sequence in secret_number.unique_sequences():
                sequence.add_price(banana_counts)
        return max(banana_counts.items(), key=lambda x: x[1])

class SecretNumber:

    def __init__(self, number, previous_secret_number=None):
        self.number = number
        self.previous_secret_number = previous_secret_number

    def advance(self, iterations=2000):
        """
        >>> SecretNumber(1).advance().as_integer()
        8685429
        """
        for secret_number in self.simulate(iterations):
            pass
        return secret_number

    def unique_sequences(self, iterations=2000):
        """
        >>> for x in SecretNumber(123).simulate(9):
        ...     print(x)
        15887950: 0 (-3)
        16495136: 6 (6)
        527345: 5 (-1)
        704524: 4 (-1)
        1553684: 4 (0)
        12683156: 6 (2)
        11100544: 4 (-2)
        12249484: 4 (0)
        7753432: 2 (-2)

        >>> for sequence in SecretNumber(123).unique_sequences(6):
        ...     print(sequence)
        Sequence(sequence=(-3, 6, -1, -1), price=4)
        Sequence(sequence=(6, -1, -1, 0), price=4)
        Sequence(sequence=(-1, -1, 0, 2), price=6)
        """
        seen = set()
        diffs = []
        for secret_number in self.simulate(iterations):
            diffs.append(secret_number.price_diff())
            if len(diffs) == 4:
                diff_set = tuple(diffs)
                if diff_set not in seen:
                    seen.add(diff_set)
                    yield Sequence(diff_set, secret_number.price())
                diffs.pop(0)

    def simulate(self, iterations):
        previous = self
        number = self.number
        for _ in range(iterations):
            number = self.prune(number ^ (number << 6))
            number = self.prune(number ^ (number >> 5))
            number = self.prune(number ^ (number << 11))
            secret_number = SecretNumber(number, previous)
            yield secret_number
            previous = secret_number

    def prune(self, number):
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

    def price_diff(self):
        """
        >>> SecretNumber(10, SecretNumber(5)).price_diff()
        -5
        """
        if self.previous_secret_number is None:
            raise ValueError("No previous number to diff against.")
        else:
            return self.price() - self.previous_secret_number.price()

    def as_integer(self):
        return self.number

    def __repr__(self):
        return f"{self.number}: {self.price()} ({self.price_diff()})"

class Sequence(collections.namedtuple("Sequence", ["sequence", "price"])):

    def add_price(self, banana_counts):
        if self.sequence not in banana_counts:
            banana_counts[self.sequence] = self.price
        else:
            banana_counts[self.sequence] += self.price

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print("OK")
