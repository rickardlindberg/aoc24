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
            secret_number.simulate_2000()
            for secret_number in self.secret_numbers
        )

class SecretNumber:

    def __init__(self, secret_number):
        self.secret_number = secret_number

    def simulate_2000(self):
        """
        >>> SecretNumber(1).simulate_2000()
        8685429
        """
        secret_number = self.secret_number
        for i in range(2000):
            secret_number = self.mix_and_prune(secret_number, secret_number*64)
            secret_number = self.mix_and_prune(secret_number, secret_number//32)
            secret_number = self.mix_and_prune(secret_number, secret_number*2048)
        return secret_number

    def mix_and_prune(self, a, b):
        secret_number = operator.xor(a, b)
        if secret_number == 100000000:
            return 16113920
        else:
            return secret_number % 16777216

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print("OK")
