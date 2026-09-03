'''
Day 82 示例：多层记忆系统
'''

from dataclasses import dataclass, field
from datetime import datetime
from collections import deque
from typing import Any


class ShortTermMemory:
    '''短期记忆'''
    
    def __init__(self, max_items: int = 50):
        self.items: deque = deque(maxlen=max_items)
    
    def add(self, content: str, role: str):
        self.items.append({
            "content": content,
            "role": role,
            "timestamp": datetime.now()
        })
    
    def get_recent(self, n: int = 10):
        return list(self.items)[-n:]
    
    def search(self, query: str):
        query_lower = query.lower()
        return [item for item in self.items if query_lower in item["content"].lower()]


class WorkingMemory:
    '''工作记忆'''
    
    def __init__(self):
        self.current_task: str | None = None
        self.variables: dict = {}
        self.notes: list[str] = []
    
    def set_task(self, task: str):
        self.current_task = task
    
    def set_variable(self, key: str, value: Any):
        self.variables[key] = value
    
    def add_note(self, note: str):
        self.notes.append(note)


class LongTermMemory:
    '''长期记忆（简化版）'''
    
    def __init__(self):
        self.memories: list[dict] = []
    
    def store(self, content: str, metadata: dict = None):
        self.memories.append({
            "content": content,
            "metadata": metadata or {},
            "timestamp": datetime.now()
        })
    
    def search(self, query: str, top_k: int = 5):
        query_lower = query.lower()
        results = []
        
        for mem in self.memories:
            if query_lower in mem["content"].lower():
                results.append(mem)
        
        return results[:top_k]


def main():
    '''演示记忆系统'''
    print("=" * 60)
    print("多层记忆系统演示")
    print("=" * 60)
    
    # 创建记忆系统
    short_term = ShortTermMemory()
    working = WorkingMemory()
    long_term = LongTermMemory()
    
    # 模拟对话
    print("\n1. 短期记忆（对话历史）:")
    conversations = [
        ("user", "什么是Python？"),
        ("assistant", "Python是一种流行的编程语言。"),
        ("user", "如何学习Python？"),
        ("assistant", "可以通过在线课程和实践项目来学习。")
    ]
    
    for role, content in conversations:
        short_term.add(content, role)
        print(f"  {role}: {content}")
    
    print("\n  最近的对话:")
    for item in short_term.get_recent(3):
        print(f"    {item['role']}: {item['content']}")
    
    # 工作记忆
    print("\n2. 工作记忆（任务状态）:")
    working.set_task("学习Python基础")
    working.set_variable("progress", "30%")
    working.add_note("需要完成第5章练习")
    
    print(f"  当前任务: {working.current_task}")
    print(f"  进度: {working.variables.get('progress')}")
    print(f"  便签: {working.notes}")
    
    # 长期记忆
    print("\n3. 长期记忆（知识库）:")
    knowledge = [
        "Python是Guido van Rossum在1991年创造的。",
        "Python支持面向对象、函数式和过程式编程。",
        "Python的主要特点包括简洁、易读、丰富库支持。"
    ]
    
    for k in knowledge:
        long_term.store(k, {"type": "knowledge"})
        print(f"  存储: {k[:30]}...")
    
    # 检索
    print("\n  搜索'编程':")
    results = long_term.search("编程")
    for r in results:
        print(f"    - {r['content'][:50]}...")
    
    print("\n" + "=" * 60)
    print("演示完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
