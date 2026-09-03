"""Challenge 2: 分数比较器"""
from functools import total_ordering

@total_ordering
class Score:
    def __init__(self, name, points):
        self.name, self.points = name, points

    # TODO: 实现 __eq__ 和 __lt__
