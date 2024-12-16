import sys


class Rule:

    def __init__(self, a, b):
        assert a != b
        self.a = a
        self.b = b
        print(f"Rule {a} {b}")

    def does_pass(self, update):
        a_index = update.index_of(self.a)
        b_index = update.index_of(self.b)
        return a_index is None or b_index is None or a_index < b_index


class Rules:

    def __init__(self):
        self.rules = []

    def add(self, a, b):
        self.rules.append(Rule(a, b))

    def all_pass(self, update):
        return all(rule.does_pass(update) for rule in self.rules)


class Update:

    def __init__(self, rules, numbers):
        self.rules = rules
        self.numbers = numbers
        print(f"Update: {numbers!r}")

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
rules = Rules()
for line in sys.stdin:
    if "|" in line:
        rules.add(*[int(x) for x in line.split("|")])
    if "," in line:
        update = Update(rules, [int(x) for x in line.split(",")])
        if update.is_in_correct_order():
            total += update.middle_number()
print(total)
