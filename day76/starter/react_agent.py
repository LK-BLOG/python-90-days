# Day 76 骨架代码 - ReAct Agent
\"\"\"
你的任务：实现一个基础的 ReAct Agent
不要看 examples 里的答案，自己动手写！
\"\"\"
import re
from typing import Callable


class Tool:
    \"\"\"工具类\"\"\"
    def __init__(self, name: str, description: str, func: Callable):
        self.name = name
        self.description = description
        self.func = func
    
    def execute(self, **kwargs) -> str:
        # TODO: 执行工具函数，捕获异常
        pass


class ReActAgent:
    \"\"\"ReAct Agent\"\"\"
    
    def __init__(self, tools: list[Tool], max_steps: int = 10):
        # TODO: 初始化工具字典和步数限制
        pass
    
    def build_prompt(self, query: str, history: list) -> str:
        \"\"\"构建包含工具描述和历史的 prompt\"\"\"
        # TODO: 
        # 1. 生成工具描述列表
        # 2. 拼接历史记录
        # 3. 返回完整 prompt
        pass
    
    def parse_response(self, response: str) -> dict:
        \"\"\"解析 LLM 响应\"\"\"
        # TODO: 解析 Thought 和 Action
        # 返回格式: {"thought": "...", "action": {"type": "finish/tool", ...}}
        pass
    
    def run(self, query: str) -> str:
        \"\"\"ReAct 主循环\"\"\"
        # TODO: 实现完整循环
        # 1. 构建 prompt
        # 2. 循环直到完成或达到最大步数
        # 3. 每步: 思考 → 行动 → 观察
        pass


# 测试
if __name__ == "__main__":
    tools = [
        Tool("calc", "数学计算", lambda expression: str(eval(expression))),
    ]
    agent = ReActAgent(tools)
    print(agent.run("1+1等于几"))
