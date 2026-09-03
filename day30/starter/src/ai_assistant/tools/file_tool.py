"""Day 30 - 文件读写工具"""
from __future__ import annotations

from pathlib import Path
from ai_assistant.tools.base import BaseTool, ToolResult


class FileReadTool(BaseTool):
    """文件读取工具"""

    @property
    def name(self) -> str:
        return "file_read"

    @property
    def description(self) -> str:
        return "读取指定路径的文件内容"

    @property
    def parameters_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "文件路径"},
                "encoding": {"type": "string", "description": "文件编码", "default": "utf-8"},
            },
            "required": ["path"],
        }

    async def execute(self, path: str = "", encoding: str = "utf-8", **kwargs) -> ToolResult:
        """读取文件内容"""
        # TODO: 检查文件是否存在
        # TODO: 读取并返回内容
        # TODO: 处理异常
        try:
            p = Path(path)
            if not p.exists():
                return ToolResult(success=False, error=f"文件不存在: {path}")
            content = p.read_text(encoding=encoding)
            return ToolResult(success=True, output=content[:5000])  # 截断大文件
        except Exception as e:
            return ToolResult(success=False, error=str(e))
