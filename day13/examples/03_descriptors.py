# 描述符基础

class Validated:
    """属性验证描述符"""

    def __init__(self, min_val=None, max_val=None):
        self.min_val = min_val
        self.max_val = max_val

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return obj.__dict__.get(self.name)

    def __set__(self, obj, value):
        if self.min_val is not None and value < self.min_val:
            raise ValueError(f'{self.name} >= {self.min_val} required')
        if self.max_val is not None and value > self.max_val:
            raise ValueError(f'{self.name} <= {self.max_val} required')
        obj.__dict__[self.name] = value

class Student:
    age = Validated(0, 150)
    score = Validated(0, 100)

    def __init__(self, name, age, score):
        self.name = name
        self.age = age
        self.score = score

s = Student('Alice', 15, 95)
print(s.age, s.score)
# s.age = -5    # ValueError
# s.score = 200 # ValueError
