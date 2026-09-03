"""Day 29 starter: Agent骨架"""

from __future__ import annotations
import json
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Tool:
    name: str
    description: str
    parameters: dict
    func: Any  # Callable


class ToolRegistry:
    """工具注册器"""
    
    def __init__(self):
        self._tools: dict[str, Tool] = {}
    
    def register(self, name: str, description: str, parameters: dict):
        """装饰器：注册工具"""
        def decorator(func):
            # TODO: 创建Tool对象并注册到self._tools
            ...
            return func
        return decorator
    
    def get_definitions(self) -> list[dict]:
        """获取OpenAI格式的工具定义"""
        # TODO: 返回所有工具的OpenAI格式定义
        ...
    
    async def execute(self, name: str, **kwargs) -> Any:
        """执行工具"""
        # TODO: 查找并执行工具
        ...


class Agent:
    """ReAct Agent"""
    
    def __init__(self, engine, tools: ToolRegistry, memory, max_iterations: int = 10):
        self.engine = engine
        self.tools = tools
        self.memory = memory
        self.max_iterations = max_iterations
    
    async def run(self, user_input: str) -> str:
        """Agent主循环"""
        # TODO: 实现ReAct循环
        # 1. 添加用户消息到memory
        # 2. 循环：调用engine → 检查tool_calls → 执行工具 → 继续
        # 3. 达到最大迭代时返回错误信息
        ...
