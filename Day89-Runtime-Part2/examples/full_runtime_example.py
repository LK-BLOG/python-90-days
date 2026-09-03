'''
Day 89 示例：完整的AI Runtime
'''

import asyncio
from dataclasses import dataclass, field
from typing import Any, Callable
from datetime import datetime


@dataclass
class MemoryItem:
    '''记忆项'''
    content: str
    role: str
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: dict = field(default_factory=dict)


class MemorySystem:
    '''记忆系统'''
    
    def __init__(self, max_items: int = 100):
        self.items: list[MemoryItem] = []
        self.max_items = max_items
    
    def add(self, content: str, role: str, metadata: dict = None):
        '''添加记忆'''
        self.items.append(MemoryItem(
            content=content,
            role=role,
            metadata=metadata or {}
        ))
        
        # 限制大小
        if len(self.items) > self.max_items:
            self.items = self.items[-self.max_items:]
    
    def search(self, query: str, top_k: int = 5) -> list[MemoryItem]:
        '''搜索记忆'''
        query_lower = query.lower()
        
        scored = []
        for item in self.items:
            # 简单的相关性评分
            score = sum(1 for word in query_lower.split() if word in item.content.lower())
            if score > 0:
                scored.append((score, item))
        
        scored.sort(key=lambda x: x[0], reverse=True)
        return [item for _, item in scored[:top_k]]
    
    def get_recent(self, n: int = 10) -> list[MemoryItem]:
        '''获取最近的记忆'''
        return self.items[-n:]


class TaskPlanner:
    '''任务规划器'''
    
    def create_plan(self, goal: str) -> dict:
        '''创建计划'''
        # 简化的计划创建
        return {
            "goal": goal,
            "steps": [
                {"id": 1, "description": f"分析: {goal}"},
                {"id": 2, "description": f"执行: {goal}"},
                {"id": 3, "description": f"验证: {goal}"}
            ]
        }


class AIRuntime:
    '''AI Runtime'''
    
    def __init__(self):
        self.memory = MemorySystem()
        self.planner = TaskPlanner()
        self.tools: dict[str, Callable] = {}
    
    def register_tool(self, name: str, func: Callable):
        '''注册工具'''
        self.tools[name] = func
    
    async def run(self, query: str) -> str:
        '''运行'''
        # 添加到记忆
        self.memory.add(query, "user")
        
        # 检索相关记忆
        relevant = self.memory.search(query)
        
        # 构建上下文
        context = self._build_context(query, relevant)
        
        # 处理
        response = await self._process(context)
        
        # 添加到记忆
        self.memory.add(response, "assistant")
        
        return response
    
    def _build_context(self, query: str, memories: list[MemoryItem]) -> str:
        '''构建上下文'''
        parts = [f"用户问题: {query}"]
        
        if memories:
            parts.append("\n相关记忆:")
            for mem in memories:
                parts.append(f"  - {mem.content}")
        
        return "\n".join(parts)
    
    async def _process(self, context: str) -> str:
        '''处理（简化）'''
        # 这里应该调用LLM
        return f"基于上下文的响应: {context[:50]}..."


async def main():
    '''演示AI Runtime'''
    print("=" * 60)
    print("AI Runtime 演示")
    print("=" * 60)
    
    runtime = AIRuntime()
    
    # 多轮对话
    queries = [
        "什么是Python？",
        "如何学习Python？",
        "推荐一些Python库"
    ]
    
    for query in queries:
        print(f"\n用户: {query}")
        response = await runtime.run(query)
        print(f"助手: {response}")
    
    # 显示记忆
    print("\n记忆:")
    for mem in runtime.memory.get_recent(5):
        print(f"  [{mem.role}] {mem.content[:50]}...")
    
    print("\n" + "=" * 60)
    print("演示完成！")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
