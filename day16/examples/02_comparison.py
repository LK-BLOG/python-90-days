"""比较运算符"""
from functools import total_ordering

@total_ordering
class Student:
    def __init__(self, name, score):
        self.name, self.score = name, score
    def __eq__(self, other):
        return self.score == other.score
    def __lt__(self, other):
        return self.score < other.score
    def __repr__(self):
        return f'{self.name}({self.score})'

students = [Student('Alice', 90), Student('Bob', 85), Student('Charlie', 95)]
print(sorted(students))  # [Bob(85), Alice(90), Charlie(95)]
print(max(students))     # Charlie(95)
