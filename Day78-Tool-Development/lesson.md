# Day 78 课程：工具开发实战

## 1. 文件操作工具

`python
import os
import aiofiles
from pathlib import Path
from typing import Optional


class FileOperationTool(BaseTool):
    '''文件操作工具'''
    
    def __init__(self, allowed_dirs: list[str] = None):
        super().__init__(
            name="file_operations",
            description="执行文件操作：读取、写入、列出目录",
            parameters=[
                ToolParameter("operation", "string", "操作类型：read/write/list"),
                ToolParameter("path", "string", "文件路径"),
                ToolParameter("content", "string", "写入内容（write操作时必填）", required=False)
            ]
        )
        self.allowed_dirs = allowed_dirs or [os.getcwd()]
    
    def _validate_path(self, path: str) -> bool:
        '''验证路径安全性'''
        abs_path = os.path.abspath(path)
        
        # 检查是否在允许的目录中
        for allowed_dir in self.allowed_dirs:
            if abs_path.startswith(os.path.abspath(allowed_dir)):
                return True
        
        return False
    
    async def execute(self, **kwargs) -> ToolResult:
        operation = kwargs.get("operation")
        path = kwargs.get("path")
        content = kwargs.get("content")
        
        # 验证路径
        if not self._validate_path(path):
            return ToolResult(
                success=False,
                output=None,
                error=f"路径不在允许的目录中: {path}"
            )
        
        try:
            if operation == "read":
                async with aiofiles.open(path, 'r', encoding='utf-8') as f:
                    content = await f.read()
                return ToolResult(success=True, output=content)
            
            elif operation == "write":
                if content is None:
                    return ToolResult(
                        success=False,
                        output=None,
                        error="写入操作需要content参数"
                    )
                async with aiofiles.open(path, 'w', encoding='utf-8') as f:
                    await f.write(content)
                return ToolResult(success=True, output=f"已写入文件: {path}")
            
            elif operation == "list":
                items = []
                for item in Path(path).iterdir():
                    items.append({
                        "name": item.name,
                        "type": "directory" if item.is_dir() else "file",
                        "size": item.stat().st_size if item.is_file() else 0
                    })
                return ToolResult(success=True, output=items)
            
            else:
                return ToolResult(
                    success=False,
                    output=None,
                    error=f"未知操作: {operation}"
                )
        
        except Exception as e:
            return ToolResult(success=False, output=None, error=str(e))
`

## 2. Shell执行工具

`python
import asyncio
import subprocess
import shlex
from typing import Optional


class ShellTool(BaseTool):
    '''Shell执行工具（带沙箱）'''
    
    def __init__(
        self, 
        timeout: int = 30,
        allowed_commands: list[str] = None
    ):
        super().__init__(
            name="shell",
            description="执行Shell命令。注意：危险命令会被阻止。",
            parameters=[
                ToolParameter("command", "string", "要执行的Shell命令")
            ]
        )
        self.timeout = timeout
        self.allowed_commands = allowed_commands or [
            "ls", "cat", "echo", "pwd", "whoami",
            "date", "grep", "find", "head", "tail"
        ]
    
    def _is_safe_command(self, command: str) -> bool:
        '''检查命令是否安全'''
        # 危险命令黑名单
        dangerous_commands = [
            "rm", "rmdir", "del", "format",
            "sudo", "su", "chmod", "chown",
            "kill", "killall", "pkill"
        ]
        
        # 解析命令
        parts = command.split()
        if not parts:
            return False
        
        cmd = parts[0]
        
        # 检查是否在黑名单中
        for dangerous in dangerous_commands:
            if cmd.endswith(dangerous):
                return False
        
        # 检查管道和重定向
        if "|" in command or ">" in command or "<" in command:
            # 允许简单的管道
            if "|" in command:
                sub_commands = command.split("|")
                for sub_cmd in sub_commands:
                    if not self._is_safe_command(sub_cmd.strip()):
                        return False
                return True
            return False
        
        return True
    
    async def execute(self, **kwargs) -> ToolResult:
        command = kwargs.get("command")
        
        # 检查命令安全性
        if not self._is_safe_command(command):
            return ToolResult(
                success=False,
                output=None,
                error=f"命令被阻止: {command}"
            )
        
        try:
            # 执行命令
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            # 等待完成（带超时）
            stdout, stderr = await asyncio.wait_for(
                process.communicate(),
                timeout=self.timeout
            )
            
            if process.returncode == 0:
                return ToolResult(
                    success=True,
                    output=stdout.decode('utf-8')
                )
            else:
                return ToolResult(
                    success=False,
                    output=stdout.decode('utf-8'),
                    error=stderr.decode('utf-8')
                )
        
        except asyncio.TimeoutError:
            process.kill()
            return ToolResult(
                success=False,
                output=None,
                error=f"命令执行超时（{self.timeout}秒）"
            )
        except Exception as e:
            return ToolResult(
                success=False,
                output=None,
                error=str(e)
            )
`

