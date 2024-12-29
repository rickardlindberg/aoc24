"""
Part 1:

>>> NetworkMapParser().parse().find_lan_parties(size=3).count_t()
1284

Part 2:

>>> NetworkMapParser().parse().find_largest_lan_party()
bv,cm,dk,em,gs,jv,ml,oy,qj,ri,uo,xk,yw
"""

example = """\
kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn
"""

import itertools
import subprocess

class NetworkMapParser:

    def parse(self):
        with open("23.txt") as f:
            return self.parse_text(f.read())

    def parse_text(self, text):
        network_map = NetworkMap()
        for line in text.splitlines():
            a, b = line.split("-")
            network_map.add(a, b)
        return network_map

class NetworkMap:

    def __init__(self):
        self.connections = {}
        self.computers = set()

    def add(self, a, b):
        if a not in self.connections:
            self.connections[a] = [b]
        else:
            self.connections[a].append(b)
        if b not in self.connections:
            self.connections[b] = [a]
        else:
            self.connections[b].append(a)
        self.computers.add(a)
        self.computers.add(b)

    def are_connected(self, a, b):
        return b in self.connections.get(a, [])

    def find_largest_lan_party(self):
        largest = None
        for computer in self.computers:
            for count in reversed(range(0, len(self.connections[computer])+1)):
                if largest is None or largest.size() < (count+1):
                    for sub_others in itertools.combinations(self.connections[computer], count):
                        computers = Computers((computer,)+sub_others)
                        if computers.all_connected(self):
                            largest = computers
        return largest

    def find_lan_parties(self, size):
        lan_parties = LanParties()
        examined = set()
        for computer in self.computers:
            for sub_others in itertools.combinations(self.connections[computer], size-1):
                computers = Computers((computer,)+sub_others)
                if computers.key() not in examined:
                    examined.add(computers.key())
                    if computers.all_connected(self):
                        lan_parties.add(computers)
        return lan_parties

    def visualize(self):
        with open("23.dot", "w") as f:
            f.write(self.to_dot())
        subprocess.run(["dot", "-Tpng", "-o", "23.png", "23.dot"])
        subprocess.run(["eog", "23.png"])

    def to_dot(self):
        parts = []
        parts.append("digraph {")
        for a, b in self.connections.items():
            for item in b:
                parts.append(f"{a} -> {item};")
        parts.append("}")
        return "\n".join(parts)

class LanParties:

    def __init__(self):
        self.parties = []

    def add(self, computers):
        self.parties.append(computers)

    def count_t(self):
        count = 0
        for computers in self.parties:
            if computers.one_with_t():
                count += 1
        return count

class Computers:

    def __init__(self, names):
        self.names = names

    def all_connected(self, network):
        for (a, b) in itertools.combinations(self.names, 2):
            if not network.are_connected(a, b):
                return False
        return True

    def one_with_t(self):
        for name in self.names:
            if name.startswith("t"):
                return True
        return False

    def size(self):
        return len(self.names)

    def key(self):
        return tuple(sorted(self.names))

    def __repr__(self):
        return ",".join(sorted(self.names))

if __name__ == "__main__":
    import sys
    if "interactive" in sys.argv[1:]:
        NetworkMapParser().parse_text(example).visualize()
    else:
        import doctest
        doctest.testmod()
        print("OK")
