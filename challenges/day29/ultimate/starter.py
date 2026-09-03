"""Day 29 Boss挑战 starter: AI助手Agent
构建完整的AI助手。这是骨架代码，你需要实现所有TODO部分。
"""

from __future__ import annotations
import asyncio
import json
import logging
import os
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Callable

from openai import AsyncOpenAI, APIError, RateLimitError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ════════════════════════════════════════
# 第一部分：工具注册系统
# ════════════════════════════════════════

@dataclass
class Tool:
    name: str
    description: str
    parameters: dict
    func: Callable
    is_async: bool = False


class ToolRegistry:
    """工具注册器"""
    
    def __init__(self):
        self._tools: dict[str, Tool] = {}
    
    def register(self, name: str, description: str, parameters: dict):
        """装饰器注册工具"""
        def decorator(func: Callable) -> Callable:
            # TODO: 创建Tool并注册
            ...
            return func
        return decorator
    
    def get_definitions(self) -> list[dict]:
        # TODO: 返回OpenAI格式工具定义
        ...
    
    async def execute(self, name: str, **kwargs) -> Any:
        # TODO: 执行工具
        ...
    
    def list_tools(self) -> list[str]:
        return list(self._tools.keys())


# ════════════════════════════════════════
# 第二部分：AI引擎
# ════════════════════════════════════════

class AIEngine:
    """AI引擎"""
    
    def __init__(self, api_key: str, model: str = "gpt-4o-mini"):
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = model
    
    async def chat(self, messages, tools=None, temperature=0.7, max_tokens=2000):
        # TODO: 实现chat completion
        ...
    
    async def chat_stream(self, messages):
        # TODO: 流式输出
        ...


# ════════════════════════════════════════
# 第三部分：Memory系统
# ════════════════════════════════════════

class Memory:
    def __init__(self, system_prompt: str, max_tokens: int = 4000):
        self.system_prompt = system_prompt
        self.max_tokens = max_tokens
        self._messages: list[dict] = []
        self.summary = ""
    
    def add(self, role: str, content: str):
        # TODO
        ...
    
    def get_messages(self) -> list[dict]:
        # TODO: 返回带token控制的消息列表
        ...
    
    async def compress_if_needed(self, engine: AIEngine):
        # TODO: 如果消息太多，用AI压缩
        ...
    
    def clear(self):
        self._messages.clear()
        self.summary = ""
    
    def save(self, path: str):
        # TODO: 保存到JSON
        ...
    
    def load(self, path: str):
        # TODO: 从JSON加载
        ...


# ════════════════════════════════════════
# 第四部分：Agent
# ════════════════════════════════════════

class Agent:
    def __init__(self, api_key: str):
        self.engine = AIEngine(api_key)
        self.registry = ToolRegistry()
        self.memory = Memory("你是一个有用的AI助手。")
        self.max_iterations = 10
        self._register_builtins()
    
    def _register_builtins(self):
        """注册内置工具"""
        # TODO: 注册 calculator, file_read, file_write, code_exec, search
        ...
    
    async def run(self, user_input: str) -> str:
        # TODO: Agent主循环
        ...
    
    async def _execute_parallel(self, tool_calls) -> list[dict]:
        # TODO: 并行执行工具
        ...


# ════════════════════════════════════════
# 第五部分：CLI
# ════════════════════════════════════════

class CLI:
    def __init__(self, api_key: str):
        self.agent = Agent(api_key)
    
    async def run(self):
        """交互式循环"""
        # TODO: 实现CLI循环
        # - 支持 /clear, /history, /tools, /quit
        # - 调用 agent.run()
        # - 处理异常
        ...


if __name__ == "__main__":
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("请设置 OPENAI_API_KEY 环境变量")
        exit(1)
    asyncio.run(CLI(api_key).run())
