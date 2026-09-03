# 示例：模块系统基础
# 注意：这个示例需要创建多个模块文件

# 首先创建示例模块
import sys
from pathlib import Path

# 创建示例模块目录
example_dir = Path("module_examples")
example_dir.mkdir(exist_ok=True)

# 创建math_utils.py模块
math_utils_content = '''
"""数学工具模块"""

__all__ = ['add', 'subtract', 'multiply', 'divide', 'Calculator']

def add(a, b):
    """两数相加"""
    return a + b

def subtract(a, b):
    """两数相减"""
    return a - b

def multiply(a, b):
    """两数相乘"""
    return a * b

def divide(a, b):
    """两数相除"""
    if b == 0:
        raise ValueError("除数不能为零")
    return a / b

class Calculator:
    """计算器类"""
    
    def __init__(self):
        self.history = []
    
    def calculate(self, operation, a, b):
        """执行计算"""
        if operation == "+":
            result = add(a, b)
        elif operation == "-":
            result = subtract(a, b)
        elif operation == "*":
            result = multiply(a, b)
        elif operation == "/":
            result = divide(a, b)
        else:
            raise ValueError(f"不支持的操作: {operation}")
        
        self.history.append((operation, a, b, result))
        return result

if __name__ == "__main__":
    # 直接运行时执行
    print("数学工具模块")
    print(f"2 + 3 = {add(2, 3)}")
    print(f"10 - 4 = {subtract(10, 4)}")
'''

# 创建string_utils.py模块
string_utils_content = '''
"""字符串工具模块"""

__all__ = ['capitalize_words', 'reverse_string', 'count_words', 'truncate']

def capitalize_words(text):
    """每个单词首字母大写"""
    return text.title()

def reverse_string(text):
    """反转字符串"""
    return text[::-1]

def count_words(text):
    """统计单词数"""
    return len(text.split())

def truncate(text, max_length=100, suffix="..."):
    """截断字符串"""
    if len(text) <= max_length:
        return text
    return text[:max_length-len(suffix)] + suffix

if __name__ == "__main__":
    print("字符串工具模块")
    print(capitalize_words("hello world"))
    print(reverse_string("Python"))
'''

# 写入模块文件
(example_dir / "math_utils.py").write_text(math_utils_content, encoding='utf-8')
(example_dir / "string_utils.py").write_text(string_utils_content, encoding='utf-8')

# 创建__init__.py
init_content = '''
"""模块示例包"""

from . import math_utils
from . import string_utils

__all__ = ['math_utils', 'string_utils']
'''
(example_dir / "__init__.py").write_text(init_content, encoding='utf-8')

# 添加到sys.path
sys.path.insert(0, str(example_dir))

# 现在可以导入模块了
print("=== 导入模块 ===")
import math_utils
print(f"math_utils.add(2, 3) = {math_utils.add(2, 3)}")

import string_utils
print(f"string_utils.capitalize_words('hello world') = {string_utils.capitalize_words('hello world')}")

print("\n=== 使用from导入 ===")
from math_utils import add, subtract
print(f"add(10, 5) = {add(10, 5)}")
print(f"subtract(10, 5) = {subtract(10, 5)}")

print("\n=== 使用别名 ===")
import math_utils as mu
print(f"mu.multiply(4, 5) = {mu.multiply(4, 5)}")

print("\n=== 使用__all__ ===")
print(f"math_utils.__all__ = {math_utils.__all__}")
print(f"string_utils.__all__ = {string_utils.__all__}")

print("\n=== 模块信息 ===")
print(f"math_utils模块文件: {math_utils.__file__}")
print(f"math_utils模块名: {math_utils.__name__}")

# 清理
import shutil
shutil.rmtree(example_dir)

print("\n演示完成，示例模块已删除")
