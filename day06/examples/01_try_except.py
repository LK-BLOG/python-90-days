# -*- coding: utf-8 -*-
try:
    result = 10 / 0
except ZeroDivisionError as e:
    print(f"错误: {e}")
finally:
    print("清理工作")
