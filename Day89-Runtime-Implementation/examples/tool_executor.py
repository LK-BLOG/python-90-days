#!/usr/bin/env python3
"""Tool Execution Engine Example"""

import asyncio
from typing import Callable, Any, Dict, List
import inspect


class Tool:
    """Tool wrapper"""
    def __init__(self, name: str, func: Callable, description: str):
        self.name = name
        self.func = func
        self.description = description
        self.parameters = self._extract_parameters()
    
    def _extract_parameters(self) -> Dict:
        sig = inspect.signature(self.func)
        params = {}
        for name, param in sig.parameters.items():
            params[name] = {
                "type": param.annotation.__name__ if param.annotation != inspect.Parameter.empty else "any",
                "required": param.default == inspect.Parameter.empty,
                "default": param.default if param.default != inspect.Parameter.empty else None
            }
        return params
    
    async def execute(self, **kwargs) -> Any:
        if asyncio.iscoroutinefunction(self.func):
            return await self.func(**kwargs)
        return self.func(**kwargs)


class ToolExecutor:
    """Tool execution engine"""
    def __init__(self):
        self.tools: Dict[str, Tool] = {}
    
    def register(self, name: str = None, description: str = ""):
        """Decorator to register a tool"""
        def decorator(func: Callable):
            tool_name = name or func.__name__
            self.tools[tool_name] = Tool(tool_name, func, description)
            return func
        return decorator
    
    async def execute(self, tool_calls: List[Dict]) -> List[Any]:
        """Execute tool calls"""
        results = []
        for call in tool_calls:
            tool_name = call["name"]
            args = call.get("arguments", {})
            if tool_name not in self.tools:
                raise ValueError(f"Tool not found: {tool_name}")
            tool = self.tools[tool_name]
            result = await tool.execute(**args)
            results.append({"tool": tool_name, "result": result, "success": True})
        return results


# Create executor
executor = ToolExecutor()


@executor.register(description="Calculate math expression")
def calculator(expression: str) -> float:
    """Safe calculator"""
    allowed_chars = set("0123456789+-*/(). ")
    if not all(c in allowed_chars for c in expression):
        raise ValueError("Invalid characters in expression")
    return eval(expression)


@executor.register(description="Search in database")
async def database_search(query: str, limit: int = 10) -> list:
    """Simulated database search"""
    await asyncio.sleep(0.1)
    return [{"id": i, "name": f"result_{i}"} for i in range(min(limit, 5))]


@executor.register(description="Read file content")
def read_file(path: str) -> str:
    """Read file content"""
    import os
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


async def main():
    print("=== Tool Executor Example ===")
    
    # List tools
    print("\nRegistered tools:")
    for name, tool in executor.tools.items():
        print(f"  - {name}: {tool.description}")
    
    # Execute calculator
    print("\nTest calculator:")
    result = await executor.execute([{"name": "calculator", "arguments": {"expression": "2 + 3 * 4"}}])
    print(f"  2 + 3 * 4 = {result[0][\"result\"]}")
    
    # Execute database search
    print("\nTest database search:")
    result = await executor.execute([{"name": "database_search", "arguments": {"query": "test", "limit": 3}}])
    print(f"  Results: {result[0][\"result\"]}")


if __name__ == "__main__":
    asyncio.run(main())
