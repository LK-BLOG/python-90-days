"""Challenge 1: 基础API调用
用openai库和httpx分别实现对话调用。
"""

import asyncio
from openai import AsyncOpenAI, APIError, RateLimitError, AuthenticationError
import httpx

API_KEY = "your-api-key-here"


async def chat_with_sdk():
    """用openai SDK调用"""
    client = AsyncOpenAI(api_key=API_KEY)
    
    # TODO: 调用 chat.completions.create
    # - messages: system + user
    # - 打印回复内容
    # - 打印 token 用量
    ...


async def chat_with_httpx():
    """用httpx直接调用"""
    # TODO: 用 httpx.AsyncClient 发送POST请求
    # - URL: https://api.openai.com/v1/chat/completions
    # - Headers: Authorization, Content-Type
    # - 解析响应JSON
    ...


async def chat_with_retry():
    """带重试的调用"""
    # TODO: 实现重试逻辑
    # - 捕获 RateLimitError: 等待 2^attempt 秒
    # - 捕获 AuthenticationError: 直接报错
    # - 最多重试3次
    ...


if __name__ == "__main__":
    asyncio.run(chat_with_sdk())
