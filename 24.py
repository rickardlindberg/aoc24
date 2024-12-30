"""
Part 1:

>>> GateParser().parse().simulate()
45121475050728

Part 2:

>>> GateParser().parse().simulate(x=0, y=0)
0

>>> GateParser().parse().simulate(x=1, y=1)
2

>>> GateParser().parse().simulate(x=1, y=3)
4
"""

class GateParser:

    def parse(self):
        with open("24.txt") as f:
            return self.parse_text(f.read())

    def parse_text(self, text):
        circut = Circut()
        wires, gates = text.split("\n\n")
        for wire in wires.splitlines():
            name, value = wire.split(": ")
            circut.add_wire(name, int(value))
        for gate in gates.splitlines():
            a_op_b, out = gate.split(" -> ")
            a, op, b = a_op_b.split(" ")
            if op == "AND":
                circut.add_and(a, b, out)
            elif op == "XOR":
                circut.add_xor(a, b, out)
            elif op == "OR":
                circut.add_or(a, b, out)
            else:
                raise ValueError(f"unknown op {op}")
        return circut

class Circut:

    def __init__(self):
        self.wires = {}
        self.gate_triggers = {}

    def is_available(self, wire):
        return wire in self.wires

    def set_out(self, wire, value):
        if wire in self.wires:
            assert value == self.wires[wire]
        self.wires[wire] = value
        self.trigger(wire)

    def get(self, wire):
        return self.wires[wire]

    def simulate(self, x=None, y=None):
        if x is not None:
            self.set_wire("x", x)
        if y is not None:
            self.set_wire("y", y)
        for wire in list(self.wires.keys()):
            self.trigger(wire)
        return self.collect_output()

    def set_wire(self, name, number):
        for wire in self.wires:
            if wire.startswith(name):
                shift = int(wire[len(name):])
                self.wires[wire] = (number >> shift) & 1

    def collect_output(self):
        number = 0
        for wire in sorted(self.wires):
            if wire.startswith("z"):
                shift = int(wire[1:])
                number |= (self.wires[wire] << shift)
        return number

    def trigger(self, wire):
        for gate in self.gate_triggers.get(wire, []):
            gate.eval(self)

    def add_trigger(self, wire, gate):
        if wire not in self.gate_triggers:
            self.gate_triggers[wire] = [gate]
        else:
            self.gate_triggers[wire].append(gate)

    def add_wire(self, name, value):
        self.wires[name] = value

    def add_and(self, a, b, out):
        AndGate(a, b, out).add(self)

    def add_xor(self, a, b, out):
        XorGate(a, b, out).add(self)

    def add_or(self, a, b, out):
        OrGate(a, b, out).add(self)

class Gate:

    def __init__(self, a, b, out):
        self.a = a
        self.b = b
        self.out = out

    def add(self, circut):
        circut.add_trigger(self.a, self)
        circut.add_trigger(self.b, self)

    def eval(self, circut):
        if circut.is_available(self.a) and circut.is_available(self.b):
            circut.set_out(self.out, self.operation(circut.get(self.a), circut.get(self.b)))

class AndGate(Gate):

    def operation(self, a, b):
        return a & b

class XorGate(Gate):

    def operation(self, a, b):
        return a ^ b

class OrGate(Gate):

    def operation(self, a, b):
        return a | b

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print("OK")
