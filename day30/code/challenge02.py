# Challenge 2 Starter: 工具注册系统

from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass
class ToolResult:
    success: bool
    content: str
    error: str | None = None


class BaseTool(ABC):
    @property
    @abstractmethod
    def name(self) -> str: ...
    @property
    @abstractmethod
    def description(self) -> str: ...
    @property
    @abstractmethod
    def parameters(self) -> dict: ...
    @abstractmethod
    async def execute(self, **kwargs) -> ToolResult: ...
    def to_openai_format(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters,
            }
        }


class ToolRegistry:
    def __init__(self):
        self._tools: dict[str, BaseTool] = {}

    def register(self, tool: BaseTool) -> BaseTool:
        # TODO: 注册工具
        ...

    async def execute(self, name: str, **kwargs) -> ToolResult:
        # TODO: 执行工具
        ...

    def get_definitions(self) -> list[dict]:
        # TODO: 返回OpenAI格式定义
        ...

    def list_tools(self) -> list[str]:
        return list(self._tools.keys())


# TODO: 实现 FileReadTool 和 CalculatorTool
# class FileReadTool(BaseTool): ...
# class CalculatorTool(BaseTool): ...
