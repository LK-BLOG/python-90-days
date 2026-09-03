# -*- coding: utf-8 -*-
# Day 1 练习2: *args 和 **kwargs

# 练习1: 求平均值
def average(*numbers):
    # TODO: 计算并返回平均值
    pass

print(average(1, 2, 3))            # 2.0
print(average(10, 20, 30, 40, 50))  # 30.0

# 练习2: 个人信息格式化
def format_profile(name, **info):
    # TODO: 返回字符串 "姓名: {name}, 信息: {键1=值1, 键2=值2, ...}"
    pass

print(format_profile("张三", age=25, city="北京"))
# 输出：姓名: 张三, 信息: age=25, city=北京
