"""Challenge 2: Prompt Engineering实战
设计代码审查机器人的Prompt系统。
"""

import asyncio
import json
from openai import AsyncOpenAI

API_KEY = "your-api-key-here"


def build_system_prompt() -> str:
    """构建系统提示"""
    # TODO: 设计完整的系统提示
    # - 角色定义
    # - Few-shot 示例
    # - Chain-of-Thought 引导
    # - JSON输出格式说明
    ...


def build_review_prompt(code: str) -> list[dict]:
    """构建审查消息"""
    system = build_system_prompt()
    
    # TODO: 
    # - 检查代码长度，过长则截断
    # - 构建 messages 列表
    # - 用CoT引导逐步分析
    ...


async def review_code(code: str) -> dict:
    """执行代码审查"""
    client = AsyncOpenAI(api_key=API_KEY)
    
    messages = build_review_prompt(code)
    
    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        # TODO: 如果支持，使用 response_format=json_object
    )
    
    content = response.choices[0].message.content
    
    # TODO: 解析JSON响应
    ...


if __name__ == "__main__":
    sample_code = '''
def fib(n):
    if n <= 1:
        return n
    return fib(n-1) + fib(n-2)
'''
    result = asyncio.run(review_code(sample_code))
    print(json.dumps(result, indent=2, ensure_ascii=False))
