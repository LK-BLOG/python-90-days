# Day 29 - Challenge 1&2: AI Engine + Prompt Engineering
# AI 引擎骨架 + 代码审查机器人 Prompt 设计

import json
import asyncio
from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class Message:
    """对话消息"""
    role: str  # system / user / assistant / tool
    content: str
    name: str = ""
    tool_call_id: str = ""
    tool_calls: list[dict] = field(default_factory=list)


@dataclass
class TokenUsage:
    """Token 用量"""
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    estimated_cost: float = 0.0


@dataclass
class AIResponse:
    """AI 响应"""
    content: str = ""
    tool_calls: list[dict] = field(default_factory=list)
    usage: TokenUsage = field(default_factory=TokenUsage)
    finish_reason: str = ""


class AIEngine:
    """AI 引擎

    封装 OpenAI API 调用，支持同步和异步调用。
    """

    def __init__(self, api_key: str, model: str = "gpt-4",
                 base_url: str = "https://api.openai.com/v1"):
        """初始化

        Args:
            api_key: OpenAI API Key
            model: 模型名称
            base_url: API 基础 URL
        """
        self.api_key = api_key
        self.model = model
        self.base_url = base_url

    async def chat(self, messages: list[Message], **kwargs) -> AIResponse:
        """发送对话请求

        Args:
            messages: 消息列表
            **kwargs: 其他参数（temperature, max_tokens 等）

        Returns:
            AIResponse 对象
        """
        # TODO: 构建 API 请求
        # TODO: 使用 httpx 或 urllib 发送请求
        # TODO: 解析响应
        ...

    async def chat_stream(self, messages: list[Message], **kwargs):
        """流式对话请求

        Args:
            messages: 消息列表

        Yields:
            每次生成的内容片段
        """
        # TODO: 设置 stream=True
        # TODO: 逐行解析 SSE 数据
        ...

    def count_tokens(self, messages: list[Message]) -> int:
        """估算 Token 数量

        Args:
            messages: 消息列表

        Returns:
            估算的 token 数
        """
        # TODO: 简单估算（中文约 2 token/字，英文约 0.75 token/word）
        ...


class CodeReviewPromptBuilder:
    """代码审查机器人 Prompt 构建器

    使用 Few-shot + Chain-of-Thought 设计 Prompt。
    """

    SYSTEM_PROMPT = """你是一个专业的代码审查机器人。你的任务是：
1. 分析代码的质量、安全性、性能
2. 按严重程度分类问题
3. 给出具体的修改建议
4. 输出 JSON 格式的结果"""

    FEW_SHOT_EXAMPLES = [
        {
            "input": "def add(a,b): return a+b",
            "output": {
                "issues": [
                    {"line": 1, "severity": "low", "message": "缺少类型注解",
                     "suggestion": "def add(a: int, b: int) -> int:"}
                ],
                "score": 7,
            },
        },
    ]

    @classmethod
    def build_messages(cls, code: str, language: str = "python") -> list[Message]:
        """构建代码审查的完整消息列表

        Args:
            code: 待审查的代码
            language: 编程语言

        Returns:
            消息列表（含 system + few-shot + user）
        """
        # TODO: 组装 system prompt + few-shot 示例 + Chain-of-Thought 引导
        # TODO: 如果代码过长，自动截断
        ...

    @staticmethod
    def truncate_code(code: str, max_tokens: int = 3000) -> str:
        """截断过长的代码

        Args:
            code: 源代码
            max_tokens: 最大 token 数

        Returns:
            截断后的代码
        """
        # TODO: 按行保留前 N 行，附带截断提示
        ...


# ==================== 测试 ====================
if __name__ == "__main__":
    engine = AIEngine(api_key="demo_key")
    print(f"AI 引擎初始化: model={engine.model}")

    # 测试 Prompt 构建
    messages = CodeReviewPromptBuilder.build_messages(
        "def add(a,b):\n    return a+b\n"
    )
    print(f"构建了 {len(messages)} 条消息")
    for msg in messages:
        print(f"  [{msg.role}] {msg.content[:50]}...")
