# 工具注册器
# TODO: 实现 ToolRegistry 类

from __future__ import annotations
# from abc import ABC, abstractmethod
# from dataclasses import dataclass

# TODO:
# @dataclass
# class ToolResult:
#     success: bool
#     content: str
#     error: str | None = None
#
# class BaseTool(ABC):
#     name, description, parameters 属性
#     async def execute(**kwargs) -> ToolResult
#     def to_openai_format() -> dict
#
# class ToolRegistry:
#     def register(self, tool): ...
#     async def execute(self, name, **kwargs) -> ToolResult: ...
#     def get_definitions(self) -> list[dict]: ...
#     def list_tools(self) -> list[str]: ...
