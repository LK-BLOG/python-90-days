# Day 17 - Challenge 4: 自定义验证
# 难度: ⭐⭐⭐☆☆
#
# 要求: 用 __post_init__ 添加验证
# 参考 challenge.md

"""
自定义验证挑战 — 用 __post_init__ 在初始化后执行验证

核心知识点:
- __post_init__: 初始化后自动调用
- dataclass(frozen=True) 下的验证
- 类型注解与运行时检查
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class CreateUserRequest:
    """用户创建请求 — 带验证"""

    username: str
    email: str
    age: int
    password: str = ""
    confirm_password: str = ""
    role: str = "user"
    bio: str = ""

    def __post_init__(self):
        """初始化后的验证钩子"""
        # TODO: 验证以下规则:
        # 1. username: 3-20 字符，只含字母数字下划线
        # 2. email: 包含 @ 和 .
        # 3. age: 0-150
        # 4. password 和 confirm_password 一致（如果提供了密码）
        # 5. role 必须在 ["admin", "user", "guest"] 中
        pass


@dataclass
class Range:
    """范围类 — 验证最小值 <= 值 <= 最大值"""

    min_val: float
    max_val: float

    def __post_init__(self):
        if self.min_val > self.max_val:
            raise ValueError(
                f"最小值 {self.min_val} 不能大于最大值 {self.max_val}"
            )

    def contains(self, value: float) -> bool:
        """是否在范围内"""
        return self.min_val <= value <= self.max_val

    def clamp(self, value: float) -> float:
        """将值限制在范围内"""
        return max(self.min_val, min(self.max_val, value))

    def overlaps(self, other: "Range") -> bool:
        """是否与其他范围有重叠"""
        return self.min_val <= other.max_val and other.min_val <= self.max_val

    def __repr__(self) -> str:
        return f"Range({self.min_val}, {self.max_val})"


@dataclass
class Schedule:
    """日程表 — 验证时间逻辑"""

    start_hour: int = 9
    end_hour: int = 17
    break_start: int = 12
    break_end: int = 13

    def __post_init__(self):
        """验证时间逻辑"""
        # TODO: 验证:
        # 1. 0 <= start_hour < end_hour <= 24
        # 2. break 在工作时间内
        pass

    def work_hours(self) -> int:
        """工作时长（减去休息）"""
        total = self.end_hour - self.start_hour
        brk = self.break_end - self.break_start
        return total - brk

    def is_work_time(self, hour: int) -> bool:
        """指定时间是否在工作时段"""
        return (self.start_hour <= hour < self.end_hour and
                not (self.break_start <= hour < self.break_end))


# ---- 测试 ----
if __name__ == "__main__":
    print("=== 自定义验证测试 ===")

    # 正常创建
    req = CreateUserRequest(
        username="alice", email="alice@test.com",
        age=25, password="123456", confirm_password="123456"
    )
    print(f"创建请求: {req}")

    # 验证失败
    try:
        CreateUserRequest(username="ab", email="bad", age=200, password="a", confirm_password="b")
    except ValueError as e:
        print(f"验证失败: {e}")

    # 范围
    r = Range(0, 100)
    print(f"50 在 [0,100] 内: {r.contains(50)}")
    print(f"clamp(150): {r.clamp(150)}")

    # 日程
    sched = Schedule(start_hour=9, end_hour=17)
    print(f"工作时长: {sched.work_hours()}h")
    print(f"10点工作: {sched.is_work_time(10)}")
    print(f"12点休息: {sched.is_work_time(12)}")

    print("✅ Challenge 04 完成")
