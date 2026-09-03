"""Day 29 示例1：OpenAI API基础调用"""

import asyncio
import httpx
from openai import AsyncOpenAI

# ======== 方式1：使用OpenAI SDK ========

async def chat_with_sdk():
    """使用openai库调用Chat Completion"""
    client = AsyncOpenAI(api_key="your-api-key")
    
    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "你是一个Python教学助手，用简洁的中文回答问题。"},
            {"role": "user", "content": "用一句话解释什么是装饰器？"},
        ],
        temperature=0.7,
        max_tokens=200,
    )
    
    print(f"回复: {response.choices[0].message.content}")
    print(f"Token用量: prompt={response.usage.prompt_tokens}, completion={response.usage.completion_tokens}, total={response.usage.total_tokens}")


# ======== 方式2：使用httpx直接调用 ========

async def chat_with_httpx(api_key: str):
    """使用httpx直接调用OpenAI API"""
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": "gpt-4o-mini",
                "messages": [
                    {"role": "user", "content": "用一句话解释什么是装饰器？"},
                ],
                "temperature": 0.7,
            },
        )
        response.raise_for_status()
        data = response.json()
        print(f"回复: {data['choices'][0]['message']['content']}")


# ======== 方式3：流式输出 ========

async def chat_streaming():
    """流式输出，逐字打印"""
    client = AsyncOpenAI(api_key="your-api-key")
    
    stream = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "写一个Python快排实现"}],
        stream=True,
    )
    
    full_response = ""
    async for chunk in stream:
        delta = chunk.choices[0].delta
        if delta.content:
            print(delta.content, end="", flush=True)
            full_response += delta.content
    
    print()  # 换行
    return full_response


# ======== 错误处理 ========

from openai import APIError, RateLimitError, AuthenticationError

async def chat_with_retry(max_retries: int = 3):
    """带重试的API调用"""
    client = AsyncOpenAI(api_key="your-api-key")
    
    for attempt in range(max_retries):
        try:
            response = await client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": "Hello"}],
            )
            return response.choices[0].message.content
            
        except AuthenticationError:
            print("API Key无效")
            raise
        except RateLimitError:
            wait = 2 ** attempt
            print(f"速率限制，等待{wait}秒后重试...")
            await asyncio.sleep(wait)
        except APIError as e:
            print(f"API错误: {e}")
            if attempt == max_retries - 1:
                raise
    
    return "达到最大重试次数"


if __name__ == "__main__":
    # 注意：需要设置真实的API Key才能运行
    # asyncio.run(chat_with_sdk())
    print("示例代码，请设置API Key后运行")
