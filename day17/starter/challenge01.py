# Day 17 - Challenge 1: 基础 dataclass
# 难度: ⭐⭐⭐☆☆
#
# 要求: 创建带默认值的 dataclass
# 参考 challenge.md

"""
基础 dataclass 挑战 — 快速创建数据类

核心知识点:
- @dataclass 装饰器
- field() 函数
- 默认值、默认工厂
"""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Student:
    """学生数据类

    自动获得 __init__, __repr__, __eq__
    """

    name: str
    age: int
    scores: list[int] = field(default_factory=list)
    enrolled_at: datetime = field(default_factory=datetime.now)

    @property
    def average_score(self) -> float:
        """平均分"""
        if not self.scores:
            return 0.0
        return sum(self.scores) / len(self.scores)

    @property
    def is_passing(self) -> bool:
        """是否全部及格（60分以上）"""
        return all(s >= 60 for s in self.scores) if self.scores else False


@dataclass
class Course:
    """课程数据类"""

    name: str
    credits: int = 3
    students: list[Student] = field(default_factory=list)

    def add_student(self, student: Student) -> None:
        """添加学生"""
        if student not in self.students:
            self.students.append(student)

    def top_students(self, n: int = 3) -> list[Student]:
        """返回平均分最高的 n 个学生"""
        # TODO: 按 average_score 降序排序，取前 n 个
        pass

    def pass_rate(self) -> float:
        """及格率"""
        if not self.students:
            return 0.0
        passing = sum(1 for s in self.students if s.is_passing)
        return passing / len(self.students)

    def __post_init__(self):
        """dataclass 初始化后的钩子"""
        if self.credits < 1:
            raise ValueError("学分不能小于1")


# ---- 测试 ----
if __name__ == "__main__":
    print("=== 基础 dataclass 测试 ===")

    s1 = Student("Alice", 20, [90, 85, 92])
    s2 = Student("Bob", 21, [78, 50, 85])
    s3 = Student("Carol", 19, [95, 98, 100])

    print(s1)
    print(f"Alice 平均分: {s1.average_score:.1f}")
    print(f"Bob 及格: {s2.is_passing}")

    course = Course("Python", credits=4)
    for s in [s1, s2, s3]:
        course.add_student(s)

    print(f"及格率: {course.pass_rate():.0%}")
    print(f"Top: {course.top_students(2)}")

    print("✅ Challenge 01 完成")
