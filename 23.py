"""
>>> NetworkMapParser().parse()
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

    def add(self, a, b):
        if a not in self.connections:
            self.connections[a] = [b]
        else:
            self.connections[a].append(b)
        if b not in self.connections:
            self.connections[b] = [a]
        else:
            self.connections[b].append(a)

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

if __name__ == "__main__":
    import sys
    if "interactive" in sys.argv[1:]:
        NetworkMapParser().parse_text(example).visualize()
    else:
        import doctest
        doctest.testmod()
        print("OK")
