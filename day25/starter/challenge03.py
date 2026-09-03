# Day 25 - Challenge 3: Mock 模拟器
# 难度: ⭐⭐⭐
# 自动记录调用、参数验证、返回值配置、调用计数检查

from dataclasses import dataclass, field
from typing import Any, Callable
from unittest.mock import MagicMock


class MockFunction:
    """自定义 Mock 函数

    记录调用历史、验证参数、配置返回值。
    """

    def __init__(self, name: str = "mock", return_value: Any = None,
                 side_effect: Any = None):
        """初始化 Mock 函数

        Args:
            name: Mock 名称（用于调试）
            return_value: 固定返回值
            side_effect: 异常或可调用对象（每次调用执行）
        """
        self.name = name
        self.return_value = return_value
        self.side_effect = side_effect
        # TODO: 初始化调用记录
        self._call_count: int = 0
        self._call_args: list[tuple] = []
        self._call_kwargs: list[dict] = []

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """模拟函数调用

        Args:
            *args: 位置参数
            **kwargs: 关键字参数

        Returns:
            配置的返回值或 side_effect 结果
        """
        # TODO: 记录调用参数
        # TODO: 处理 side_effect（异常或可调用）
        # TODO: 返回 return_value
        ...

    def assert_called(self) -> None:
        """断言至少被调用过一次"""
        # TODO: 如果未调用，抛出 AssertionError
        ...

    def assert_called_once(self) -> None:
        """断言只被调用过一次"""
        ...

    def assert_called_with(self, *args: Any, **kwargs: Any) -> None:
        """断言最后一次调用的参数"""
        ...

    def assert_called_times(self, n: int) -> None:
        """断言调用次数

        Args:
            n: 期望的调用次数
        """
        ...

    def reset(self) -> None:
        """重置所有调用记录"""
        # TODO: 清空所有记录
        ...


class MockFactory:
    """Mock 工厂，批量创建和管理 Mock 对象"""

    def __init__(self):
        self._mocks: dict[str, MockFunction] = {}

    def create(self, name: str, **kwargs) -> MockFunction:
        """创建一个 Mock 函数并注册

        Args:
            name: Mock 名称
            **kwargs: 传递给 MockFunction 的参数

        Returns:
            创建的 MockFunction
        """
        # TODO: 创建 MockFunction 并存入 _mocks
        ...

    def verify_all(self) -> list[str]:
        """验证所有 Mock 是否被调用过

        Returns:
            未被调用的 Mock 名称列表
        """
        # TODO: 检查所有 mock 的调用计数
        ...

    def reset_all(self) -> None:
        """重置所有 Mock"""
        ...


# ==================== 测试 ====================
if __name__ == "__main__":
    factory = MockFactory()
    api_call = factory.create("api_call", return_value={"status": "ok"})

    # 模拟调用
    result = api_call("https://example.com")
    print(f"返回值: {result}")

    api_call.assert_called()
    api_call.assert_called_with("https://example.com")
    print(f"调用次数: {api_call._call_count}")

    # 验证所有 mock
    unvisited = factory.verify_all()
    print(f"未调用的 Mock: {unvisited}")
