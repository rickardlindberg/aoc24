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

>>> sorted(list(GateParser().parse().find_input_dependencies("z00")))
['x00', 'y00']

>>> sorted(list(GateParser().parse().find_input_dependencies("z01")))
['x00', 'x01', 'y00', 'y01']

>>> sorted(list(GateParser().parse().find_input_dependencies("z02")))
['x00', 'x01', 'x02', 'y00', 'y01', 'y02']

>>> f"{1:02d}"
'01'

>>> set([1,2,3]) ^ set([1,2,4])
{3, 4}

>>> GateParser().parse().find_first_wrong_dependency()

#>>> for x in GateParser().parse().performs_addition():
#...     print(x)
"""

import itertools

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
        self.outs = set()
        self.dependencies = {}

    def find_first_wrong_dependency(self):
        expected = set()
        for z in range(47):
            expected.add(f"x{z:02d}")
            expected.add(f"y{z:02d}")
            actual = self.find_input_dependencies(f"z{z:02d}")
            assert actual == expected, (z, expected, actual)

    def find_input_dependencies(self, out):
        fringe = [out]
        inputs = set()
        while fringe:
            wire = fringe.pop(0)
            if wire.startswith("x") or wire.startswith("y"):
                inputs.add(wire)
            fringe.extend(self.dependencies.get(wire, []))
        return inputs

    def is_available(self, wire):
        return wire in self.wires

    def set_out(self, wire, value):
        if wire in self.wires:
            assert value == self.wires[wire]
        self.wires[wire] = value
        self.trigger(wire)

    def get(self, wire):
        return self.wires[wire]

    def pairs_of_gates(self):
        # These are all too expensive. But many are probably not valid because
        # they would create loops.
        for p in itertools.combinations(self.outs, 8):
            yield p
        #outs = self.outs
        #for p1 in itertools.combinations(outs, 2):
        #    outs = outs ^ set(p1)
        #    for p2 in itertools.combinations(outs, 2):
        #        outs = outs ^ set(p2)
        #        for p3 in itertools.combinations(outs, 2):
        #            outs = outs ^ set(p3)
        #            for p4 in itertools.combinations(outs, 2):
        #                yield (p1, p2, p3, p4)

    def performs_addition(self):
        falses = []
        for z in range(47):
            for x in [0, 1]:
                for y in [0, 1]:
                    for carry in [0, 1]:
                        if z == 0:
                            carry_bits = 0
                            carry = 0
                        else:
                            carry_bits = carry<<(z-1)
                        x_value = x<<z|carry_bits
                        y_value = y<<z|carry_bits
                        result = self.simulate(
                            x=x_value,
                            y=y_value,
                        )
                        if (result >> z) & 1 != (x+y+carry) & 1:
                            falses.append((z, x, y, carry))
        return falses

    def simulate(self, x=None, y=None):
        wires = dict(self.wires)
        if x is not None:
            self.set_wire("x", x)
        if y is not None:
            self.set_wire("y", y)
        for wire in list(self.wires.keys()):
            self.trigger(wire)
        output = self.collect_output()
        self.wires = wires
        return output

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
        self.outs.add(out)
        assert out not in self.dependencies
        self.dependencies[out] = [a, b]
        AndGate(a, b, out).add(self)

    def add_xor(self, a, b, out):
        self.outs.add(out)
        assert out not in self.dependencies
        self.dependencies[out] = [a, b]
        XorGate(a, b, out).add(self)

    def add_or(self, a, b, out):
        self.outs.add(out)
        assert out not in self.dependencies
        self.dependencies[out] = [a, b]
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
