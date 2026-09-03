"""Day 30 - 搜索工具"""
from __future__ import annotations

import subprocess
from pathlib import Path
from ai_assistant.tools.base import BaseTool, ToolResult


class SearchTool(BaseTool):
    """文件内容搜索工具（grep-like）"""

    @property
    def name(self) -> str:
        return "search"

    @property
    def description(self) -> str:
        return "在文件中搜索指定文本或正则表达式"

    @property
    def parameters_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "pattern": {"type": "string", "description": "搜索模式（支持正则）"},
                "path": {"type": "string", "description": "搜索目录", "default": "."},
                "file_pattern": {"type": "string", "description": "文件名模式", "default": "*.py"},
            },
            "required": ["pattern"],
        }

    async def execute(self, pattern: str = "", path: str = ".",
                      file_pattern: str = "*.py", **kwargs) -> ToolResult:
        """搜索文件内容"""
        # TODO: 使用 pathlib + 正则搜索
        # TODO: 返回匹配结果
        try:
            results = []
            search_dir = Path(path)
            for f in search_dir.rglob(file_pattern):
                try:
                    lines = f.read_text(encoding="utf-8", errors="replace").splitlines()
                    for i, line in enumerate(lines, 1):
                        if pattern.lower() in line.lower():
                            results.append(f"{f}:{i}: {line.strip()}")
                except Exception:
                    continue
                if len(results) >= 50:
                    break
            if not results:
                return ToolResult(success=True, output="未找到匹配结果")
            return ToolResult(success=True, output="\n".join(results))
        except Exception as e:
            return ToolResult(success=False, error=str(e))
