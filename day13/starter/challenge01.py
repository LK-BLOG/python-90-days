# Day 13 - Challenge 1: 学生计数器
# 难度: ⭐⭐⭐☆☆
#
# 要求: 用类属性实现自动计数
# 参考 challenge.md

"""
学生计数器挑战 — 掌握类属性 vs 实例属性、__del__ 生命周期

核心知识点:
- 类属性：所有实例共享
- 实例属性：每个实例独有
- __init__ / __del__ 生命周期
"""


class Student:
    """学生类，自动追踪学生总数

    类属性:
        total_count: 当前存活的学生实例数

    实例属性:
        name: 姓名
        age: 年龄
        scores: 成绩列表
    """

    total_count = 0  # 类属性：追踪学生总数

    def __init__(self, name: str, age: int, scores: list[int] = None):
        """初始化学生

        Args:
            name: 学生姓名
            age: 年龄
            scores: 成绩列表（默认空列表）
        """
        # TODO:
        # 1. 设置 name, age, scores
        # 2. total_count += 1
        pass

    def __del__(self):
        """析构函数，实例被销毁时调用"""
        # TODO: total_count -= 1
        pass

    def average_score(self) -> float:
        """计算平均分

        Returns:
            平均分（无成绩时返回 0.0）
        """
        # TODO: sum(scores) / len(scores)
        pass

    def add_score(self, score: int) -> None:
        """添加成绩

        Args:
            score: 成绩分数

        Raises:
            ValueError: 分数不在 0-100 范围
        """
        # TODO: 范围检查 -> 添加到 scores
        pass

    def is_passing(self, passing_score: int = 60) -> bool:
        """是否所有科目都及格"""
        # TODO: 检查所有分数 >= passing_score
        pass

    def __repr__(self) -> str:
        # TODO: 返回 Student(name='Alice', age=20, avg=89.0)
        pass


# ---- 测试 ----
if __name__ == "__main__":
    print("=== 学生计数器测试 ===")
    print(f"初始总数: {Student.total_count}")  # 0

    s1 = Student("Alice", 20, [90, 85, 92])
    s2 = Student("Bob", 21, [78, 82, 85])
    print(f"创建2人后: {Student.total_count}")  # 2

    print(f"s1 平均分: {s1.average_score()}")
    print(f"s1 及格: {s1.is_passing()}")

    del s1
    print(f"删除1人后: {Student.total_count}")  # 1

    print("✅ Challenge 01 完成")
