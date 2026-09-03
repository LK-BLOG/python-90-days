"""Day 30 示例：工具注册器 + 具体工具参考实现"""

from __future__ import annotations
import ast
import os
import subprocess
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class ToolResult:
    """工具执行结果"""
    success: bool
    content: str
    error: str | None = None
    
    def __str__(self) -> str:
        return self.content if self.success else f"错误: {self.error}"


class BaseTool(ABC):
    """工具抽象基类"""
    
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
    """工具注册器"""
    
    def __init__(self):
        self._tools: dict[str, BaseTool] = {}
    
    def register(self, tool: BaseTool) -> BaseTool:
        """注册工具实例"""
        self._tools[tool.name] = tool
        return tool
    
    def register_class(self, cls: type[BaseTool]) -> type[BaseTool]:
        """注册工具类"""
        instance = cls()
        self._tools[instance.name] = instance
        return cls
    
    async def execute(self, name: str, **kwargs) -> ToolResult:
        if name not in self._tools:
            return ToolResult(False, "", f"未知工具: {name}. 可用: {self.list_tools()}")
        try:
            return await self._tools[name].execute(**kwargs)
        except Exception as e:
            return ToolResult(False, "", f"{type(e).__name__}: {e}")
    
    def get_definitions(self) -> list[dict]:
        return [tool.to_openai_format() for tool in self._tools.values()]
    
    def list_tools(self) -> list[str]:
        return list(self._tools.keys())


# ══════════════════════════════════════
# 具体工具实现
# ══════════════════════════════════════

class FileReadTool(BaseTool):
    name = "file_read"
    description = "读取指定路径的文件内容"
    parameters = {
        "type": "object",
        "properties": {
            "path": {"type": "string", "description": "文件路径"},
            "encoding": {"type": "string", "description": "编码，默认utf-8", "default": "utf-8"},
        },
        "required": ["path"],
    }
    
    async def execute(self, path: str, encoding: str = "utf-8") -> ToolResult:
        try:
            p = Path(path).resolve()
            if not p.exists():
                return ToolResult(False, "", f"文件不存在: {path}")
            if not p.is_file():
                return ToolResult(False, "", f"不是文件: {path}")
            
            content = p.read_text(encoding=encoding)
            if len(content) > 10000:
                content = content[:10000] + f"\n... (截断，共{len(content)}字符)"
            
            return ToolResult(True, content)
        except Exception as e:
            return ToolResult(False, "", str(e))


class FileWriteTool(BaseTool):
    name = "file_write"
    description = "将内容写入指定路径的文件"
    parameters = {
        "type": "object",
        "properties": {
            "path": {"type": "string", "description": "文件路径"},
            "content": {"type": "string", "description": "要写入的内容"},
        },
        "required": ["path", "content"],
    }
    
    async def execute(self, path: str, content: str) -> ToolResult:
        try:
            p = Path(path)
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(content, encoding="utf-8")
            return ToolResult(True, f"已写入 {len(content)} 字节到 {path}")
        except Exception as e:
            return ToolResult(False, "", str(e))


class ShellExecTool(BaseTool):
    name = "shell_exec"
    description = "执行Shell命令并返回输出"
    parameters = {
        "type": "object",
        "properties": {
            "command": {"type": "string", "description": "要执行的Shell命令"},
            "timeout": {"type": "integer", "description": "超时秒数，默认30", "default": 30},
        },
        "required": ["command"],
    }
    
    async def execute(self, command: str, timeout: int = 30) -> ToolResult:
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=os.getcwd(),
            )
            output = result.stdout
            if result.stderr:
                output += f"\n[stderr] {result.stderr}"
            if not output.strip():
                output = "(无输出)"
            return ToolResult(True, output[:5000])
        except subprocess.TimeoutExpired:
            return ToolResult(False, "", f"命令超时 ({timeout}秒)")
        except Exception as e:
            return ToolResult(False, "", str(e))


class CodeExecTool(BaseTool):
    name = "code_exec"
    description = "执行Python代码并返回输出"
    parameters = {
        "type": "object",
        "properties": {
            "code": {"type": "string", "description": "要执行的Python代码"},
        },
        "required": ["code"],
    }
    
    async def execute(self, code: str) -> ToolResult:
        import io
        from contextlib import redirect_stdout, redirect_stderr
        
        stdout_buf = io.StringIO()
        stderr_buf = io.StringIO()
        
        try:
            with redirect_stdout(stdout_buf), redirect_stderr(stderr_buf):
                exec(code, {"__builtins__": __builtins__})
            
            output = stdout_buf.getvalue()
            errors = stderr_buf.getvalue()
            
            if errors:
                output += f"\n[stderr] {errors}"
            if not output.strip():
                output = "(无输出)"
            
            return ToolResult(True, output[:5000])
        except Exception as e:
            return ToolResult(False, "", f"{type(e).__name__}: {e}")


if __name__ == "__main__":
    import asyncio
    
    registry = ToolRegistry()
    registry.register(FileReadTool())
    registry.register(FileWriteTool())
    registry.register(ShellExecTool())
    registry.register(CodeExecTool())
    
    print(f"已注册工具: {registry.list_tools()}")
    
    result = asyncio.run(registry.execute("code_exec", code="print(2**100)"))
    print(f"计算结果: {result}")
