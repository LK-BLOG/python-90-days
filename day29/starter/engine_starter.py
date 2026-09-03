# Day 29 - Challenge 3: Function Calling 工具系统
# 计算器、天气查询、文本处理 + tool_call 循环

import json
import math
from dataclasses import dataclass
from typing import Any, Callable


@dataclass
class ToolDefinition:
    """工具定义"""
    name: str
    description: str
    parameters: dict  # JSON Schema 格式
    func: Callable


class ToolRegistry:
    """工具注册器

    管理和执行工具调用，支持 OpenAI Function Calling 格式。
    """

    def __init__(self):
        self._tools: dict[str, ToolDefinition] = {}

    def register(self, name: str, description: str, parameters: dict):
        """装饰器：注册一个工具

        Args:
            name: 工具名
            description: 工具描述
            parameters: JSON Schema 参数定义

        用法：
            @registry.register("calc", "计算表达式", {...})
            def calc(expression: str) -> str:
                ...
        """
        def decorator(func: Callable) -> Callable:
            # TODO: 创建 ToolDefinition 并注册
            self._tools[name] = ToolDefinition(
                name=name, description=description,
                parameters=parameters, func=func
            )
            return func
        return decorator

    def get_definitions(self) -> list[dict]:
        """获取 OpenAI 格式的工具定义列表

        Returns:
            工具定义字典列表
        """
        # TODO: 返回 [{"type": "function", "function": {...}}, ...]
        ...

    def execute(self, name: str, arguments: str) -> str:
        """执行工具调用

        Args:
            name: 工具名
            arguments: JSON 格式的参数字符串

        Returns:
            工具执行结果（JSON 字符串）

        Raises:
            ValueError: 工具不存在
        """
        # TODO: 查找工具，解析参数，调用函数
        ...

    def list_tools(self) -> list[str]:
        """列出所有已注册的工具名"""
        return list(self._tools.keys())


# ---- 具体工具实现 ----

registry = ToolRegistry()


@registry.register(
    name="calculator",
    description="计算数学表达式，支持加减乘除、幂运算、三角函数等",
    parameters={
        "type": "object",
        "properties": {
            "expression": {"type": "string", "description": "数学表达式"}
        },
        "required": ["expression"]
    }
)
def calculator(expression: str) -> str:
    """执行数学计算

    Args:
        expression: 数学表达式字符串

    Returns:
        计算结果的 JSON 字符串
    """
    # TODO: 安全地计算表达式（使用 math 模块或 ast.literal_eval）
    ...


@registry.register(
    name="word_count",
    description="统计文本的字数、词数、行数",
    parameters={
        "type": "object",
        "properties": {
            "text": {"type": "string", "description": "待统计的文本"}
        },
        "required": ["text"]
    }
)
def word_count(text: str) -> str:
    """统计文本信息

    Args:
        text: 待统计的文本

    Returns:
        统计结果的 JSON 字符串
    """
    # TODO: 统计字符数、单词数、行数
    ...


@registry.register(
    name="weather",
    description="查询指定城市的天气信息",
    parameters={
        "type": "object",
        "properties": {
            "city": {"type": "string", "description": "城市名"}
        },
        "required": ["city"]
    }
)
def weather(city: str) -> str:
    """查询天气（模拟）

    Args:
        city: 城市名

    Returns:
        天气信息的 JSON 字符串
    """
    # TODO: 模拟返回天气数据
    return json.dumps({"city": city, "temp": 25, "weather": "sunny"})


# ==================== 测试 ====================
if __name__ == "__main__":
    print("已注册工具:", registry.list_tools())
    print("\n工具定义:")
    for defn in registry.get_definitions():
        print(f"  {defn['function']['name']}: {defn['function']['description'][:30]}...")
    print("\n执行 calculator:")
    result = registry.execute("calculator", '{"expression": "2**10"}')
    print(f"  结果: {result}")
