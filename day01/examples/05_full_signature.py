# -*- coding: utf-8 -*-
# Day 1 示例5: 完整参数签名

def full_example(pos_only, /, normal, *args, kw_only, **kwargs):
    """展示所有参数类型的组合"""
    print(f"  仅位置参数: {pos_only}")
    print(f"  普通参数:   {normal}")
    print(f"  *args:      {args}")
    print(f"  仅关键字:   {kw_only}")
    print(f"  **kwargs:   {kwargs}")

print("调用 full_example(1, 2, 3, 4, kw_only=5, extra=6):")
full_example(1, 2, 3, 4, kw_only=5, extra=6)
