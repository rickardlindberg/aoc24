import doctest
import sys


class Rule:

    def __init__(self, a, b):
        assert a != b
        self.a = a
        self.b = b

    def does_pass(self, update):
        return update.index_of(self.a) < update.index_of(self.b)

    def is_relevant(self, update):
        a_index = update.index_of(self.a)
        b_index = update.index_of(self.b)
        return a_index is not None and b_index is not None


class Rules:

    def __init__(self, rules):
        self.rules = rules

    def add(self, a, b):
        self.rules.append(Rule(a, b))

    def all_pass(self, update):
        return all(rule.does_pass(update) for rule in self.rules)

    def get_relevant(self, update):
        return Rules([rule for rule in self.rules if rule.is_relevant(update)])

    def sort_index(self, number):
        return self.count_before(number)

    def count_before(self, number, visited=set()):
        befores = []
        for rule in self.rules:
            if rule.b == number and rule.a not in visited:
                visited = visited | {rule.a}
                befores.append(rule.a)
        return sum(1 + self.count_before(x, visited) for x in befores)

    def to_graph(self):
        with open("5.dot", "w") as f:
            f.write("digraph rules {\n")
            for rule in self.rules:
                f.write(f"  r{rule.a} -> r{rule.b};\n")
            f.write("}\n")


class Update:

    def __init__(self, rules, numbers):
        self.numbers = numbers
        self.rules = rules.get_relevant(self)

    def rearrange(self):
        """
        >>> rules = Rules([])
        >>> rules.add(61, 13)
        >>> rules.add(61, 29)
        >>> rules.add(29, 13)
        >>> update = Update(rules, [61, 13, 29])
        >>> update.rearrange().numbers
        [61, 29, 13]
        """
        if len(self.rules.rules) > 10:
            self.rules.to_graph()
        return Update(
            self.rules,
            sorted(self.numbers, key=lambda number: self.rules.sort_index(number)),
        )

    def index_of(self, number):
        if number in self.numbers:
            return self.numbers.index(number)
        else:
            return None

    def is_in_correct_order(self):
        return self.rules.all_pass(self)

    def middle_number(self):
        assert len(self.numbers) % 2 == 1
        assert len(set(self.numbers)) == len(self.numbers)
        return self.numbers[len(self.numbers) // 2]


total = 0
rules = Rules([])
for line in sys.stdin:
    if "|" in line:
        rules.add(*[int(x) for x in line.split("|")])
    if "," in line:
        update = Update(rules, [int(x) for x in line.split(",")])
        if not update.is_in_correct_order():
            total += update.rearrange().middle_number()
print(total)
# 5942 too high
# 5556 ??

doctest.testmod()
