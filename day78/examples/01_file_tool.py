# Day 78 示例 1: 文件操作工具
import os
from pathlib import Path
from dataclasses import dataclass
from typing import Optional

@dataclass
class ToolResult:
    success: bool
    data = None
    error: str = ""

class SafeFileReadTool:
    name = "file_read"
    description = "安全读取文件内容"
    
    def __init__(self, allowed_dirs: list = None):
        self.allowed_dirs = [Path(d).resolve() for d in (allowed_dirs or ["."])]
    
    def _check_path(self, path: str) -> tuple:
        p = Path(path).resolve()
        if not any(str(p).startswith(str(d)) for d in self.allowed_dirs):
            return False, f"禁止访问: {path}"
        if p.stat().st_size > 5 * 1024 * 1024:
            return False, "文件过大(>5MB)"
        return True, ""
    
    def execute(self, path: str) -> ToolResult:
        p = Path(path)
        if not p.exists():
            return ToolResult(False, error=f"文件不存在: {path}")
        ok, reason = self._check_path(path)
        if not ok:
            return ToolResult(False, error=reason)
        return ToolResult(True, data=p.read_text(encoding="utf-8"))

class SafeFileWriteTool:
    name = "file_write"
    def __init__(self, allowed_dirs: list = None):
        self.allowed_dirs = [Path(d).resolve() for d in (allowed_dirs or ["."])]
    
    def execute(self, path: str, content: str) -> ToolResult:
        p = Path(path).resolve()
        if not any(str(p).startswith(str(d)) for d in self.allowed_dirs):
            return ToolResult(False, error=f"禁止写入: {path}")
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
        return ToolResult(True, data=f"已写入: {path}")

if __name__ == "__main__":
    reader = SafeFileReadTool(["."])
    writer = SafeFileWriteTool(["."])
    print(writer.execute("test_output.txt", "Hello Agent!"))
    print(reader.execute("test_output.txt"))