## 3. 代码执行工具（安全沙箱）

`python
import sys
import io
import traceback
from contextlib import contextmanager
from typing import Any


@contextmanager
def restricted_globals():
    '''受限的全局变量'''
    safe_builtins = {
        'abs': abs, 'bool': bool, 'dict': dict,
        'enumerate': enumerate, 'filter': filter,
        'float': float, 'frozenset': frozenset,
        'getattr': getattr, 'hasattr': hasattr,
        'hash': hash, 'hex': hex, 'id': id,
        'int': int, 'isinstance': isinstance,
        'issubclass': issubclass, 'iter': iter,
        'len': len, 'list': list, 'map': map,
        'max': max, 'min': min, 'next': next,
        'oct': oct, 'open': open, 'ord': ord,
        'pow': pow, 'print': print, 'property': property,
        'range': range, 'repr': repr, 'reversed': reversed,
        'round': round, 'set': set, 'setattr': setattr,
        'slice': slice, 'sorted': sorted, 'str': str,
        'sum': sum, 'super': super, 'tuple': tuple,
        'type': type, 'zip': zip,
        # 禁用危险函数
        # 'exec': exec, 'eval': eval, '__import__': __import__
    }
    
    yield {"__builtins__": safe_builtins}


class PythonExecutorTool(BaseTool):
    '''Python代码执行工具（沙箱）'''
    
    def __init__(self, timeout: int = 10):
        super().__init__(
            name="python_executor",
            description="安全执行Python代码。只允许安全的操作。",
            parameters=[
                ToolParameter("code", "string", "要执行的Python代码")
            ]
        )
        self.timeout = timeout
    
    async def execute(self, **kwargs) -> ToolResult:
        code = kwargs.get("code")
        
        # 检查代码安全性
        if not self._is_safe_code(code):
            return ToolResult(
                success=False,
                output=None,
                error="代码包含不安全的操作"
            )
        
        try:
            # 捕获输出
            old_stdout = sys.stdout
            old_stderr = sys.stderr
            redirected_output = io.StringIO()
            redirected_error = io.StringIO()
            
            sys.stdout = redirected_output
            sys.stderr = redirected_error
            
            # 在受限环境中执行
            with restricted_globals() as safe_globals:
                exec(code, safe_globals)
            
            # 恢复输出
            sys.stdout = old_stdout
            sys.stderr = old_stderr
            
            output = redirected_output.getvalue()
            error = redirected_error.getvalue()
            
            if error:
                return ToolResult(
                    success=False,
                    output=output,
                    error=error
                )
            
            return ToolResult(success=True, output=output or "代码执行完成")
        
        except Exception as e:
            sys.stdout = old_stdout
            sys.stderr = old_stderr
            return ToolResult(
                success=False,
                output=None,
                error=f"执行错误: {traceback.format_exc()}"
            )
    
    def _is_safe_code(self, code: str) -> bool:
        '''检查代码安全性'''
        dangerous_patterns = [
            '__import__', 'import os', 'import sys',
            'import subprocess', 'import shutil',
            'open(', 'exec(', 'eval(',
            'os.', 'sys.', 'subprocess.',
            'rm ', 'del ', 'rmdir'
        ]
        
        code_lower = code.lower()
        for pattern in dangerous_patterns:
            if pattern.lower() in code_lower:
                return False
        
        return True
`

## 4. 网络搜索工具

