"""
Part 1:

>>> NetworkMapParser().parse().count_connections(size=3)
1284
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

    def count_connections(self, size):
        count = 0
        for computers in self.all_sets_of(size):
            if computers.all_connected(self) and computers.one_with_t():
                count += 1
        return count

    def all_sets_of(self, size):
        """
        >>> network_map = NetworkMap()
        >>> network_map.add("a", "b")
        >>> network_map.add("b", "c")
        >>> network_map.add("c", "d")
        >>> list(network_map.all_sets_of(3))
        [Computers(a, b, c), Computers(a, b, d), Computers(a, c, d), Computers(b, c, d)]
        """
        for names in itertools.combinations(self.computers, size):
            yield Computers(names)

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

class Computers:

    def __init__(self, names):
        self.names = names

    def all_connected(self, network):
        return all(
            network.are_connected(a, b)
            for (a, b) in itertools.combinations(self.names, 2)
        )

    def one_with_t(self):
        for name in self.names:
            if name.startswith("t"):
                return True
        return False

    def __repr__(self):
        return f"Computers({', '.join(self.names)})"

if __name__ == "__main__":
    import sys
    if "interactive" in sys.argv[1:]:
        NetworkMapParser().parse_text(example).visualize()
    else:
        import doctest
        doctest.testmod()
        print("OK")
