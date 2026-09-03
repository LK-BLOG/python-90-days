"""Day 30 - 代码执行工具"""
from __future__ import annotations

import asyncio
from ai_assistant.tools.base import BaseTool, ToolResult


class CodeExecTool(BaseTool):
    """Python 代码执行工具"""

    @property
    def name(self) -> str:
        return "code_exec"

    @property
    def description(self) -> str:
        return "执行 Python 代码并返回输出"

    @property
    def parameters_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "code": {"type": "string", "description": "要执行的 Python 代码"},
            },
            "required": ["code"],
        }

    async def execute(self, code: str = "", **kwargs) -> ToolResult:
        """安全执行 Python 代码"""
        # TODO: 在子进程中执行，限制资源
        # TODO: 捕获 stdout/stderr
        # TODO: 设置执行超时
        try:
            proc = await asyncio.create_subprocess_exec(
                "python", "-c", code,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=10)
            output = stdout.decode(errors="replace")
            if proc.returncode != 0:
                return ToolResult(success=False, error=stderr.decode(errors="replace"))
            return ToolResult(success=True, output=output)
        except asyncio.TimeoutError:
            return ToolResult(success=False, error="代码执行超时 (10s)")
        except Exception as e:
            return ToolResult(success=False, error=str(e))
