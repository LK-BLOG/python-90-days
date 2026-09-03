# -*- coding: utf-8 -*-
# Day 1 示例2: 默认参数与可变对象陷阱

def connect(host, port=3306, user="root", password=""):
    print(f"连接到 {user}@{host}:{port}")
    return {"host": host, "port": port, "user": user}

conn = connect("localhost")
conn = connect("192.168.1.1", port=5432)

# 可变对象陷阱
print("\n--- 可变默认参数陷阱 ---")

def bad_append(item, lst=[]):
    """错误：可变默认参数"""
    lst.append(item)
    return lst

print(bad_append(1))  # [1]
print(bad_append(2))  # [1, 2] — 不是[2]！

def good_append(item, lst=None):
    """正确：用None作为默认值"""
    if lst is None:
        lst = []
    lst.append(item)
    return lst

print(good_append(1))  # [1]
print(good_append(2))  # [2] — 正确了！
