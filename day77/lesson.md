# Day 77: Agent 工具系统

## 1. 工具抽象设计

### 1.1 为什么需要工具抽象？

Agent 的核心能力来自工具。好的工具抽象让 Agent 可以：
- **即插即用**：添加新工具不需要修改 Agent 代码
- **自描述**：工具自带描述，LLM 可以自动发现和使用
- **类型安全**：输入输出有明确的类型约束
- **可组合**：工具可以组合使用

### 1.2 BaseTool 抽象基类

`python
from abc import ABC, abstractmethod
from pydantic import BaseModel, Field
from typing import Any, Type


class ToolInput(BaseModel):
    \"\"\"工具输入基类\"\"\"
    pass


class ToolOutput(BaseModel):
    \"\"\"工具输出基类\"\"\"
    success: bool
    data: Any = None
    error: str = ""


class BaseTool(ABC):
    \"\"\"工具抽象基类\"\"\"
    
    # 子类必须定义
    name: str = ""
    description: str = ""
    input_type: Type[ToolInput] = ToolInput
    
    def get_schema(self) -> dict:
        \"\"\"获取工具的 JSON Schema（给 LLM 看的）\"\"\"
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.input_type.schema() if hasattr(self.input_type, 'schema') else {}
        }
    
    def validate_input(self, data: dict) -> ToolInput:
        \"\"\"验证输入\"\"\"
        try:
            return self.input_type(**data)
        except Exception as e:
            raise ValueError(f"输入验证失败: {e}")
    
    def run(self, **kwargs) -> ToolOutput:
        \"\"\"执行工具（带验证和错误处理）\"\"\"
        try:
            validated = self.validate_input(kwargs)
            result = self._execute(validated)
            return ToolOutput(success=True, data=result)
        except Exception as e:
            return ToolOutput(success=False, error=str(e))
    
    @abstractmethod
    def _execute(self, input_data: ToolInput) -> Any:
        \"\"\"实际执行逻辑（子类实现）\"\"\"
        pass
`

### 1.3 具体工具实现

`python
# 计算器工具
class CalculatorInput(ToolInput):
    expression: str = Field(description="数学表达式，如 '2+3*4'")

class CalculatorTool(BaseTool):
    name = "calculator"
    description = "执行数学计算。输入一个数学表达式，返回计算结果。"
    input_type = CalculatorInput
    
    def _execute(self, input_data: CalculatorInput) -> str:
        # 安全计算（限制可用函数）
        allowed = {'abs': abs, 'round': round, 'min': min, 'max': max}
        result = eval(input_data.expression, {"__builtins__": {}}, allowed)
        return str(result)

# 搜索工具
class SearchInput(ToolInput):
    query: str = Field(description="搜索关键词")
    max_results: int = Field(default=5, description="最大返回数量")

class SearchTool(BaseTool):
    name = "web_search"
    description = "在互联网上搜索信息。输入搜索关键词，返回相关结果。"
    input_type = SearchInput
    
    def _execute(self, input_data: SearchInput) -> list:
        # 模拟搜索
        return [
            {"title": f"关于 '{input_data.query}' 的结果 {i}", "url": f"https://example.com/{i}"}
            for i in range(input_data.max_results)
        ]
`

## 2. ToolRegistry 工具注册表

### 2.1 注册表设计

`python
from typing import Dict, List
import inspect


class ToolRegistry:
    \"\"\"工具注册表 - 管理所有可用工具\"\"\"
    
    def __init__(self):
        self._tools: Dict[str, BaseTool] = {}
        self._categories: Dict[str, List[str]] = {}
    
    def register(self, tool: BaseTool, category: str = "general") -> None:
        \"\"\"注册工具\"\"\"
        if tool.name in self._tools:
            raise ValueError(f"工具 '{tool.name}' 已存在")
        
        self._tools[tool.name] = tool
        
        if category not in self._categories:
            self._categories[category] = []
        self._categories[category].append(tool.name)
        
        print(f"✅ 注册工具: {tool.name} ({category})")
    
    def unregister(self, name: str) -> None:
        \"\"\"注销工具\"\"\"
        if name in self._tools:
            del self._tools[name]
            for cat_tools in self._categories.values():
                if name in cat_tools:
                    cat_tools.remove(name)
    
    def get(self, name: str) -> BaseTool:
        \"\"\"获取工具\"\"\"
        if name not in self._tools:
            raise KeyError(f"工具 '{name}' 不存在")
        return self._tools[name]
    
    def list_all(self) -> List[str]:
        \"\"\"列出所有工具名\"\"\"
        return list(self._tools.keys())
    
    def list_by_category(self, category: str) -> List[str]:
        \"\"\"按类别列出工具\"\"\"
        return self._categories.get(category, [])
    
    def get_schemas(self, category: str = None) -> List[dict]:
        \"\"\"获取工具 Schema（给 LLM 使用）\"\"\"
        tools = self._tools.values()
        if category:
            tool_names = self._categories.get(category, [])
            tools = [self._tools[n] for n in tool_names if n in self._tools]
        return [t.get_schema() for t in tools]
    
    def execute(self, name: str, **kwargs) -> ToolOutput:
        \"\"\"执行工具\"\"\"
        tool = self.get(name)
        return tool.run(**kwargs)
`

### 2.2 装饰器注册

