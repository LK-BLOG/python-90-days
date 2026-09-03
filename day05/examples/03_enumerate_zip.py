# -*- coding: utf-8 -*-
for i, name in enumerate(["张三", "李四", "王五"], 1):
    print(f"{i}. {name}")

names = ["张三", "李四"]
ages = [25, 30]
for n, a in zip(names, ages):
    print(f"{n}: {a}")
