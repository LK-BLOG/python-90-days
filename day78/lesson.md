# Day 78: 工具开发实战

## 1. 文件操作工具

### 1.1 安全的文件读写

`python
import os
import json
from pathlib import Path
from typing import Optional
from dataclasses import dataclass


@dataclass
class ToolResult:
    success: bool
    data: any = None
    error: str = ""


class FileReadTool:
    \"\"\"安全读取文件\"\"\"
    name = "file_read"
    description = "读取指定路径的文件内容"
    
    # 安全：限制可访问的目录
    ALLOWED_ROOTS = [Path.home() / "workspace", Path("./data")]
    
    def __init__(self, allowed_roots: list = None):
        self.allowed_roots = allowed_roots or self.ALLOWED_ROOTS
    
    def _is_safe_path(self, filepath: Path) -> bool:
        \"\"\"检查路径是否安全\"\"\"
        try:
            resolved = filepath.resolve()
            return any(
                str(resolved).startswith(str(root.resolve()))
                for root in self.allowed_roots
            )
        except (ValueError, OSError):
            return False
    
    def execute(self, path: str, encoding: str = "utf-8") -> ToolResult:
        filepath = Path(path)
        
        # 安全检查
        if not self._is_safe_path(filepath):
            return ToolResult(False, error=f"禁止访问: {path}")
        
        if not filepath.exists():
            return ToolResult(False, error=f"文件不存在: {path}")
        
        if not filepath.is_file():
            return ToolResult(False, error=f"不是文件: {path}")
        
        # 限制文件大小（10MB）
        if filepath.stat().st_size > 10 * 1024 * 1024:
            return ToolResult(False, error="文件过大（>10MB）")
        
        try:
            content = filepath.read_text(encoding=encoding)
            return ToolResult(True, data=content)
        except Exception as e:
            return ToolResult(False, error=str(e))


class FileWriteTool:
    \"\"\"安全写入文件\"\"\"
    name = "file_write"
    description = "将内容写入文件"
    
    def __init__(self, allowed_roots: list = None, max_size: int = 5*1024*1024):
        self.allowed_roots = allowed_roots or [Path("./output")]
        self.max_size = max_size
    
    def execute(self, path: str, content: str, mode: str = "w") -> ToolResult:
        filepath = Path(path)
        
        # 安全检查
        resolved = filepath.resolve()
        if not any(str(resolved).startswith(str(r.resolve())) for r in self.allowed_roots):
            return ToolResult(False, error=f"禁止写入: {path}")
        
        if len(content) > self.max_size:
            return ToolResult(False, error="内容过大")
        
        try:
            filepath.parent.mkdir(parents=True, exist_ok=True)
            filepath.write_text(content, encoding="utf-8")
            return ToolResult(True, data=f"已写入: {filepath}")
        except Exception as e:
            return ToolResult(False, error=str(e))


class FileListTool:
    \"\"\"列出目录内容\"\"\"
    name = "file_list"
    description = "列出目录中的文件"
    
    def execute(self, path: str = ".", pattern: str = "*") -> ToolResult:
        try:
            p = Path(path)
            if not p.is_dir():
                return ToolResult(False, error=f"不是目录: {path}")
            
            files = []
            for f in p.glob(pattern):
                stat = f.stat()
                files.append({
                    "name": f.name,
                    "type": "dir" if f.is_dir() else "file",
                    "size": stat.st_size,
                })
            
            return ToolResult(True, data=files)
        except Exception as e:
            return ToolResult(False, error=str(e))
`

## 2. Shell 执行工具

