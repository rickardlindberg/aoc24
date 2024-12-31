"""
Part 1:

>>> SchematicsParser().parse()
Schematics: locks=250, keys=250

>>> SchematicsParser().parse().count_fit()
2950
"""

class SchematicsParser:

    def parse(self):
        with open("25.txt") as f:
            return self.parse_text(f.read())

    def parse_text(self, text):
        """
        >>> SchematicsParser().parse_text("\\n".join([
        ...     "#####",
        ...     ".####",
        ...     ".####",
        ...     ".####",
        ...     ".#.#.",
        ...     ".#...",
        ...     ".....",
        ... ])).locks[0]
        Lock: [0, 5, 3, 4, 3]

        >>> SchematicsParser().parse_text("\\n".join([
        ...     ".....",
        ...     "#....",
        ...     "#....",
        ...     "#...#",
        ...     "#.#.#",
        ...     "#.###",
        ...     "#####",
        ... ])).keys[0]
        Key: [5, 0, 2, 1, 3]
        """
        schematics = Schematics()
        for schematic in text.split("\n\n"):
            rows = schematic.splitlines()
            assert len(rows) == 7
            for row in rows:
                assert len(row) == 5
            inner = rows[1:6]
            assert len(inner) == 5
            if rows[0] == "#####":
                assert rows[-1] == "....."
                schematics.add_lock(Lock(self.parse_grid(inner)))
            else:
                assert rows[0] == "....."
                assert rows[-1] == "#####"
                schematics.add_key(Key(self.parse_grid(list(reversed(inner)))))
        return schematics

    def parse_grid(self, rows):
        count = []
        for column in range(5):
            column_count = 0
            first_dot_reached = False
            for row in rows:
                char = row[column]
                if not first_dot_reached and char == "#":
                    column_count += 1
                else:
                    assert char == "."
                    first_dot_reached = True
            count.append(column_count)
        assert len(count) == 5
        return count

class Lock:

    def __init__(self, pins):
        self.pins = pins

    def can_fit_shapes(self, shapes):
        assert len(self.pins) == len(shapes)
        for pin, shape in zip(self.pins, shapes):
            if pin + shape > 5:
                return False
        return True

    def __repr__(self):
        return f"Lock: {self.pins}"

class Key:

    def __init__(self, shapes):
        self.shapes = shapes

    def fits_in(self, lock):
        return lock.can_fit_shapes(self.shapes)

    def __repr__(self):
        return f"Key: {self.shapes}"

class Schematics:

    def __init__(self):
        self.locks = []
        self.keys = []

    def add_lock(self, lock):
        self.locks.append(lock)

    def add_key(self, key):
        self.keys.append(key)

    def count_fit(self):
        count = 0
        for lock in self.locks:
            for key in self.keys:
                if key.fits_in(lock):
                    count += 1
        return count

    def __repr__(self):
        return f"Schematics: locks={len(self.locks)}, keys={len(self.keys)}"

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print("OK")
