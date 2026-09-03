# Day 11 - Challenge 4: 自定义导入机制
# 难度: ⭐⭐⭐⭐☆
#
# 要求: 模拟自定义的模块导入和查找机制
# 参考 challenge.md

"""
自定义导入机制挑战 — 理解 Python 模块加载原理

核心概念:
- sys.path 查找顺序
- importlib 的基本用法
- 模块缓存机制
- __import__ 函数
"""

import sys
import types
from importlib import import_module


# ===== 挑战1: 模拟模块缓存 =====
class ModuleCache:
    """简易模块缓存管理器

    模拟 Python 的 sys.modules 缓存机制。
    """

    def __init__(self):
        # TODO: 初始化缓存字典
        pass

    def register(self, name: str, module) -> None:
        """注册一个模块到缓存

        Args:
            name: 模块名
            module: 模块对象
        """
        # TODO: 存入缓存
        pass

    def get(self, name: str):
        """从缓存获取模块

        Args:
            name: 模块名

        Returns:
            模块对象或 None
        """
        # TODO: 返回缓存中的模块
        pass

    def has(self, name: str) -> bool:
        """检查模块是否已缓存"""
        # TODO: 检查是否存在
        pass

    def clear(self) -> None:
        """清空缓存"""
        # TODO: 清空
        pass


# ===== 挑战2: 自定义模块查找器 =====
class SimpleModuleFinder:
    """简易模块查找器

    模拟 Python 的模块查找机制。
    支持从指定路径列表中查找模块。
    """

    def __init__(self, search_paths: list = None):
        # TODO: 设置搜索路径列表
        pass

    def add_path(self, path: str) -> None:
        """添加搜索路径"""
        # TODO: 添加到搜索路径
        pass

    def find_module(self, module_name: str) -> str | None:
        """查找模块文件路径

        Args:
            module_name: 模块名（如 "utils.string"）

        Returns:
            找到的文件路径，或 None

        Hint:
            遍历 search_paths，拼接 module_name + ".py" 检查文件是否存在
        """
        # TODO: 实现查找逻辑
        pass


# ===== 挑战3: 动态模块创建 =====
def create_module(name: str, attrs: dict = None) -> types.ModuleType:
    """动态创建一个模块

    Args:
        name: 模块名
        attrs: 模块属性字典 {name: value}

    Returns:
        新创建的模块对象

    Example:
        >>> m = create_module("math_utils", {"pi": 3.14})
        >>> m.pi
        3.14
    """
    # TODO: 使用 types.ModuleType 创建模块
    # 1. 创建 ModuleType 实例
    # 2. 设置 attrs 中的属性
    # 3. 注册到 sys.modules
    # 4. 返回模块对象
    pass


# ===== 挑战4: import 别名 =====
def import_as(module_name: str, alias: str):
    """带别名的导入

    Args:
        module_name: 原模块名
        alias: 别名

    Returns:
        导入的模块

    Example:
        >>> os = import_as("os", "operating_system")
    """
    # TODO: importlib 导入后绑定到新名字
    pass


# ---- 测试 ----
if __name__ == "__main__":
    print("=== 自定义导入机制测试 ===")

    # 模块缓存
    cache = ModuleCache()
    mod = create_module("test_mod", {"hello": "world"})
    cache.register("test_mod", mod)
    assert cache.has("test_mod")
    assert cache.get("test_mod").hello == "world"
    print("模块缓存: ✅")

    # 查找器
    finder = SimpleModuleFinder([sys.prefix])
    print(f"查找 sys: {finder.find_module('sys')}")

    # 动态模块
    m = create_module("math_utils", {"pi": 3.14, "e": 2.71})
    print(f"动态模块 pi={m.pi}, e={m.e}")

    print("✅ Challenge 04 完成")
