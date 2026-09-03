# -*- coding: utf-8 -*-
square = lambda x: x ** 2
print(square(5))

students = [("张三", 85), ("李四", 92), ("王五", 78)]
by_score = sorted(students, key=lambda s: s[1], reverse=True)
print(by_score)
