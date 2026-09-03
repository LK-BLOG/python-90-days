# Day 12 - Challenge 1: 包结构设计
# 难度: ⭐⭐⭐☆☆
#
# 要求: 创建一个标准 Python 包的完整结构
# 参考 challenge.md

"""
包结构设计挑战 — 创建符合最佳实践的 Python 包

目标结构:
    my_toolkit/
        __init__.py
        string_utils.py
        file_utils.py
        validators.py
        _internal.py
"""

from __future__ import annotations


# ===== string_utils 模拟 =====

def reverse(s: str) -> str:
    """反转字符串

    Args:
        s: 输入字符串

    Returns:
        反转后的字符串

    Example:
        >>> reverse("hello")
        'olleh'
    """
    # TODO: 实现字符串反转
    pass


def is_palindrome(s: str) -> bool:
    """判断是否为回文字符串（忽略大小写和空格）

    Args:
        s: 输入字符串

    Returns:
        是否为回文

    Example:
        >>> is_palindrome("Racecar")
        True
    """
    # TODO: 去空格转小写后判断回文
    pass


def word_count(s: str) -> dict[str, int]:
    """统计单词出现次数

    Args:
        s: 输入文本

    Returns:
        {word: count} 字典

    Example:
        >>> word_count("a b a c a")
        {'a': 3, 'b': 1, 'c': 1}
    """
    # TODO: 分词 -> 统计 -> 返回字典
    pass


# ===== file_utils 模拟 =====

def ensure_dir(path: str) -> str:
    """确保目录存在，不存在则创建

    Args:
        path: 目录路径

    Returns:
        创建或已存在的目录路径
    """
    # TODO: 用 os.makedirs(exist_ok=True) 实现
    pass


def count_lines(filepath: str) -> int:
    """统计文件行数

    Args:
        filepath: 文件路径

    Returns:
        行数（文件不存在返回 0）

    Raises:
        FileNotFoundError: 文件不存在且非静默模式
    """
    # TODO: 打开文件逐行计数
    pass


# ===== validators 模拟 =====

def validate_range(value, min_val=None, max_val=None, name: str = "value"):
    """通用范围验证

    Args:
        value: 待验证的值
        min_val: 最小值
        max_val: 最大值
        name: 参数名（用于错误信息）

    Raises:
        ValueError: 验证失败时抛出
    """
    # TODO: 检查类型、最小值、最大值
    pass


def validate_not_empty(value, name: str = "value"):
    """非空验证

    Args:
        value: 待验证的值
        name: 参数名

    Raises:
        ValueError: 值为空时抛出
    """
    # TODO: 检查字符串非空（strip 后）
    pass


# ===== _internal 模拟 — 约定以 _ 开头为内部模块 =====

_VERSION = "1.0.0"


def _internal_helper():
    """内部辅助函数，不对外暴露"""
    return _VERSION


# ===== __init__.py 统一导出 =====
__all__ = [
    "reverse",
    "is_palindrome",
    "word_count",
    "ensure_dir",
    "count_lines",
    "validate_range",
    "validate_not_empty",
    "_VERSION",
]


# ---- 测试 ----
if __name__ == "__main__":
    print("=== 包结构设计测试 ===")

    print(reverse("hello"))
    print(is_palindrome("Racecar"))
    print(word_count("a b a c a"))

    try:
        validate_range(10, min_val=0, max_val=5, name="score")
    except ValueError as e:
        print(f"验证失败: {e}")

    validate_not_empty("hello")
    print(f"版本: {_VERSION}")

    print("✅ Challenge 01 完成")
