# -*- coding: utf-8 -*-
# Day 1 练习1: 参数基础

# 练习1: 位置参数
# 实现一个函数，接收name和price两个参数，打印 "商品{name}的价格是{price}元"
def show_price(name, price):
    # TODO: 实现函数
    pass

show_price("iPhone", 5999)  # 应输出：商品iPhone的价格是5999元

# 练习2: 关键字参数
# 使用关键字参数调用show_price
# TODO: 下面的调用
# show_price(???)

# 练习3: 默认参数
# 实现一个函数，接收name和greeting(默认为"你好")
def greet(name, greeting=None):
    # TODO: 如果greeting为None，设为"你好"
    pass

greet("小明")         # 应输出：你好，小明
greet("小明", "早上好")  # 应输出：早上好，小明
