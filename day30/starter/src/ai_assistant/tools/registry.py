"""Day 30 - 工具注册器"""
from __future__ import annotations

from typing import Any
from ai_assistant.tools.base import BaseTool, ToolResult


class ToolRegistry:
    """工具注册器

    管理所有已注册的工具，支持按名查找和批量获取定义。
    """

    def __init__(self):
        self._tools: dict[str, BaseTool] = {}

    def register(self, tool: BaseTool) -> None:
        """注册一个工具实例

        Args:
            tool: BaseTool 子类实例
        """
        # TODO: 将 tool 存入 _tools 字典
        ...

    def get(self, name: str) -> BaseTool | None:
        """按名称获取工具

        Args:
            name: 工具名

        Returns:
            工具实例或 None
        """
        return self._tools.get(name)

    async def execute(self, name: str, arguments: dict[str, Any]) -> ToolResult:
        """执行指定工具

        Args:
            name: 工具名
            arguments: 参数字典

        Returns:
            ToolResult 执行结果
        """
        # TODO: 查找工具，调用 execute
        tool = self.get(name)
        if not tool:
            return ToolResult(success=False, error=f"工具 {name} 不存在")
        return await tool.execute(**arguments)

    def get_definitions(self) -> list[dict]:
        """获取所有工具的 OpenAI 格式定义

        Returns:
            工具定义列表
        """
        # TODO: 返回所有工具的 get_definition()
        ...

    def list_names(self) -> list[str]:
        """列出所有工具名"""
        return list(self._tools.keys())
