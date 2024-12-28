import sys

left = []
right = {}

for line in sys.stdin:
    x, y = line.split("   ")
    left.append(int(x))
    xx = int(y)
    if xx in right:
        right[xx] += 1
    else:
        right[xx] = 1

total = 0
for x in left:
    total += right.get(x, 0) * x

print(total)
