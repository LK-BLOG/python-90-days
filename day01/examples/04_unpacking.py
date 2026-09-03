# -*- coding: utf-8 -*-
# Day 1 示例4: 参数解包

def calculate(a, b, c):
    return a * 2 + b * 3 + c * 5

# * 解包列表/元组
values = [10, 20, 30]
result = calculate(*values)
print(f"结果: {result}")  # 10*2 + 20*3 + 30*5 = 220

# ** 解包字典
params = {"a": 10, "b": 20, "c": 30}
result = calculate(**params)
print(f"结果: {result}")

# 合并字典（新语法）
defaults = {"theme": "dark", "lang": "zh"}
user_settings = {"theme": "light", "font_size": 16}
config = {**defaults, **user_settings}
print(f"配置: {config}")
