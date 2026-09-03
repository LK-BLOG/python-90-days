# Day 77 课程：Agent 工具系统

## 1. 工具抽象设计

### BaseTool接口

`python
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Callable


@dataclass
class ToolParameter:
    '''工具参数描述'''
    name: str
    type: str  # "string", "number", "boolean", "array", "object"
    description: str
    required: bool = True
    default: Any = None


@dataclass
class ToolResult:
    '''工具执行结果'''
    success: bool
    output: Any
    error: str | None = None
    metadata: dict | None = None


class BaseTool(ABC):
    '''工具抽象基类'''
    
    def __init__(
        self, 
        name: str, 
        description: str,
        parameters: list[ToolParameter] = None
    ):
        self.name = name
        self.description = description
        self.parameters = parameters or []
    
    @abstractmethod
    async def execute(self, **kwargs) -> ToolResult:
        '''执行工具'''
        pass
    
    def to_schema(self) -> dict:
        '''转换为OpenAI函数调用格式'''
        properties = {}
        required = []
        
        for param in self.parameters:
            properties[param.name] = {
                "type": param.type,
                "description": param.description
            }
            if param.required:
                required.append(param.name)
        
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "type": "object",
                "properties": properties,
                "required": required
            }
        }
    
    def to_llm_description(self) -> str:
        '''生成给LLM看的工具描述'''
        params_desc = "\n".join([
            f"  - {p.name} ({p.type}){'[必填]' if p.required else '[可选]'}: {p.description}"
            for p in self.parameters
        ])
        
        return f\"\"\"
工具名称: {self.name}
描述: {self.description}
参数:
{params_desc}
\"\"\"
`

## 2. 工具注册与发现

### ToolRegistry

`python
from typing import Type
import importlib
import inspect


class ToolRegistry:
    '''工具注册表'''
    
    def __init__(self):
        self._tools: dict[str, BaseTool] = {}
        self._categories: dict[str, list[str]] = {}
    
    def register(self, tool: BaseTool, category: str = "general"):
        '''注册工具'''
        if tool.name in self._tools:
            raise ValueError(f"工具 {tool.name} 已存在")
        
        self._tools[tool.name] = tool
        
        if category not in self._categories:
            self._categories[category] = []
        self._categories[category].append(tool.name)
    
    def get(self, name: str) -> BaseTool | None:
        '''获取工具'''
        return self._tools.get(name)
    
    def list_tools(self) -> list[dict]:
        '''列出所有工具'''
        return [
            {
                "name": tool.name,
                "description": tool.description,
                "category": self._get_category(tool.name)
            }
            for tool in self._tools.values()
        ]
    
    def search(self, query: str) -> list[BaseTool]:
        '''根据描述搜索工具'''
        results = []
        query_lower = query.lower()
        
        for tool in self._tools.values():
            if query_lower in tool.description.lower():
                results.append(tool)
        
        return results
    
    def _get_category(self, tool_name: str) -> str:
        '''获取工具分类'''
        for category, tools in self._categories.items():
            if tool_name in tools:
                return category
        return "general"
    
    def auto_discover(self, package_path: str):
        '''自动发现并注册工具'''
        module = importlib.import_module(package_path)
        
        for name, obj in inspect.getmembers(module):
            if (
                inspect.isclass(obj) 
                and issubclass(obj, BaseTool) 
                and obj is not BaseTool
            ):
                tool_instance = obj()
                self.register(tool_instance)
`

## 3. 工具描述的重要性

工具描述是给LLM看的"说明书"，直接影响LLM能否正确使用工具。

### 好的工具描述 vs 坏的工具描述

`python
# 坏的描述
class BadSearchTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="search",
            description="搜索"  # 太简单，LLM不知道怎么用
        )

# 好的描述
class GoodSearchTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="web_search",
            description="在互联网上搜索信息。输入搜索关键词，返回相关网页的摘要和链接。适合查找实时信息、新闻、技术文档等。",
            parameters=[
                ToolParameter(
                    name="query",
                    type="string",
                    description="搜索关键词，建议使用具体、明确的词语",
                    required=True
                ),
                ToolParameter(
                    name="num_results",
                    type="number",
                    description="返回结果数量，默认5条",
                    required=False,
                    default=5
                )
            ]
        )
`

## 4. 工具执行沙箱

为了安全执行工具，我们需要沙箱机制：

`python
import asyncio
import signal
from typing import Callable


class ToolSandbox:
    '''工具执行沙箱'''
    
    def __init__(self, timeout: int = 30, max_memory: int = 1024 * 1024 * 100):
        self.timeout = timeout
        self.max_memory = max_memory
    
    async def execute(
        self, 
        tool: BaseTool, 
        **kwargs
    ) -> ToolResult:
        '''在沙箱中执行工具'''
        try:
            # 设置超时
            result = await asyncio.wait_for(
                tool.execute(**kwargs),
                timeout=self.timeout
            )
            return result
        except asyncio.TimeoutError:
            return ToolResult(
                success=False,
                output=None,
                error=f"工具执行超时（{self.timeout}秒）"
            )
        except Exception as e:
            return ToolResult(
                success=False,
                output=None,
                error=f"工具执行错误: {str(e)}"
            )
`

## 5. MCP（Model Context Protocol）基础

MCP是Anthropic推出的工具协议标准：

`python
from typing import Any
import json


class MCPServer:
    '''MCP服务器基础实现'''
    
    def __init__(self, name: str):
        self.name = name
        self.tools: dict[str, BaseTool] = {}
    
    def add_tool(self, tool: BaseTool):
        '''添加工具'''
        self.tools[tool.name] = tool
    
    def handle_request(self, request: dict) -> dict:
        '''处理MCP请求'''
        method = request.get("method")
        
        if method == "tools/list":
            return self._list_tools()
        elif method == "tools/call":
            return self._call_tool(request.get("params", {}))
        else:
            return {
                "error": {
                    "code": -32601,
                    "message": f"Unknown method: {method}"
                }
            }
    
    def _list_tools(self) -> dict:
        '''列出所有工具'''
        tools = [
            {
                "name": tool.name,
                "description": tool.description,
                "inputSchema": tool.to_schema()["parameters"]
            }
            for tool in self.tools.values()
        ]
        
        return {"tools": tools}
    
    def _call_tool(self, params: dict) -> dict:
        '''调用工具'''
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        
        tool = self.tools.get(tool_name)
        if not tool:
            return {
                "error": {
                    "code": -32602,
                    "message": f"Tool not found: {tool_name}"
                }
            }
        
        # 同步执行（实际应该用异步）
        result = asyncio.run(tool.execute(**arguments))
        
        return {
            "content": [
                {
                    "type": "text",
                    "text": str(result.output)
                }
            ]
        }
`

## 6. 本日总结

- 工具抽象设计是Agent工具系统的基础
- 工具描述质量直接影响LLM的使用效果
- ToolRegistry实现了工具的注册和发现
- 沙箱机制保证工具执行的安全性
- MCP是工具系统的标准化协议

明天我们将动手实现各种实用工具。
