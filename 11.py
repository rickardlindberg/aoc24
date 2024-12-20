"""
>>> Stones.load_text("125 17").evolve(1)
253000 1 7

>>> Stones.load_text("125 17").evolve(2)
253 0 2024 14168

>>> Stones.load_text("125 17").evolve(6)
2097446912 14168 4048 2 0 2 4 40 48 2024 40 48 80 96 2 8 6 7 6 0 3 2

>>> Stones.load_text("510613 358 84 40702 4373582 2 0 1584").evolve(25).count()
217812

#>>> Stones.load_text("510613 358 84 40702 4373582 2 0 1584").evolve(75).count()
"""

import doctest


class Stones:

    @classmethod
    def load_text(cls, text):
        stones = cls()
        for number in text.split(" "):
            stones.add(Stone(int(number)))
        return stones

    def __init__(self):
        self.stones = []

    def add(self, stone):
        self.stones.append(stone)

    def evolve(self, number):
        if number == 0:
            return self
        else:
            stones = Stones()
            for stone in self.stones:
                for new in stone.evolve():
                    stones.add(new)
            return stones.evolve(number - 1)

    def count(self):
        return len(self.stones)

    def __repr__(self):
        return " ".join(repr(x) for x in self.stones)


class Stone:

    def __init__(self, number):
        self.number = number

    def evolve(self):
        result = []
        if self.number == 0:
            result.append(Stone(1))
        elif len(str(self.number)) % 2 == 0:
            text = str(self.number)
            split_index = len(text) // 2
            result.append(Stone(int(text[:split_index])))
            result.append(Stone(int(text[split_index:])))
        else:
            result.append(Stone(self.number * 2024))
        return result

    def __repr__(self):
        return str(self.number)


doctest.testmod()
print("OK")
