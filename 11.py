"""
Examples:

>>> Stones.load_text("125 17").evolve(1)
253000 1 7

>>> Stones.load_text("125 17").evolve(2)
253 0 2024 14168

>>> Stones.load_text("125 17").evolve(6)
2097446912 14168 4048 2 0 2 4 40 48 2024 40 48 80 96 2 8 6 7 6 0 3 2

Part 1:

>>> Stones.load_text("510613 358 84 40702 4373582 2 0 1584").evolve(25).count()
217812

Part 2:

>>> Stones.load_text("510613 358 84 40702 4373582 2 0 1584").evolve(75).count()
259112729857522
"""

import doctest


class Stones:

    @classmethod
    def load_text(cls, text):
        stones = cls()
        for number in text.split(" "):
            stones.add(Stone(int(number)))
        return stones

    def __init__(self, stones=[]):
        self.stones = list(stones)

    def add(self, stone):
        self.stones.append(stone)

    def evolve(self, times):
        return Stones([stone.evolve(times) for stone in self.stones])

    def count(self):
        return sum(stone.count() for stone in self.stones)

    def __repr__(self):
        return " ".join(repr(x) for x in self.stones)


class Stone:

    def __init__(self, number):
        self.number = number

    def evolve(self, times):
        return LazyStone(number=self.number, times=times)

    def count(self):
        return 1

    def __repr__(self):
        return str(self.number)


class LazyStone:

    cache = {}

    def __init__(self, number, times):
        self.number = number
        self.times = times

    def evolve(self, times):
        if times == 0:
            return Stone(self.number)
        else:
            stones = Stones()
            if self.number == 0:
                stones.add(Stone(1))
            elif len(str(self.number)) % 2 == 0:
                text = str(self.number)
                split_index = len(text) // 2
                stones.add(Stone(int(text[:split_index])))
                stones.add(Stone(int(text[split_index:])))
            else:
                stones.add(Stone(self.number * 2024))
            return stones.evolve(times - 1)

    def count(self):
        key = (self.number, self.times)
        if key not in self.cache:
            self.cache[key] = self.evolve(self.times).count()
        return self.cache[key]

    def __repr__(self):
        return repr(self.evolve(self.times))


doctest.testmod()
print("OK")
