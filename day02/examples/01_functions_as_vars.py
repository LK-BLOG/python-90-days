# -*- coding: utf-8 -*-
def greet(name):
    return f"你好, {name}!"
say_hello = greet
print(say_hello("小明"))

operations = {"add": lambda a, b: a + b, "sub": lambda a, b: a - b}
print(operations["add"](3, 5))
