# Day 11 - Ultimate: 模块系统终极挑战
# 难度: ⭐⭐⭐⭐⭐
#
# 要求: 设计并实现一个插件系统，支持动态加载模块
# 参考 ultimate_challenge.md

"""
插件系统终极挑战 — 综合运用模块系统的所有知识

任务:
- 设计插件发现机制
- 实现动态加载和注册
- 插件生命周期管理
- 配置化插件行为
"""

import os
import json
from abc import ABC, abstractmethod


# ===== 插件基类 =====
class PluginBase(ABC):
    """插件基类，所有插件必须继承此类

    插件生命周期:
        __init__ -> activate() -> run() -> deactivate()
    """

    name: str = "unnamed"
    version: str = "0.0.1"
    description: str = ""

    def __init__(self):
        self._active = False
        self._config = {}

    @abstractmethod
    def activate(self) -> None:
        """激活插件"""
        # TODO: 子类实现
        pass

    @abstractmethod
    def run(self, *args, **kwargs):
        """执行插件逻辑"""
        # TODO: 子类实现
        pass

    @abstractmethod
    def deactivate(self) -> None:
        """停用插件"""
        # TODO: 子类实现
        pass

    def is_active(self) -> bool:
        """是否已激活"""
        # TODO: 返回 _active 状态
        pass

    def configure(self, config: dict) -> None:
        """配置插件

        Args:
            config: 配置字典
        """
        # TODO: 更新 _config
        pass


# ===== 插件管理器 =====
class PluginManager:
    """插件管理器 — 发现、加载、管理插件

    Features:
        - 从指定目录发现插件
        - 动态加载和注册
        - 生命周期管理
    """

    def __init__(self, plugin_dir: str = "plugins"):
        # TODO: 初始化插件目录和插件注册表
        pass

    def discover(self) -> list[str]:
        """发现插件目录下的所有插件

        Returns:
            发现的插件名列表
        """
        # TODO: 扫描 plugin_dir，找到包含 __init__.py 的子目录
        pass

    def register(self, plugin: PluginBase) -> None:
        """注册一个插件实例

        Args:
            plugin: 插件实例

        Raises:
            ValueError: 插件名已注册时抛出
        """
        # TODO: 检查重复 -> 注册到字典 -> 激活插件
        pass

    def unregister(self, name: str) -> bool:
        """注销指定插件

        Returns:
            是否成功注销
        """
        # TODO: 停用 -> 从注册表移除
        pass

    def get(self, name: str) -> PluginBase | None:
        """获取插件实例"""
        # TODO: 从注册表查找
        pass

    def list_plugins(self) -> list[dict]:
        """列出所有已注册插件的信息

        Returns:
            [{"name": ..., "version": ..., "active": ...}, ...]
        """
        # TODO: 遍历注册表，返回摘要信息
        pass

    def run_plugin(self, name: str, *args, **kwargs):
        """执行指定插件

        Raises:
            KeyError: 插件未注册时抛出
            RuntimeError: 插件未激活时抛出
        """
        # TODO: 查找 -> 检查激活状态 -> 执行
        pass


# ===== 示例插件 =====
class HelloPlugin(PluginBase):
    """示例插件：打印问候语"""

    name = "hello"
    version = "1.0.0"
    description = "打印问候语的示例插件"

    def activate(self) -> None:
        # TODO: 设置 _active = True
        pass

    def run(self, name: str = "World") -> str:
        # TODO: 返回 f"Hello, {name}!"
        pass

    def deactivate(self) -> None:
        # TODO: 设置 _active = False
        pass


class MathPlugin(PluginBase):
    """示例插件：简单数学运算"""

    name = "math"
    version = "1.0.0"
    description = "数学运算插件"

    def activate(self) -> None:
        pass

    def run(self, operation: str = "add", *args) -> float:
        # TODO: 根据 operation 执行加减乘除
        pass

    def deactivate(self) -> None:
        pass


# ---- 测试 ----
if __name__ == "__main__":
    print("=== 插件系统终极挑战 ===")

    mgr = PluginManager()

    # 注册插件
    hello = HelloPlugin()
    math_p = MathPlugin()
    mgr.register(hello)
    mgr.register(math_p)

    # 列出插件
    for p in mgr.list_plugins():
        print(p)

    # 执行插件
    print(mgr.run_plugin("hello", "Python"))
    print(mgr.run_plugin("math", "add", 2, 3))

    # 注销
    mgr.unregister("hello")
    print(mgr.list_plugins())

    print("✅ Ultimate 完成")
