# -*- coding: utf-8 -*-
# Day 1 示例1: 参数基础

def greet(name, age):
    """基本的位置参数"""
    print(f"你好，我叫{name}，今年{age}岁")

# 位置调用
greet("小明", 25)

# 关键字调用
greet(name="小红", age=22)

# 混合调用（位置参数在前）
greet("小刚", age=30)