`python
import subprocess
import shlex
from typing import Optional
import threading
import signal


class ShellTool:
    \"\"\"安全执行 Shell 命令\"\"\"
    name = "shell"
    description = "执行 Shell 命令"
    
    # 危险命令黑名单
    BLACKLIST = [
        "rm -rf /", "mkfs", "dd if=", "> /dev/sda",
        "chmod -R 777 /", ":(){:|:&};:",  # fork bomb
    ]
    
    def __init__(self, timeout: int = 30, max_output: int = 10000):
        self.timeout = timeout
        self.max_output = max_output
    
    def _is_safe(self, command: str) -> tuple[bool, str]:
        \"\"\"安全检查\"\"\"
        cmd_lower = command.lower().strip()
        
        for blocked in self.BLACKLIST:
            if blocked in cmd_lower:
                return False, f"危险命令被阻止: {blocked}"
        
        # 防止管道注入
        if "||" in command or "&&" in command:
            # 允许但记录
            pass
        
        return True, ""
    
    def execute(self, command: str, cwd: str = None) -> ToolResult:
        safe, reason = self._is_safe(command)
        if not safe:
            return ToolResult(False, error=reason)
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=self.timeout,
                cwd=cwd
            )
            
            stdout = result.stdout[:self.max_output]
            stderr = result.stderr[:self.max_output]
            
            return ToolResult(
                success=result.returncode == 0,
                data={
                    "stdout": stdout,
                    "stderr": stderr,
                    "returncode": result.returncode
                },
                error=stderr if result.returncode != 0 else ""
            )
            
        except subprocess.TimeoutExpired:
            return ToolResult(False, error=f"命令超时 ({self.timeout}秒)")
        except Exception as e:
            return ToolResult(False, error=str(e))
`

## 3. 代码执行沙箱

`python
import sys
import io
import traceback
from typing import Any
from contextlib import redirect_stdout, redirect_stderr


class CodeSandbox:
    \"\"\"安全执行 Python 代码\"\"\"
    
    def __init__(self, timeout: int = 10, max_output: int = 10000):
        self.timeout = timeout
        self.max_output = max_output
        
        # 可用的内置函数白名单
        self.safe_builtins = {
            "print": print, "len": len, "range": range,
            "int": int, "float": float, "str": str,
            "list": list, "dict": dict, "set": set,
            "tuple": tuple, "bool": bool, "type": type,
            "min": min, "max": max, "sum": sum,
            "sorted": sorted, "enumerate": enumerate,
            "zip": zip, "map": map, "filter": filter,
            "isinstance": isinstance, "hasattr": hasattr,
            "getattr": getattr, "abs": abs, "round": round,
        }
    
    def execute(self, code: str) -> ToolResult:
        \"\"\"执行代码并捕获输出\"\"\"
        # 禁止危险操作
        dangerous = ["import os", "import subprocess", "import sys", 
                     "__import__", "eval(", "exec(", "open("]
        for d in dangerous:
            if d in code:
                return ToolResult(
                    False, 
                    error=f"禁止使用: {d}"
                )
        
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()
        
        local_vars = {"__builtins__": self.safe_builtins}
        
        try:
            with redirect_stdout(stdout_capture), redirect_stderr(stderr_capture):
                exec(code, {}, local_vars)
            
            stdout = stdout_capture.getvalue()[:self.max_output]
            stderr = stderr_capture.getvalue()[:self.max_output]
            
            # 获取最后表达式的值
            result_value = local_vars.get("_", None)
            
            return ToolResult(
                success=True,
                data={
                    "stdout": stdout,
                    "stderr": stderr,
                    "result": str(result_value) if result_value else None
                }
            )
            
        except Exception as e:
            tb = traceback.format_exc()
            return ToolResult(
                False,
                error=f"{type(e).__name__}: {e}\n{tb}"
            )
`

## 4. 网络搜索工具

`python
import urllib.request
import urllib.parse
import json
from typing import List, Dict


class WebSearchTool:
    \"\"\"网络搜索工具\"\"\"
    name = "web_search"
    description = "在互联网上搜索信息"
    
    def __init__(self, max_results: int = 5):
        self.max_results = max_results
    
    def execute(self, query: str) -> ToolResult:
        \"\"\"执行搜索（模拟实现）\"\"\"
        # 注意：实际项目中接入真实的搜索 API
        # 这里用模拟数据演示
        
        try:
            # 模拟搜索结果
            results = [
                {
                    "title": f"关于 '{query}' 的搜索结果 {i+1}",
                    "url": f"https://example.com/result{i+1}",
                    "snippet": f"这是关于 '{query}' 的第 {i+1} 条结果摘要..."
                }
                for i in range(min(self.max_results, 5))
            ]
            
            return ToolResult(True, data=results)
            
        except Exception as e:
            return ToolResult(False, error=str(e))


# 真实搜索实现示例（需要 API key）
class RealWebSearchTool:
    \"\"\"接入真实搜索 API\"\"\"
    name = "web_search"
    
    def __init__(self, api_key: str, search_engine: str = "bing"):
        self.api_key = api_key
        self.search_engine = search_engine
    
    def execute(self, query: str) -> ToolResult:
        try:
            # Bing Search API 示例
            url = "https://api.bing.microsoft.com/v7.0/search"
            params = urllib.parse.urlencode({
                "q": query,
                "count": 5
            })
            
            req = urllib.request.Request(
                f"{url}?{params}",
                headers={"Ocp-Apim-Subscription-Key": self.api_key}
            )
            
            with urllib.request.urlopen(req) as resp:
                data = json.loads(resp.read())
            
            results = [
                {
                    "title": r.get("name", ""),
                    "url": r.get("url", ""),
                    "snippet": r.get("snippet", "")
                }
                for r in data.get("webPages", {}).get("value", [])
            ]
            
            return ToolResult(True, data=results)
            
        except Exception as e:
            return ToolResult(False, error=str(e))
`