`python
import aiohttp
from typing import Optional
import json


class WebSearchTool(BaseTool):
    '''网络搜索工具'''
    
    def __init__(self, api_key: str = None):
        super().__init__(
            name="web_search",
            description="在互联网上搜索信息",
            parameters=[
                ToolParameter("query", "string", "搜索关键词"),
                ToolParameter("num_results", "number", "结果数量", required=False, default=5)
            ]
        )
        self.api_key = api_key
    
    async def execute(self, **kwargs) -> ToolResult:
        query = kwargs.get("query")
        num_results = kwargs.get("num_results", 5)
        
        try:
            # 模拟搜索结果（实际使用时替换为真实API）
            results = self._mock_search(query, num_results)
            
            return ToolResult(
                success=True,
                output=results
            )
        
        except Exception as e:
            return ToolResult(
                success=False,
                output=None,
                error=f"搜索失败: {str(e)}"
            )
    
    def _mock_search(self, query: str, num_results: int) -> list[dict]:
        '''模拟搜索结果'''
        results = []
        for i in range(num_results):
            results.append({
                "title": f"搜索结果 {i+1}: {query}",
                "snippet": f"这是关于{query}的第{i+1}个结果的摘要...",
                "url": f"https://example.com/result{i+1}"
            })
        return results


class HTTPRequestTool(BaseTool):
    '''HTTP请求工具'''
    
    def __init__(self, timeout: int = 30):
        super().__init__(
            name="http_request",
            description="发送HTTP请求",
            parameters=[
                ToolParameter("url", "string", "请求URL"),
                ToolParameter("method", "string", "请求方法", required=False, default="GET"),
                ToolParameter("headers", "string", "请求头（JSON格式）", required=False),
                ToolParameter("data", "string", "请求数据", required=False)
            ]
        )
        self.timeout = timeout
    
    async def execute(self, **kwargs) -> ToolResult:
        url = kwargs.get("url")
        method = kwargs.get("method", "GET")
        headers = kwargs.get("headers")
        data = kwargs.get("data")
        
        try:
            async with aiohttp.ClientSession() as session:
                kwargs_request = {
                    "timeout": aiohttp.ClientTimeout(total=self.timeout)
                }
                
                if headers:
                    kwargs_request["headers"] = json.loads(headers)
                
                if data:
                    kwargs_request["data"] = data
                
                async with session.request(method, url, **kwargs_request) as response:
                    content = await response.text()
                    
                    return ToolResult(
                        success=True,
                        output={
                            "status": response.status,
                            "headers": dict(response.headers),
                            "body": content[:1000]  # 限制响应大小
                        }
                    )
        
        except Exception as e:
            return ToolResult(
                success=False,
                output=None,
                error=f"请求失败: {str(e)}"
            )
`

## 5. 数据库查询工具

`python
import sqlite3
from typing import Optional
import json


class SQLiteTool(BaseTool):
    '''SQLite数据库工具'''
    
    def __init__(self, db_path: str = ":memory:"):
        super().__init__(
            name="sqlite",
            description="执行SQLite数据库查询",
            parameters=[
                ToolParameter("query", "string", "SQL查询语句"),
                ToolParameter("params", "string", "查询参数（JSON数组）", required=False)
            ]
        )
        self.db_path = db_path
        self.connection = None
    
    def _get_connection(self):
        '''获取数据库连接'''
        if self.connection is None:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row
        return self.connection
    
    async def execute(self, **kwargs) -> ToolResult:
        query = kwargs.get("query")
        params = kwargs.get("params")
        
        # 安全检查：只允许SELECT查询
        query_upper = query.upper().strip()
        if not query_upper.startswith("SELECT"):
            return ToolResult(
                success=False,
                output=None,
                error="只允许SELECT查询"
            )
        
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # 解析参数
            if params:
                params = json.loads(params)
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            # 获取结果
            rows = cursor.fetchall()
            results = [dict(row) for row in rows]
            
            return ToolResult(
                success=True,
                output=results
            )
        
        except Exception as e:
            return ToolResult(
                success=False,
                output=None,
                error=f"查询失败: {str(e)}"
            )
    
    def close(self):
        '''关闭连接'''
        if self.connection:
            self.connection.close()
            self.connection = None
`

## 6. 自定义工具开发模式

### 工具开发清单

1. **定义工具元数据**
   - 名称
   - 描述
   - 参数定义
   - 使用示例

2. **实现执行逻辑**
   - 输入验证
   - 业务逻辑
   - 输出格式化
   - 错误处理

3. **添加安全机制**
   - 权限检查
   - 沙箱执行
   - 超时控制
   - 日志记录

4. **编写测试**
   - 单元测试
   - 集成测试
   - 边界测试

5. **文档和示例**
   - 使用说明
   - 示例代码
   - 常见问题

## 7. 本日总结

- 文件操作工具需要路径验证
- Shell工具需要命令白名单和黑名单
- 代码执行工具需要沙箱环境
- 网络工具需要超时控制
- 数据库工具需要查询限制

明天我们将学习Planning和目标分解。
