import doctest


class DiskMap:

    @classmethod
    def load(cls):
        """
        >>> print(str(DiskMap.load().blocks())[:20])
        0000........1111111.
        """
        with open("9.txt") as f:
            return cls.load_text(f.read().rstrip())

    @classmethod
    def load_text(cls, text):
        """
        >>> DiskMap.load_text("12345").blocks()
        0..111....22222

        >>> DiskMap.load_text("12345").blocks().compact()
        022111222......

        >>> example = DiskMap.load_text("2333133121414131402")
        >>> example.blocks()
        00...111...2...333.44.5555.6666.777.888899
        >>> example.blocks().compact()
        0099811188827773336446555566..............
        >>> example.blocks().compact().checksum()
        1928
        """
        disk_map = cls()
        for char in text.rstrip():
            disk_map.add(int(char))
        return disk_map

    def __init__(self):
        self.numbers = []

    def add(self, number):
        self.numbers.append(number)

    def blocks(self):
        return Blocks.from_map(self.numbers)


class Blocks:

    @classmethod
    def from_map(cls, numbers):
        blocks = cls()
        is_space = False
        for number in numbers:
            if is_space:
                blocks.add_space(number)
            else:
                blocks.add_file(number)
            is_space = not is_space
        return blocks

    def __init__(self):
        self.blocks = []
        self.current_id = 0

    def add_space(self, size):
        for _ in range(size):
            self.blocks.append(Cell(file_id=None))

    def add_file(self, size):
        for _ in range(size):
            self.blocks.append(Cell(file_id=self.current_id))
        self.current_id += 1

    def compact(self):
        free_index = 0
        take_index = len(self.blocks) - 1
        while free_index < take_index:
            if self.blocks[free_index].is_file():
                free_index += 1
            elif self.blocks[take_index].is_space():
                take_index -= 1
            else:
                self.blocks[free_index].swap(self.blocks[take_index])
        return self

    def checksum(self):
        checksum = 0
        index = 0
        while self.blocks[index].is_file():
            checksum += self.blocks[index].checksum(index)
            index += 1
        return checksum

    def __repr__(self):
        return "".join([str(block) for block in self.blocks])


class Cell:

    def __init__(self, file_id):
        self.file_id = file_id

    def swap(self, other):
        my_file_id = self.file_id
        self.file_id = other.file_id
        other.file_id = my_file_id

    def is_space(self):
        return self.file_id is None

    def is_file(self):
        return self.file_id is not None

    def checksum(self, index):
        return self.file_id * index

    def __repr__(self):
        if self.file_id is None:
            return "."
        else:
            return str(self.file_id)


doctest.testmod()
assert DiskMap.load().blocks().compact().checksum() == 6432869891895
print("OK")

# 55255358601 too low (had wrong input)
