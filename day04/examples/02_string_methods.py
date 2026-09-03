# -*- coding: utf-8 -*-
csv_line = "张三,25,北京"
parts = csv_line.split(",")
print(parts)

words = ["Hello", "World"]
print(" ".join(words))

text = "  Hello World  "
print(text.strip().lower().replace("world", "Python"))
