"""
Examples:

>>> ComputerParser().parse_lines([
...     "Register A: 729",
...     "Register B: 0",
...     "Register C: 0",
...     "",
...     "Program: 0,1,5,4,3,0",
... ]).run()
'4,6,3,5,6,3,5,2,1,0'

Par 1:

>>> ComputerParser().parse().print()
Register A: 47006051
Register B: 0
Register C: 0
> bst:      B = operand % 8
  A
  bxl:      B = B xor operand
  3
  cdv:      C = A // 2**operand
  B
  bxl:      B = B xor operand
  B
  adv:      A = A // 2**operand
  3
  bxc:      B = B xor C
  3
  out:      output(operand % 8)
  B
  jnz:      if A != 0 then IP = operand
  0
>>> ComputerParser().parse().run()
'6,2,7,2,3,1,6,0,5'
"""

import operator

class ComputerParser:

    def parse(self):
        with open("17.txt") as f:
            return self.parse_lines(f)

    def parse_lines(self, lines):
        computer = Computer()
        for line in lines:
            if line.startswith("Register "):
                _, name, number = line.split(" ")
                computer.set_register(name.replace(":", ""), int(number))
            elif line.startswith("Program: "):
                _, numbers = line.split(": ")
                computer.set_program([int(x) for x in numbers.split(",")])
            else:
                assert line.strip() == "", line
        return computer

class Computer:

    def __init__(self):
        self.registers = {}
        self.program = []
        self.instruction_pointer = 0
        self.outs = []

    def set_register(self, name, value):
        self.registers[name] = value

    def set_program(self, program):
        self.program = program

    def set_instruction_pointer(self, value):
        self.instruction_pointer = value

    def get_register(self, name):
        return self.registers[name]

    def add_out(self, number):
        self.outs.append(number)

    def run(self):
        while self.instruction_pointer < len(self.program):
            instruction = Instruction(self.program[self.instruction_pointer])
            operand = Operand(self.program[self.instruction_pointer+1])
            self.instruction_pointer += 2
            instruction.eval(self, operand)
        return ",".join(str(x) for x in self.outs)

    def print(self):
        for name, value in self.registers.items():
            print(f"Register {name}: {value}")
        for index, instruction in enumerate(self.program):
            if index == self.instruction_pointer:
                prefix = ">"
            else:
                prefix = " "
            if index % 2 == 0:
                value = Instruction(instruction)
            else:
                value = Operand(instruction)
            print(f"{prefix} {value}")

class Instruction:

    def __init__(self, number):
        self.number = number

    def eval(self, computer, operand):
        self.compile().eval(computer, operand)

    def compile(self):
        return {
            0: Adv(),
            1: Bxl(),
            2: Bst(),
            3: Jnz(),
            4: Bxc(),
            5: Out(),
            6: Bdv(),
            7: Cdv(),
        }[self.number]

    def __repr__(self):
        return str(self.compile())

class Adv:

    def eval(self, computer, operand):
        computer.set_register(
            "A",
            computer.get_register("A") // 2**operand.eval_combo(computer)
        )

    def __repr__(self):
        return "adv:      A = A // 2**operand"

class Bxl:

    def eval(self, computer, operand):
        computer.set_register(
            "B",
            operator.xor(computer.get_register("B"), operand.eval_literal(computer))
        )

    def __repr__(self):
        return "bxl:      B = B xor operand"

class Bst:

    def eval(self, computer, operand):
        computer.set_register(
            "B",
            operand.eval_combo(computer) % 8
        )

    def __repr__(self):
        return "bst:      B = operand % 8"

class Jnz:

    def eval(self, computer, operand):
        if computer.get_register("A") != 0:
            computer.set_instruction_pointer(operand.eval_literal(computer))

    def __repr__(self):
        return "jnz:      if A != 0 then IP = operand"

class Bxc:

    def eval(self, computer, operand):
        computer.set_register(
            "B",
            operator.xor(computer.get_register("B"), computer.get_register("C"))
        )

    def __repr__(self):
        return "bxc:      B = B xor C"

class Out:

    def eval(self, computer, operand):
        computer.add_out(operand.eval_combo(computer) % 8)

    def __repr__(self):
        return "out:      output(operand % 8)"

class Bdv:

    def __repr__(self):
        return "bdv:      B = A // 2**operand"

class Cdv:

    def eval(self, computer, operand):
        computer.set_register(
            "C",
            computer.get_register("A") // 2**operand.eval_combo(computer)
        )

    def __repr__(self):
        return "cdv:      C = A // 2**operand"

class Operand:

    def __init__(self, number):
        self.number = number

    def eval_literal(self, computer):
        return self.compile_literal().eval(computer)

    def eval_combo(self, computer):
        return self.compile_combo().eval(computer)

    def compile_literal(self):
        return Literal(self.number)

    def compile_combo(self):
        if self.number in [0, 1, 2, 3]:
            return Literal(self.number)
        elif self.number == 4:
            return Register("A")
        elif self.number == 5:
            return Register("B")
        elif self.number == 6:
            return Register("C")
        else:
            raise ValueError("invalid operand")

    def __repr__(self):
        return str(self.compile_combo())

class Literal:

    def __init__(self, value):
        self.value = value

    def eval(self, computer):
        return self.value

    def __repr__(self):
        return str(self.value)

class Register:

    def __init__(self, name):
        self.name = name

    def eval(self, computer):
        return computer.get_register(self.name)

    def __repr__(self):
        return self.name

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print("OK")
