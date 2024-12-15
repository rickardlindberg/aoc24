import sys

left = []
right = []

for line in sys.stdin:
    x, y = line.split("   ")
    left.append(int(x))
    right.append(int(y))

left.sort()
right.sort()

total = 0
for x, y in zip(left, right):
    total += abs(x - y)

print(total)