`python
# 更优雅的注册方式
def tool(name: str, description: str, category: str = "general"):
    \"\"\"工具装饰器\"\"\"
    def decorator(func):
        class DecoratedTool(BaseTool):
            name = name
            description = description
            
            def _execute(self, input_data):
                return func(**vars(input_data))
        
        # 自动注册
        DecoratedTool.__qualname__ = func.__qualname__
        return DecoratedTool
    
    return decorator

# 使用装饰器
@tool("calculator", "数学计算", "math")
def calculator(expression: str) -> str:
    return str(eval(expression))

@tool("uppercase", "转大写", "text")
def uppercase(text: str) -> str:
    return text.upper()
`

## 3. 工具描述的重要性

### 3.1 好的描述 vs 坏的描述

`python
# ❌ 坏的描述 - 模糊，LLM 不知道什么时候用
class BadSearchTool:
    name = "search"
    description = "搜索东西"

# ✅ 好的描述 - 明确，LLM 知道何时用、怎么用
class GoodSearchTool:
    name = "web_search"
    description = """在互联网上搜索实时信息。
    当你需要查找以下内容时使用此工具：
    - 最新新闻或事件
    - 技术文档或 API
    - 事实性信息验证
    不要用于：数学计算、代码执行、文件操作
    """
`

### 3.2 参数描述

`python
class SearchInput(ToolInput):
    query: str = Field(
        description="搜索关键词，建议使用英文获得更好结果",
        min_length=1,
        max_length=200
    )
    max_results: int = Field(
        default=5,
        description="返回结果数量，1-20，默认5",
        ge=1, le=20
    )
`

## 4. 工具发现机制

### 4.1 自动发现

`python
import os
import importlib

class ToolDiscoverer:
    \"\"\"自动发现和加载工具\"\"\"
    
    def __init__(self, tools_dir: str = "./tools"):
        self.tools_dir = tools_dir
    
    def discover(self) -> list[BaseTool]:
        \"\"\"扫描目录，自动加载工具\"\"\"
        tools = []
        
        for filename in os.listdir(self.tools_dir):
            if filename.endswith("_tool.py"):
                module_name = filename[:-3]
                spec = importlib.util.spec_from_file_location(
                    module_name, 
                    os.path.join(self.tools_dir, filename)
                )
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # 找到所有 BaseTool 子类
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if (isinstance(attr, type) and 
                        issubclass(attr, BaseTool) and 
                        attr is not BaseTool):
                        tools.append(attr())
        
        return tools
`

## 5. MCP 基础

### 5.1 什么是 MCP？

MCP（Model Context Protocol）是 Anthropic 提出的开放协议，用于标准化 LLM 与外部工具/数据的交互。

`
┌──────────┐     MCP      ┌──────────┐
│  LLM/    │ ◄──────────► │   MCP    │
│  Agent   │              │  Server  │
└──────────┘              └──────────┘
                               │
                         ┌─────┴─────┐
                         │   Tools   │
                         │ Resources │
                         │ Prompts   │
                         └───────────┘
`

### 5.2 MCP Server 基础实现

`python
from dataclasses import dataclass
from typing import Any, Callable


@dataclass
class MCPTool:
    \"\"\"MCP 工具定义\"\"\"
    name: str
    description: str
    input_schema: dict
    handler: Callable


class MCPServer:
    \"\"\"简化版 MCP Server\"\"\"
    
    def __init__(self, name: str):
        self.name = name
        self.tools: dict[str, MCPTool] = {}
    
    def tool(self, name: str, description: str, input_schema: dict = None):
        \"\"\"注册 MCP 工具\"\"\"
        def decorator(func):
            self.tools[name] = MCPTool(
                name=name,
                description=description,
                input_schema=input_schema or {},
                handler=func
            )
            return func
        return decorator
    
    def list_tools(self) -> list[dict]:
        \"\"\"列出所有工具（MCP 协议方法）\"\"\"
        return [
            {
                "name": t.name,
                "description": t.description,
                "inputSchema": t.input_schema
            }
            for t in self.tools.values()
        ]
    
    def call_tool(self, name: str, arguments: dict) -> Any:
        \"\"\"调用工具（MCP 协议方法）\"\"\"
        if name not in self.tools:
            raise ValueError(f"未知工具: {name}")
        return self.tools[name].handler(**arguments)


# 使用示例
server = MCPServer("my-tools")

@server.tool(
    name="add_numbers",
    description="两个数相加",
    input_schema={
        "type": "object",
        "properties": {
            "a": {"type": "number", "description": "第一个数"},
            "b": {"type": "number", "description": "第二个数"}
        },
        "required": ["a", "b"]
    }
)
def add_numbers(a: float, b: float) -> float:
    return a + b

# MCP 客户端调用
print(server.list_tools())  # 列出工具
print(server.call_tool("add_numbers", {"a": 1, "b": 2}))  # 调用工具
`

## 6. 常见错误

1. **描述太模糊**：LLM 不知道何时使用 → 写清使用场景
2. **没有输入验证**：恶意输入导致安全问题 → 用 Pydantic 验证
3. **错误处理缺失**：工具崩溃导致 Agent 停止 → 返回 ToolOutput
4. **工具太多**：LLM 选错工具 → 按类别分组，限制可见工具数
5. **没有工具版本**：更新工具破坏已有调用 → 版本化管理

## 7. 动手练习

### 练习 1：实现 BaseTool
创建 CalculatorTool、SearchTool、FileReadTool 三个工具。

### 练习 2：实现 ToolRegistry
实现注册、查询、执行、生成描述的完整功能。

### 练习 3：MCP Server
实现一个简单的 MCP Server，注册 3 个工具。
