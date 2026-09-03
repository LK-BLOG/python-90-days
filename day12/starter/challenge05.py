# Day 12 - Challenge 5: 包版本管理
# 难度: ⭐⭐⭐⭐☆
#
# 要求: 实现版本号管理、兼容性检查
# 参考 challenge.md

"""
包版本管理挑战 — 学习语义化版本和兼容性管理

核心知识点:
- 语义化版本号 (SemVer): MAJOR.MINOR.PATCH
- 版本比较
- 兼容性约束解析
"""

from dataclasses import dataclass
from enum import Enum


class BumpType(Enum):
    """版本升级类型"""
    MAJOR = "major"  # 不兼容的 API 修改
    MINOR = "minor"  # 向后兼容的功能新增
    PATCH = "patch"  # 向后兼容的问题修正


@dataclass(frozen=True)
class Version:
    """语义化版本号

    Attributes:
        major: 主版本号
        minor: 次版本号
        patch: 补丁版本号

    Example:
        v = Version(1, 2, 3)
        str(v) == "1.2.3"
    """
    major: int = 0
    minor: int = 1
    patch: int = 0

    def __str__(self) -> str:
        """返回 'MAJOR.MINOR.PATCH' 格式"""
        # TODO: 拼接版本号字符串
        pass

    def __gt__(self, other: "Version") -> bool:
        """大于比较"""
        # TODO: 按 major > minor > patch 顺序比较
        pass

    def __lt__(self, other: "Version") -> bool:
        # TODO
        pass

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Version):
            return NotImplemented
        return (self.major, self.minor, self.patch) == (other.major, other.minor, other.patch)

    def __ge__(self, other: "Version") -> bool:
        return self > other or self == other

    def __le__(self, other: "Version") -> bool:
        return self < other or self == other

    @classmethod
    def parse(cls, version_str: str) -> "Version":
        """解析版本字符串

        Args:
            version_str: "MAJOR.MINOR.PATCH" 格式

        Returns:
            Version 实例

        Raises:
            ValueError: 格式不正确时抛出

        Example:
            >>> Version.parse("1.2.3")
            Version(major=1, minor=2, patch=3)
        """
        # TODO: split(".") -> 转 int -> 构造 Version
        pass

    def bump(self, bump_type: BumpType) -> "Version":
        """升级版本号

        Args:
            bump_type: 升级类型

        Returns:
            新的 Version 实例

        Example:
            >>> Version(1, 2, 3).bump(BumpType.MINOR)
            Version(major=1, minor=3, patch=0)
        """
        # TODO: 根据类型升级对应位，低位归零
        pass


class CompatibilityChecker:
    """版本兼容性检查器

    支持 PEP 440 风格的兼容性约束（简化版）。
    """

    def __init__(self):
        # TODO: 存储已注册的包版本 {name: Version}
        pass

    def register(self, name: str, version: Version) -> None:
        """注册包版本"""
        # TODO: 存入字典
        pass

    def check_compatible(self, name: str, constraint: str) -> bool:
        """检查是否满足兼容性约束

        Args:
            name: 包名
            constraint: 约束字符串，如 ">=1.0,<2.0"

        Returns:
            是否兼容

        Constraint 格式支持:
            - >=1.0  : 大于等于
            - <2.0   : 小于
            - ==1.5  : 等于
            - >=1.0,<2.0: 组合约束（逗号分隔，全部满足）
        """
        # TODO: 解析约束字符串 -> 获取包版本 -> 逐个检查
        pass


# ---- 测试 ----
if __name__ == "__main__":
    print("=== 版本管理测试 ===")

    v1 = Version(1, 2, 3)
    v2 = Version(2, 0, 0)
    v3 = Version(1, 2, 3)

    print(f"v1 = {v1}")
    print(f"v2 = {v2}")
    print(f"v1 < v2: {v1 < v2}")
    print(f"v1 == v3: {v1 == v3}")

    v4 = Version.parse("3.1.4")
    print(f"parsed: {v4}")

    bumped = v1.bump(BumpType.MINOR)
    print(f"v1 bumped minor: {bumped}")

    checker = CompatibilityChecker()
    checker.register("requests", Version(2, 28, 0))
    print(f"兼容 >=2.20: {checker.check_compatible('requests', '>=2.20')}")
    print(f"兼容 <2.0: {checker.check_compatible('requests', '<2.0')}")

    print("✅ Challenge 05 完成")
