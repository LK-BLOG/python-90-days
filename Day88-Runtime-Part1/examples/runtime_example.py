'''
Day 88 示例：AI Assistant Runtime核心
'''

import asyncio
from dataclasses import dataclass, field
from typing import Any, Callable
from datetime import datetime


@dataclass
class AgentConfig:
    '''Agent配置'''
    name: str = "Assistant"
    model: str = "gpt-4"
    max_iterations: int = 10
    system_prompt: str = "你是一个有用的AI助手。"


class Agent:
    '''AI Assistant Agent'''
    
    def __init__(self, config: AgentConfig = None):
        self.config = config or AgentConfig()
        self.tools: dict[str, Callable] = {}
        self.memory: list[dict] = []
    
    def register_tool(self, name: str, func: Callable):
        '''注册工具'''
        self.tools[name] = func
    
    def add_memory(self, role: str, content: str):
        '''添加记忆'''
        self.memory.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
    
    async def run(self, user_input: str) -> str:
        '''运行Agent'''
        self.add_memory("user", user_input)
        
        # 简化的处理
        response = f"收到: {user_input}"
        self.add_memory("assistant", response)
        
        return response


# 示例工具
async def search(query: str) -> str:
    '''搜索工具'''
    return f"搜索 '{query}' 的结果"

def calculator(expression: str) -> str:
    '''计算器工具'''
    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return f"计算结果: {expression} = {result}"
    except Exception as e:
        return f"计算错误: {e}"


async def main():
    '''演示AI Assistant Runtime'''
    print("=" * 60)
    print("AI Assistant Runtime 演示")
    print("=" * 60)
    
    # 创建Agent
    agent = Agent(AgentConfig(name="Demo Assistant"))
    
    # 注册工具
    agent.register_tool("search", search)
    agent.register_tool("calculator", calculator)
    
    print(f"\nAgent: {agent.config.name}")
    print(f"已注册工具: {list(agent.tools.keys())}")
    
    # 运行
    response = await agent.run("你好！")
    print(f"\n响应: {response}")
    
    print(f"\n记忆:")
    for mem in agent.memory:
        print(f"  {mem['role']}: {mem['content']}")
    
    print("\n" + "=" * 60)
    print("演示完成！")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
