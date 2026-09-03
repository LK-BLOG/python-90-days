'''
Day 78 示例：工具开发实战
'''

import asyncio
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


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


# 示例1：文件操作工具
class FileTool(BaseTool):
    '''文件操作工具'''
    
    def __init__(self):
        super().__init__(
            name="file",
            description="读写文件",
            parameters=[
                ToolParameter("operation", "string", "操作: read/write"),
                ToolParameter("path", "string", "文件路径"),
                ToolParameter("content", "string", "写入内容", required=False)
            ]
        )
    
    def execute(self, **kwargs) -> ToolResult:
        op = kwargs.get("operation")
        path = kwargs.get("path")
        content = kwargs.get("content")
        
        try:
            if op == "read":
                with open(path, 'r', encoding='utf-8') as f:
                    return ToolResult(True, f.read())
            elif op == "write":
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(content)
                return ToolResult(True, f"已写入: {path}")
            else:
                return ToolResult(False, None, f"未知操作: {op}")
        except Exception as e:
            return ToolResult(False, None, str(e))


# 示例2：计算器工具
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
        expr = kwargs.get("expression")
        try:
            # 安全的数学计算
            result = eval(expr, {"__builtins__": {}}, {
                "abs": abs, "round": round,
                "min": min, "max": max
            })
            return ToolResult(True, result)
        except Exception as e:
            return ToolResult(False, None, str(e))


# 示例3：文本处理工具
class TextTool(BaseTool):
    '''文本处理工具'''
    
    def __init__(self):
        super().__init__(
            name="text",
            description="处理文本：统计字数、转换大小写等",
            parameters=[
                ToolParameter("operation", "string", "操作: count/upper/lower/title"),
                ToolParameter("text", "string", "输入文本")
            ]
        )
    
    def execute(self, **kwargs) -> ToolResult:
        op = kwargs.get("operation")
        text = kwargs.get("text")
        
        if op == "count":
            return ToolResult(True, len(text))
        elif op == "upper":
            return ToolResult(True, text.upper())
        elif op == "lower":
            return ToolResult(True, text.lower())
        elif op == "title":
            return ToolResult(True, text.title())
        else:
            return ToolResult(False, None, f"未知操作: {op}")


async def main():
    '''演示工具'''
    print("=" * 60)
    print("工具开发实战演示")
    print("=" * 60)
    
    # 创建工具
    tools = {
        "file": FileTool(),
        "calculator": CalculatorTool(),
        "text": TextTool()
    }
    
    # 测试计算器
    print("\n1. 计算器工具:")
    calc = tools["calculator"]
    result = calc.execute(expression="(2 + 3) * 4")
    print(f"  (2 + 3) * 4 = {result.output}")
    
    result = calc.execute(expression="10 / 3")
    print(f"  10 / 3 = {result.output}")
    
    # 测试文本处理
    print("\n2. 文本处理工具:")
    text_tool = tools["text"]
    
    result = text_tool.execute(operation="count", text="Hello World")
    print(f"  字数统计: {result.output}")
    
    result = text_tool.execute(operation="upper", text="hello world")
    print(f"  转大写: {result.output}")
    
    result = text_tool.execute(operation="title", text="hello world")
    print(f"  转标题: {result.output}")
    
    # 测试文件操作
    print("\n3. 文件操作工具:")
    file_tool = tools["file"]
    
    # 写入文件
    result = file_tool.execute(
        operation="write",
        path="test.txt",
        content="Hello from tools demo!"
    )
    print(f"  写入: {result.output}")
    
    # 读取文件
    result = file_tool.execute(operation="read", path="test.txt")
    print(f"  读取: {result.output}")
    
    # 清理
    import os
    if os.path.exists("test.txt"):
        os.remove("test.txt")
    
    print("\n" + "=" * 60)
    print("演示完成！")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
