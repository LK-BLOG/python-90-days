# -*- coding: utf-8 -*-
from collections import Counter, defaultdict, deque, namedtuple

# Counter
words = ["apple", "banana", "apple", "cherry"]
print(Counter(words).most_common(2))

# defaultdict
grouped = defaultdict(list)
for k, v in [("a", 1), ("a", 2), ("b", 3)]:
    grouped[k].append(v)
print(dict(grouped))

# deque
dq = deque([1, 2, 3], maxlen=5)
dq.appendleft(0)
print(dq)

# namedtuple
Point = namedtuple("Point", ["x", "y"])
p = Point(3, 4)
print(p.x, p.y)
