"""Day 30 - AI 引擎（封装 OpenAI API 调用）"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, AsyncIterator, Optional


@dataclass
class TokenUsage:
    """Token 用量统计"""
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0

    @property
    def estimated_cost(self) -> float:
        """估算费用（按 GPT-4 价格）"""
        # TODO: 根据 token 数估算费用
        return self.prompt_tokens * 0.00003 + self.completion_tokens * 0.00006


@dataclass
class AIResponse:
    """AI 响应"""
    content: str = ""
    tool_calls: list[dict] = field(default_factory=list)
    usage: TokenUsage = field(default_factory=TokenUsage)
    finish_reason: str = ""


class AIEngine:
    """AI 引擎

    封装 OpenAI API 调用，支持同步/异步、流式/非流式。
    """

    def __init__(self, api_key: str, model: str = "gpt-4",
                 base_url: str = "https://api.openai.com/v1"):
        self.api_key = api_key
        self.model = model
        self.base_url = base_url

    async def chat(self, messages: list[dict],
                   tools: list[dict] = None,
                   temperature: float = 0.7,
                   max_tokens: int = 4096) -> AIResponse:
        """发送对话请求

        Args:
            messages: 消息列表
            tools: 工具定义列表
            temperature: 温度参数
            max_tokens: 最大生成 token 数

        Returns:
            AIResponse 对象
        """
        # TODO: 构建请求体
        # TODO: 发送到 /chat/completions
        # TODO: 解析响应
        ...

    async def chat_stream(self, messages: list[dict],
                          **kwargs) -> AsyncIterator[str]:
        """流式对话

        Args:
            messages: 消息列表

        Yields:
            每次生成的文本片段
        """
        # TODO: stream=True，逐块解析 SSE
        ...

    def count_tokens(self, text: str) -> int:
        """估算 token 数"""
        # TODO: 中文约2 token/字，英文约0.75 token/word
        return len(text) // 2 if text else 0
