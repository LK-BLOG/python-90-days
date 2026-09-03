"""Day 29 starter: AI引擎基础骨架

你需要实现：
1. AsyncChatEngine 类
2. 带重试的API调用
3. 流式输出支持
"""

from __future__ import annotations
import asyncio
import json
from dataclasses import dataclass
from openai import AsyncOpenAI


@dataclass
class ChatResponse:
    """API响应封装"""
    content: str | None
    tool_calls: list[dict] | None = None
    usage: dict | None = None


class AsyncChatEngine:
    """异步AI引擎"""
    
    def __init__(self, api_key: str, model: str = "gpt-4o-mini"):
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = model
    
    async def chat(
        self,
        messages: list[dict],
        tools: list[dict] | None = None,
        temperature: float = 0.7,
        max_tokens: int = 2000,
    ) -> ChatResponse:
        """发送聊天请求"""
        # TODO: 实现chat completion调用
        # - 调用 client.chat.completions.create
        # - 处理 tools 参数
        # - 封装返回 ChatResponse
        raise NotImplementedError
    
    async def chat_stream(self, messages: list[dict]):
        """流式输出"""
        # TODO: 实现流式输出
        # - stream=True
        # - async for chunk in stream
        # - yield 每个delta
        raise NotImplementedError
    
    async def chat_with_retry(self, messages: list[dict], max_retries: int = 3):
        """带重试的调用"""
        # TODO: 实现指数退避重试
        # - 捕获 RateLimitError, APIError
        # - 2 ** attempt 秒后重试
        raise NotImplementedError
