# Challenge 4 Starter: Agent核心 + AI引擎

from __future__ import annotations
import json
import asyncio
from typing import AsyncGenerator, Any
from dataclasses import dataclass
from openai import AsyncOpenAI


@dataclass
class ChatResponse:
    content: str | None
    tool_calls: list | None = None
    usage: dict | None = None


class AIEngine:
    def __init__(self, api_key: str, model: str = "gpt-4o-mini", **kwargs):
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = model
        self.temperature = kwargs.get("temperature", 0.7)
        self.max_tokens = kwargs.get("max_tokens", 2000)

    async def chat(self, messages, tools=None) -> ChatResponse:
        # TODO: 调用API
        ...

    async def chat_stream(self, messages) -> AsyncGenerator[str, None]:
        # TODO: 流式输出
        ...


class Agent:
    def __init__(self, engine: AIEngine, tools, memory, max_iterations: int = 10):
        self.engine = engine
        self.tools = tools
        self.memory = memory
        self.max_iterations = max_iterations

    async def run(self, user_input: str) -> AsyncGenerator[str, None]:
        # TODO: ReAct循环
        # 1. add user message
        # 2. loop: chat → check tool_calls → execute → continue
        # 3. yield final answer
        ...

    async def _execute_parallel(self, tool_calls) -> list[dict]:
        # TODO: asyncio.gather并行执行
        ...