## 5. 数据库查询工具

`python
import sqlite3
from typing import List, Dict, Optional
from pathlib import Path


class DatabaseTool:
    \"\"\"数据库查询工具\"\"\"
    name = "database_query"
    description = "执行 SQL 查询"
    
    # 危险 SQL 关键字
    FORBIDDEN_KEYWORDS = ["DROP", "DELETE", "TRUNCATE", "ALTER", "INSERT", "UPDATE"]
    
    def __init__(self, db_path: str = ":memory:"):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        \"\"\"初始化数据库\"\"\"
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        
        # 创建示例表
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT,
                age INTEGER
            )
        ''')
        
        # 插入示例数据
        cursor.execute('SELECT COUNT(*) FROM users')
        if cursor.fetchone()[0] == 0:
            users = [
                (1, "Alice", "alice@example.com", 30),
                (2, "Bob", "bob@example.com", 25),
                (3, "Charlie", "charlie@example.com", 35),
            ]
            cursor.executemany('INSERT INTO users VALUES (?, ?, ?, ?)', users)
            self.conn.commit()
    
    def _is_read_only(self, query: str) -> tuple[bool, str]:
        \"\"\"检查是否为只读查询\"\"\"
        query_upper = query.upper().strip()
        
        for keyword in self.FORBIDDEN_KEYWORDS:
            if keyword in query_upper:
                return False, f"禁止执行: {keyword}"
        
        return True, ""
    
    def execute(self, query: str, params: tuple = ()) -> ToolResult:
        safe, reason = self._is_read_only(query)
        if not safe:
            return ToolResult(False, error=reason)
        
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            
            if query.upper().strip().startswith("SELECT"):
                rows = cursor.fetchall()
                result = [dict(row) for row in rows]
            else:
                self.conn.commit()
                result = f"影响 {cursor.rowcount} 行"
            
            return ToolResult(True, data=result)
            
        except Exception as e:
            return ToolResult(False, error=str(e))
    
    def close(self):
        self.conn.close()
`

## 6. 工具组合

`python
class ToolChain:
    \"\"\"工具链 - 串联多个工具\"\"\"
    
    def __init__(self, tools: dict):
        self.tools = tools
    
    def chain(self, steps: list) -> ToolResult:
        \"\"\"按步骤执行工具链\"\"\"
        context = {}
        
        for i, step in enumerate(steps):
            tool_name = step["tool"]
            params = step.get("params", {})
            
            # 用前一步结果替换参数引用
            for key, value in params.items():
                if isinstance(value, str) and value.startswith("$"):
                    ref = value[1:]
                    params[key] = context.get(ref, value)
            
            tool = self.tools.get(tool_name)
            if not tool:
                return ToolResult(False, error=f"工具不存在: {tool_name}")
            
            result = tool.run(**params)
            if not result.success:
                return ToolResult(False, error=f"步骤 {i+1} 失败: {result.error}")
            
            context[f"step{i+1}"] = result.data
            context["last"] = result.data
        
        return ToolResult(True, data=context)
`

## 7. 常见错误

1. **路径穿越**：用户传入 ../../etc/passwd → 始终验证路径
2. **命令注入**：用户传入 ; rm -rf / → 永远不要直接拼接用户输入
3. **资源泄露**：文件/数据库连接没关闭 → 使用 context manager
4. **超时失控**：长命令阻塞 → 设置超时限制
5. **输出爆炸**：打印海量数据 → 限制输出大小

## 8. 动手练习

### 练习 1：实现文件读取工具
添加路径安全检查和文件大小限制。

### 练习 2：实现代码沙箱
支持安全执行 Python 代码，禁止危险导入。

### 练习 3：实现工具链
串联 search → analyze → summarize 三个工具。
