"""Challenge 5: 多工具Agent
构建完整的ReAct Agent。
"""

from __future__ import annotations
import json
import asyncio
import logging
from openai import AsyncOpenAI

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)


class Agent:
    def __init__(self, api_key: str, model: str = "gpt-4o-mini"):
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = model
        self.messages: list[dict] = [
            {"role": "system", "content": "你是一个有用的AI助手。可以使用工具来完成任务。"}
        ]
        self.tools: list[dict] = []
        self.tool_map: dict = {}
        self.max_iterations = 10
    
    def register_tool(self, name: str, description: str, parameters: dict, func):
        """注册工具"""
        # TODO: 添加到self.tools和self.tool_map
        ...
    
    async def run(self, user_input: str) -> str:
        """Agent主循环"""
        self.messages.append({"role": "user", "content": user_input})
        
        for i in range(self.max_iterations):
            logger.info(f"--- 迭代 {i+1} ---")
            
            # TODO: 调用API
            response = ...
            
            # TODO: 检查tool_calls
            # TODO: 如果有tool_calls，执行工具（支持并行）
            # TODO: 如果没有，返回最终回答
            ...
        
        return "达到最大迭代次数"
    
    async def _execute_tools_parallel(self, tool_calls) -> list[dict]:
        """并行执行多个工具"""
        # TODO: 用asyncio.gather并行执行
        ...


# 注册一些工具
agent = Agent(api_key="your-key")

# TODO: 注册至少3个工具（计算器、文件读取、文本处理）

if __name__ == "__main__":
    asyncio.run(agent.run("帮我分析这段代码的质量"))
