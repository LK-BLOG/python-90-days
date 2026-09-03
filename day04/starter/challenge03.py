# Day 4 挑战三：f-string 格式化 (★★★☆☆)
# 难度: ★★★☆☆
# 要求: 掌握 f-string 的各种高级用法。


import math
from datetime import datetime


# ===== 任务1: 基础格式化 =====
name = "Alice"
age = 25
score = 95.678

# TODO: 使用 f-string 格式化
print(f"姓名: {name}, 年龄: {age}")
print(f"分数: {score:.1f}")          # 保留1位小数
print(f"分数: {score:06.2f}")        # 总宽度6，零填充
print(f"左对齐: {name:<10}|")        # 左对齐，宽度10
print(f"居中: {name:^10}|")          # 居中
print(f"右对齐: {name:>10}|")        # 右对齐


# ===== 任务2: 表达式和函数调用 =====
x, y = 3, 4

# TODO: 在 f-string 中使用表达式
print(f"\n{x} + {y} = {x + y}")
print(f"{x} * {y} = {x * y}")
print(f"|{x}| = {abs(-x)}")
print(f"π ≈ {math.pi:.4f}")
print(f"√2 ≈ {math.sqrt(2):.6f}")


# ===== 任务3: 格式化类和对象 =====
class Student:
    def __init__(self, name, score):
        self.name = name
        self.score = score
    
    def __repr__(self):
        return f"Student({self.name!r}, {self.score})"

s = Student("Bob", 92.5)
# TODO: 使用 f-string 调用对象方法和属性
print(f"\n学生: {s}")
print(f"名字长度: {len(s.name)}")
print(f"是否及格: {'✅' if s.score >= 60 else '❌'}")


# ===== 任务4: 字典和列表格式化 =====
scores = {"数学": 95, "英语": 88, "Python": 97}

# TODO: 格式化字典
print("\n成绩单:")
for subject, score in scores.items():
    bar = "█" * (score // 10)
    print(f"  {subject:>4}: {score:3d} {bar}")

# TODO: 列表推导式 + f-string
students = [("Alice", 95), ("Bob", 87), ("Charlie", 92)]
# 生成 Markdown 表格
header = "| " + " | ".join(f"{name:>10}" for name, _ in students) + " |"
separator = "|" + "|".join("-" * 12 for _ in students) + "|"
values = "| " + " | ".join(f"{score:>10}" for _, score in students) + " |"
print(f"\n{header}\n{separator}\n{values}")


# ===== 任务5: 实用格式化函数 =====

def format_bytes(size):
    """将字节数格式化为人类可读的大小。
    
    功能说明:
        自动选择合适的单位 (B, KB, MB, GB, TB)。
    
    示例:
        >>> format_bytes(1536)
        "1.50 KB"
        >>> format_bytes(1073741824)
        "1.00 GB"
    
    Args:
        size: 字节数（整数或浮点数）
    
    Returns:
        str: 格式化后的大小字符串
    """
    # TODO: 实现字节单位转换
    # 提示: 使用循环和 f-string 的格式化功能
    pass


def format_duration(seconds):
    """将秒数格式化为时分秒。
    
    示例:
        >>> format_duration(3661)
        "1小时 1分钟 1秒"
        >>> format_duration(45)
        "45秒"
    
    Args:
        seconds: 秒数
    
    Returns:
        str: 格式化后的时长字符串
    """
    # TODO: 实现时间格式化
    pass


def format_table(headers, rows, padding=2):
    """生成格式化的文本表格。
    
    Args:
        headers: 表头列表
        rows: 数据行列表（每个元素是值的列表）
        padding: 列间距
    
    Returns:
        str: 格式化的文本表格
    """
    # TODO: 计算每列最大宽度
    # TODO: 使用 f-string 生成对齐的表格
    pass


# ===== 测试 =====
if __name__ == "__main__":
    print("\n=== format_bytes ===")
    print(f"  1024 B = {format_bytes(1024)}")
    print(f"  1.5 MB = {format_bytes(1.5 * 1024 * 1024)}")
    print(f"  2.3 GB = {format_bytes(2.3 * 1024 ** 3)}")
    
    print("\n=== format_duration ===")
    print(f"  3661s = {format_duration(3661)}")
    print(f"  45s = {format_duration(45)}")
    print(f"  86400s = {format_duration(86400)}")
    
    print("\n=== format_table ===")
    headers = ["姓名", "年龄", "城市"]
    rows = [["Alice", 25, "北京"], ["Bob", 30, "上海"], ["Charlie", 22, "广州"]]
    print(format_table(headers, rows))
