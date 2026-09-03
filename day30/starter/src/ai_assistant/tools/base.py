"""Day 30 - 工具基础模块

定义 BaseTool 抽象基类和 ToolResult 数据类。
"""
from __future__ import annotations

import abc
from dataclasses import dataclass, field
from typing import Any


@dataclass
class ToolResult:
    """工具执行结果"""
    success: bool
    output: str = ""
    error: str = ""
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "success": self.success,
            "output": self.output,
            "error": self.error,
        }


class BaseTool(abc.ABC):
    """工具抽象基类

    所有工具必须继承此类并实现 execute 方法。
    """

    @property
    @abc.abstractmethod
    def name(self) -> str:
        """工具名称"""
        ...

    @property
    @abc.abstractmethod
    def description(self) -> str:
        """工具描述"""
        ...

    @property
    @abc.abstractmethod
    def parameters_schema(self) -> dict:
        """JSON Schema 格式的参数定义"""
        ...

    @abc.abstractmethod
    async def execute(self, **kwargs) -> ToolResult:
        """执行工具

        Args:
            **kwargs: 工具参数

        Returns:
            ToolResult 执行结果
        """
        ...

    def get_definition(self) -> dict:
        """获取 OpenAI Function Calling 格式的工具定义

        Returns:
            工具定义字典
        """
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters_schema,
            },
        }
