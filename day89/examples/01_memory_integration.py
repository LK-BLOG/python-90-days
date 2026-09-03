# Day 89 示例 1: Memory 集成
from collections import deque
import json, hashlib
from pathlib import Path

class MemoryManager:
    def __init__(self, size=50):
        self.short_term = deque(maxlen=size)
        self.long_term = {}
        self.working = {}
    
    def add_message(self, role, content):
        self.short_term.append({'role': role, 'content': content})
    
    def get_messages(self, last_n=None):
        msgs = list(self.short_term)
        return msgs[-last_n:] if last_n else msgs
    
    def search(self, query):
        return [m for m in self.short_term if query.lower() in m.get('content','').lower()]
    
    def store_important(self, content, key=None):
        key = key or hashlib.md5(content.encode()).hexdigest()[:8]
        self.long_term[key] = content
    
    def get_context(self):
        recent = self.get_messages(5)
        return '\\n'.join([f'[{m["role"]}]: {m["content"][:60]}' for m in recent])

if __name__ == '__main__':
    mem = MemoryManager()
    mem.add_message('user', '搜索Python')
    mem.add_message('assistant', '找到相关结果')
    mem.store_important('Python是编程语言', 'python_def')
    print(f'上下文:\\n{mem.get_context()}')
    print(f'搜索"Python": {mem.search("Python")}')
