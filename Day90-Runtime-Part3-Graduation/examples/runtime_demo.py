'''
Day 90 示例：完整的AI Assistant Runtime演示
'''

import asyncio
from dataclasses import dataclass, field
from typing import Any, Callable
from datetime import datetime


@dataclass
class AgentConfig:
    '''Agent配置'''
    name: str = "AI Assistant"
    model: str = "gpt-4"
    max_iterations: int = 10
    system_prompt: str = "你是一个有用的AI助手。"


class MemorySystem:
    '''记忆系统'''
    
    def __init__(self):
        self.items: list[dict] = []
    
    def add(self, content: str, role: str):
        self.items.append({
            "content": content,
            "role": role,
            "timestamp": datetime.now().isoformat()
        })
    
    def search(self, query: str, top_k: int = 3) -> list[dict]:
        query_lower = query.lower()
        return [
            item for item in self.items
            if query_lower in item["content"].lower()
        ][:top_k]


class GuardrailsManager:
    '''安全护栏'''
    
    def check_input(self, text: str) -> tuple[bool, str]:
        dangerous = ["ignore previous", "you are now"]
        for pattern in dangerous:
            if pattern in text.lower():
                return False, "输入被阻止"
        return True, text
    
    def check_output(self, text: str) -> tuple[bool, str]:
        return True, text  # 简化处理


class AgentMonitor:
    '''监控器'''
    
    def __init__(self):
        self.metrics: list[dict] = []
    
    def record(self, name: str, value: float):
        self.metrics.append({
            "name": name,
            "value": value,
            "timestamp": datetime.now().isoformat()
        })


class AIRuntime:
    '''AI Assistant Runtime'''
    
    def __init__(self, config: AgentConfig = None):
        self.config = config or AgentConfig()
        self.memory = MemorySystem()
        self.safety = GuardrailsManager()
        self.monitor = AgentMonitor()
        self.tools: dict[str, Callable] = {}
    
    def register_tool(self, name: str, func: Callable):
        self.tools[name] = func
    
    async def run(self, user_input: str) -> str:
        '''运行'''
        # 输入检查
        is_safe, msg = self.safety.check_input(user_input)
        if not is_safe:
            return msg
        
        # 添加到记忆
        self.memory.add(user_input, "user")
        
        # 检索记忆
        memories = self.memory.search(user_input)
        
        # 处理（简化）
        response = f"AI: 基于您的输入 '{user_input[:20]}...'，这是我的回答。"
        
        # 输出检查
        is_safe, response = self.safety.check_output(response)
        
        # 添加到记忆
        self.memory.add(response, "assistant")
        
        # 记录指标
        self.monitor.record("interaction", 1)
        
        return response
    
    def get_status(self) -> dict:
        return {
            "name": self.config.name,
            "tools": list(self.tools.keys()),
            "memory_size": len(self.memory.items),
            "interactions": len(self.monitor.metrics)
        }


# 示例工具
async def search_tool(query: str) -> str:
    '''搜索工具'''
    return f"搜索结果: {query}"

def calculator_tool(expression: str) -> str:
    '''计算器工具'''
    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return f"计算结果: {expression} = {result}"
    except Exception as e:
        return f"错误: {e}"


async def main():
    '''演示完整Runtime'''
    print("=" * 60)
    print("🎓 AI Assistant Runtime 毕业演示")
    print("=" * 60)
    
    # 创建Runtime
    runtime = AIRuntime(AgentConfig(name="毕业项目演示"))
    
    # 注册工具
    runtime.register_tool("search", search_tool)
    runtime.register_tool("calculator", calculator_tool)
    
    print(f"\nRuntime状态: {runtime.get_status()}")
    
    # 多轮对话
    conversations = [
        "你好！",
        "什么是Python？",
        "帮我计算 2 + 3 * 4",
        "搜索一下机器学习"
    ]
    
    print("\n多轮对话演示:")
    print("-" * 40)
    
    for user_input in conversations:
        print(f"\n用户: {user_input}")
        response = await runtime.run(user_input)
        print(f"助手: {response}")
    
    # 显示状态
    print("\n" + "=" * 60)
    print("最终状态:")
    status = runtime.get_status()
    for key, value in status.items():
        print(f"  {key}: {value}")
    
    print("\n" + "=" * 60)
    print("🎓 恭喜完成Python 90天Agent工程学习！")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
