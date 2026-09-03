"""Day 29 示例4：工具注册器 + 装饰器模式"""

from __future__ import annotations
import inspect
import json
from dataclasses import dataclass, field
from typing import Any, Callable


@dataclass
class Tool:
    """工具描述"""
    name: str
    description: str
    parameters: dict
    func: Callable
    is_async: bool = False


class ToolRegistry:
    """工具注册器 —— 注册器模式"""
    
    def __init__(self):
        self._tools: dict[str, Tool] = {}
    
    def tool(self, name: str, description: str, parameters: dict | None = None):
        """装饰器：注册一个工具"""
        def decorator(func: Callable) -> Callable:
            is_async = inspect.iscoroutinefunction(func)
            
            if parameters is None:
                # 自动从函数签名推断参数（简化版）
                params = {}
                sig = inspect.signature(func)
                for pname, param in sig.parameters.items():
                    params[pname] = {
                        "type": _python_type_to_json(param.annotation),
                        "description": pname,
                    }
                auto_params = {
                    "type": "object",
                    "properties": params,
                    "required": [p for p, v in sig.parameters.items() if v.default is inspect.Parameter.empty],
                }
            else:
                auto_params = parameters
            
            self._tools[name] = Tool(
                name=name,
                description=description,
                parameters=auto_params,
                func=func,
                is_async=is_async,
            )
            return func
        return decorator
    
    def get_definitions(self) -> list[dict]:
        """获取所有工具的OpenAI格式定义"""
        return [
            {
                "type": "function",
                "function": {
                    "name": t.name,
                    "description": t.description,
                    "parameters": t.parameters,
                }
            }
            for t in self._tools.values()
        ]
    
    async def execute(self, name: str, **kwargs) -> Any:
        """执行指定工具"""
        if name not in self._tools:
            return f"错误: 未知工具 '{name}'"
        
        tool = self._tools[name]
        try:
            if tool.is_async:
                return await tool.func(**kwargs)
            else:
                return tool.func(**kwargs)
        except Exception as e:
            return f"工具执行错误: {type(e).__name__}: {e}"
    
    def list_tools(self) -> list[str]:
        """列出所有工具名"""
        return list(self._tools.keys())


def _python_type_to_json(annotation) -> str:
    """Python类型 → JSON Schema类型"""
    mapping = {
        str: "string",
        int: "integer",
        float: "number",
        bool: "boolean",
        list: "array",
        dict: "object",
    }
    return mapping.get(annotation, "string")


# ======== 使用示例 ========

registry = ToolRegistry()

@registry.tool(
    name="calculator",
    description="执行安全的数学计算",
    parameters={
        "type": "object",
        "properties": {
            "expression": {"type": "string", "description": "数学表达式"}
        },
        "required": ["expression"]
    }
)
def calculator(expression: str) -> str:
    import ast
    try:
        tree = ast.parse(expression, mode='eval')
        return str(eval(compile(tree, '<calc>', 'eval')))
    except Exception as e:
        return f"计算错误: {e}"

@registry.tool(
    name="word_count",
    description="统计文本的字数",
)
def word_count(text: str) -> str:
    return f"字数: {len(text)}, 词数: {len(text.split())}"

@registry.tool(
    name="upper_case",
    description="将文本转换为大写",
)
def upper_case(text: str) -> str:
    return text.upper()


if __name__ == "__main__":
    print("已注册工具:", registry.list_tools())
    print("工具定义:", json.dumps(registry.get_definitions(), indent=2, ensure_ascii=False))
    
    import asyncio
    print("\n测试 calculator:", asyncio.run(registry.execute("calculator", expression="2**10 + 1")))
    print("测试 word_count:", asyncio.run(registry.execute("word_count", text="Hello World 你好世界")))
