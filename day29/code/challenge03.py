"""Challenge 3: Function Calling
实现工具调用系统。
"""

import json
import asyncio
from openai import AsyncOpenAI

API_KEY = "your-api-key-here"

# ======== 工具定义 ========

TOOLS = [
    # TODO: 定义至少3个工具
    # 1. calculator: 数学计算
    # 2. text_stats: 文本统计（字数、行数等）
    # 3. reverse_text: 反转文本
]


# ======== 工具执行 ========

def execute_tool(name: str, arguments: dict) -> str:
    """根据名称执行工具"""
    # TODO: 实现工具分发
    # - 根据name调用对应函数
    # - 处理参数
    # - 返回结果字符串
    ...


def calculator(expression: str) -> str:
    """安全的数学计算"""
    # TODO
    ...


def text_stats(text: str) -> str:
    """文本统计"""
    # TODO: 返回字数、行数、字符数
    ...


def reverse_text(text: str) -> str:
    """反转文本"""
    # TODO
    ...


# ======== Agent循环 ========

async def tool_call_loop(user_input: str):
    """完整的工具调用循环"""
    client = AsyncOpenAI(api_key=API_KEY)
    messages = [
        {"role": "system", "content": "你可以使用工具来帮助用户。"},
        {"role": "user", "content": user_input},
    ]
    
    # TODO: 实现循环
    # 1. 调用API（带上tools参数）
    # 2. 检查是否有tool_calls
    # 3. 执行工具，把结果加入messages
    # 4. 继续循环直到没有tool_calls
    ...


if __name__ == "__main__":
    asyncio.run(tool_call_loop("计算 (15*3) + 7 的结果，然后把结果反转成字符串"))
