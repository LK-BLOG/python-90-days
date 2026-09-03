"""Day 30 - Shell 执行工具"""
from __future__ import annotations

import asyncio
from ai_assistant.tools.base import BaseTool, ToolResult


class ShellTool(BaseTool):
    """Shell 命令执行工具"""

    @property
    def name(self) -> str:
        return "shell"

    @property
    def description(self) -> str:
        return "执行 shell 命令并返回输出"

    @property
    def parameters_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "command": {"type": "string", "description": "要执行的命令"},
                "timeout": {"type": "integer", "description": "超时秒数", "default": 30},
            },
            "required": ["command"],
        }

    async def execute(self, command: str = "", timeout: int = 30, **kwargs) -> ToolResult:
        """执行 shell 命令"""
        # TODO: 使用 asyncio.create_subprocess_shell 执行
        # TODO: 捕获 stdout 和 stderr
        # TODO: 超时处理
        try:
            proc = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=timeout)
            output = stdout.decode(errors="replace")
            if proc.returncode != 0:
                error = stderr.decode(errors="replace")
                return ToolResult(success=False, output=output, error=error)
            return ToolResult(success=True, output=output)
        except asyncio.TimeoutError:
            return ToolResult(success=False, error=f"命令超时 ({timeout}s)")
        except Exception as e:
            return ToolResult(success=False, error=str(e))
