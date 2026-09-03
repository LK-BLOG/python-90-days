# Day 77 示例 4: MCP Server 基础
\"\"\"
简化版 MCP (Model Context Protocol) Server 实现
\"\"\"
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional
import json


@dataclass
class MCPToolDef:
    \"\"\"MCP 工具定义\"\"\"
    name: str
    description: str
    input_schema: dict = field(default_factory=dict)
    handler: Callable = None


class MCPServer:
    \"\"\"简化版 MCP Server\"\"\"
    
    def __init__(self, name: str, version: str = "1.0.0"):
        self.name = name
        self.version = version
        self.tools: Dict[str, MCPToolDef] = {}
        self.resources: Dict[str, Any] = {}
    
    def tool(self, name: str, description: str, input_schema: dict = None):
        \"\"\"工具装饰器\"\"\"
        def decorator(func):
            self.tools[name] = MCPToolDef(
                name=name,
                description=description,
                input_schema=input_schema or {},
                handler=func
            )
            return func
        return decorator
    
    def resource(self, uri: str, name: str = ""):
        \"\"\"资源装饰器\"\"\"
        def decorator(func):
            self.resources[uri] = {
                "uri": uri,
                "name": name or uri,
                "handler": func
            }
            return func
        return decorator
    
    # MCP 协议方法
    def handle_list_tools(self) -> List[dict]:
        \"\"\"MCP: tools/list\"\"\"
        return [
            {
                "name": t.name,
                "description": t.description,
                "inputSchema": t.input_schema
            }
            for t in self.tools.values()
        ]
    
    def handle_call_tool(self, name: str, arguments: dict = None) -> Any:
        \"\"\"MCP: tools/call\"\"\"
        if name not in self.tools:
            return {
                "content": [{"type": "text", "text": f"错误: 未知工具 '{name}'"}],
                "isError": True
            }
        
        try:
            result = self.tools[name].handler(**(arguments or {}))
            return {
                "content": [{"type": "text", "text": str(result)}],
                "isError": False
            }
        except Exception as e:
            return {
                "content": [{"type": "text", "text": f"执行错误: {e}"}],
                "isError": True
            }
    
    def handle_list_resources(self) -> List[dict]:
        \"\"\"MCP: resources/list\"\"\"
        return [
            {"uri": r["uri"], "name": r["name"]}
            for r in self.resources.values()
        ]
    
    def to_manifest(self) -> dict:
        \"\"\"生成服务清单\"\"\"
        return {
            "name": self.name,
            "version": self.version,
            "tools": self.handle_list_tools(),
            "resources": self.handle_list_resources()
        }


# 创建 MCP Server
server = MCPServer("dev-tools", "1.0.0")

@server.tool(
    name="read_file",
    description="读取文件内容",
    input_schema={
        "type": "object",
        "properties": {
            "path": {"type": "string", "description": "文件路径"}
        },
        "required": ["path"]
    }
)
def read_file(path: str) -> str:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return f"文件不存在: {path}"

@server.tool(
    name="list_directory",
    description="列出目录内容",
    input_schema={
        "type": "object",
        "properties": {
            "path": {"type": "string", "description": "目录路径"}
        }
    }
)
def list_directory(path: str = ".") -> list:
    return os.listdir(path) if os.path.isdir(path) else []

@server.tool(
    name="run_python",
    description="执行 Python 代码",
    input_schema={
        "type": "object",
        "properties": {
            "code": {"type": "string", "description": "Python 代码"}
        },
        "required": ["code"]
    }
)
def run_python(code: str) -> str:
    try:
        result = {}
        exec(code, {"__builtins__": {}}, result)
        return str(result)
    except Exception as e:
        return f"执行错误: {e}"

import os

# 演示
if __name__ == "__main__":
    print("=== MCP Server 演示 ===\n")
    
    # 查看服务清单
    manifest = server.to_manifest()
    print(f"服务: {manifest['name']} v{manifest['version']}")
    print(f"工具数量: {len(manifest['tools'])}")
    
    for t in manifest["tools"]:
        print(f"\n  📦 {t['name']}")
        print(f"     {t['description']}")
        print(f"     参数: {json.dumps(t['inputSchema'], ensure_ascii=False, indent=2)}")
    
    # 模拟 MCP 客户端调用
    print("\n=== 模拟 MCP 调用 ===\n")
    
    response = server.handle_call_tool("run_python", {"code": "1 + 2"})
    print(f"调用 run_python: {json.dumps(response, ensure_ascii=False)}")
    
    response = server.handle_call_tool("unknown_tool", {})
    print(f"调用未知工具: {json.dumps(response, ensure_ascii=False)}")
