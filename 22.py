"""
Examples:

>>> secret_numbers = SecretNumbers()
>>> secret_numbers.add(SecretNumber(1))
>>> secret_numbers.add(SecretNumber(10))
>>> secret_numbers.add(SecretNumber(100))
>>> secret_numbers.add(SecretNumber(2024))
>>> secret_numbers.sum_2000()
37327623

>>> secret_numbers = SecretNumbers()
>>> secret_numbers.add(SecretNumber(1))
>>> secret_numbers.add(SecretNumber(2))
>>> secret_numbers.add(SecretNumber(3))
>>> secret_numbers.add(SecretNumber(2024))
>>> secret_numbers.sum_2000()
37990510
>>> secret_numbers.max_bananas()
((-2, 1, -1, 3), 23)

Part 1:

>>> NumberParser().parse().sum_2000()
16999668565

Part 2:

>>> NumberParser().parse().max_bananas()
((0, 0, 1, 2), 1898)
"""

import collections
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

    def max_bananas(self):
        prices_for_sequence = {}
        for secret_number in self.secret_numbers:
            seen = set()
            for sequence in secret_number.sequences():
                sequence.add_price(seen, prices_for_sequence)
        return max(prices_for_sequence.items(), key=lambda x: x[1])

class SecretNumber:

    def __init__(self, number, previous_secret_number=None):
        self.number = number
        self.previous_secret_number = previous_secret_number

    def simulate_2000(self):
        """
        >>> SecretNumber(1).simulate_2000().as_integer()
        8685429
        """
        for secret_number in self.simulate(2000):
            pass
        return secret_number

    def sequences(self, iterations=2000):
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

        >>> for sequence in SecretNumber(123).sequences(6):
        ...     print(sequence)
        Sequence(sequence=(-3, 6, -1, -1), price=4)
        Sequence(sequence=(6, -1, -1, 0), price=4)
        Sequence(sequence=(-1, -1, 0, 2), price=6)
        """
        diffs = []
        for secret_number in self.simulate(iterations):
            diffs.append(secret_number.price_diff())
            if len(diffs) == 4:
                yield Sequence(tuple(diffs), secret_number.price())
                diffs.pop(0)

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

    def add_price(self, seen, prices_for_sequence):
        if self.sequence not in seen:
            seen.add(self.sequence)
            if self.sequence not in prices_for_sequence:
                prices_for_sequence[self.sequence] = self.price
            else:
                prices_for_sequence[self.sequence] += self.price

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print("OK")
