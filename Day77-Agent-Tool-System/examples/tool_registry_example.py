'''
Day 77 示例：工具注册表实现
'''

from dataclasses import dataclass
from typing import Any
from abc import ABC, abstractmethod


@dataclass
class ToolParameter:
    '''工具参数'''
    name: str
    type: str
    description: str
    required: bool = True
    default: Any = None


@dataclass
class ToolResult:
    '''工具结果'''
    success: bool
    output: Any
    error: str | None = None


class BaseTool(ABC):
    '''工具基类'''
    
    def __init__(self, name: str, description: str, parameters: list[ToolParameter] = None):
        self.name = name
        self.description = description
        self.parameters = parameters or []
    
    @abstractmethod
    def execute(self, **kwargs) -> ToolResult:
        '''执行工具'''
        pass
    
    def to_schema(self) -> dict:
        '''生成OpenAI格式的schema'''
        props = {}
        required = []
        
        for p in self.parameters:
            props[p.name] = {
                "type": p.type,
                "description": p.description
            }
            if p.required:
                required.append(p.name)
        
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "type": "object",
                "properties": props,
                "required": required
            }
        }


class ToolRegistry:
    '''工具注册表'''
    
    def __init__(self):
        self._tools: dict[str, BaseTool] = {}
        self._categories: dict[str, list[str]] = {}
    
    def register(self, tool: BaseTool, category: str = "general"):
        '''注册工具'''
        self._tools[tool.name] = tool
        
        if category not in self._categories:
            self._categories[category] = []
        self._categories[category].append(tool.name)
        
        print(f"注册工具: {tool.name} (分类: {category})")
    
    def unregister(self, name: str):
        '''注销工具'''
        if name in self._tools:
            del self._tools[name]
            # 从分类中移除
            for cat, tools in self._categories.items():
                if name in tools:
                    tools.remove(name)
    
    def get(self, name: str) -> BaseTool | None:
        '''获取工具'''
        return self._tools.get(name)
    
    def list_all(self) -> list[dict]:
        '''列出所有工具'''
        return [
            {"name": t.name, "description": t.description}
            for t in self._tools.values()
        ]
    
    def search(self, query: str) -> list[BaseTool]:
        '''搜索工具'''
        query_lower = query.lower()
        return [
            t for t in self._tools.values()
            if query_lower in t.description.lower()
        ]
    
    def get_schemas(self) -> list[dict]:
        '''获取所有工具的schema'''
        return [t.to_schema() for t in self._tools.values()]


# 示例工具
class SearchTool(BaseTool):
    '''搜索工具'''
    
    def __init__(self):
        super().__init__(
            name="search",
            description="在互联网上搜索信息",
            parameters=[
                ToolParameter("query", "string", "搜索关键词"),
                ToolParameter("num_results", "number", "结果数量", required=False, default=5)
            ]
        )
    
    def execute(self, **kwargs) -> ToolResult:
        query = kwargs.get("query", "")
        return ToolResult(True, f"搜索 '{query}' 的结果...")


class CalculatorTool(BaseTool):
    '''计算器工具'''
    
    def __init__(self):
        super().__init__(
            name="calculator",
            description="执行数学计算",
            parameters=[
                ToolParameter("expression", "string", "数学表达式")
            ]
        )
    
    def execute(self, **kwargs) -> ToolResult:
        try:
            expr = kwargs.get("expression", "")
            result = eval(expr, {"__builtins__": {}}, {})
            return ToolResult(True, result)
        except Exception as e:
            return ToolResult(False, None, str(e))


def main():
    '''演示工具注册表'''
    print("=" * 60)
    print("工具注册表演示")
    print("=" * 60)
    
    # 创建注册表
    registry = ToolRegistry()
    
    # 注册工具
    registry.register(SearchTool(), "search")
    registry.register(CalculatorTool(), "math")
    
    # 列出工具
    print("\n所有工具:")
    for tool_info in registry.list_all():
        print(f"  - {tool_info['name']}: {tool_info['description']}")
    
    # 搜索工具
    print("\n搜索 '计算':")
    tools = registry.search("计算")
    for tool in tools:
        print(f"  - {tool.name}")
    
    # 获取schema
    print("\n工具Schema:")
    import json
    schemas = registry.get_schemas()
    print(json.dumps(schemas, indent=2, ensure_ascii=False))
    
    # 执行工具
    print("\n执行计算器工具:")
    calc = registry.get("calculator")
    if calc:
        result = calc.execute(expression="2 + 3 * 4")
        print(f"结果: {result.output}")


if __name__ == "__main__":
    main()
