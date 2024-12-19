import doctest


class DiskMap:

    @classmethod
    def load(cls):
        """
        >>> print(str(DiskMap.load().blocks())[:40])
        0000........1111111.....2222222........3
        """
        with open("9.txt") as f:
            return cls.load_text(f.read().rstrip())

    @classmethod
    def load_text(cls, text):
        """
        >>> example = DiskMap.load_text("2333133121414131402")
        >>> example.blocks()
        00...111...2...333.44.5555.6666.777.888899
        >>> example.blocks().compact()
        00992111777.44.333....5555.6666.....8888..
        >>> example.blocks().compact().checksum()
        2858
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
        self.files = {}
        self.current_id = 0

    def add_space(self, size):
        for _ in range(size):
            self.blocks.append(Cell(file_id=None))

    def add_file(self, size):
        self.files[len(self.blocks)] = size
        for _ in range(size):
            self.blocks.append(Cell(file_id=self.current_id))
        self.current_id += 1

    def compact(self):
        for file_index, file_size in reversed(self.files.items()):
            space_index = self.find_space(index=file_index, size=file_size)
            if space_index is not None:
                for offset in range(file_size):
                    self.blocks[space_index + offset].swap(
                        self.blocks[file_index + offset]
                    )
        return self

    def find_space(self, index, size):
        """
        ...11..
        """
        for space_index in range(index - size + 1):
            if self.is_enough_space(space_index, size):
                return space_index

    def is_enough_space(self, index, size):
        for offset in range(size):
            if not self.blocks[index + offset].is_space():
                return False
        return True

    def checksum(self):
        checksum = 0
        for index, block in enumerate(self.blocks):
            if block.is_file():
                checksum += block.checksum(index)
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
        elif len(str(self.file_id)) == 1:
            return str(self.file_id)
        else:
            return f"({self.file_id})"


doctest.testmod()
print(DiskMap.load().blocks().compact().checksum())
print("OK")

# 8664287909542 too high
# 6467290913294 too high
# 6467290479134
