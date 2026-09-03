# Day 82 示例 1: 短期记忆
from collections import deque
import time

class ShortTermMemory:
    def __init__(self, max_messages=100):
        self.messages = deque(maxlen=max_messages)
    def add(self, role, content):
        self.messages.append({'role': role, 'content': content, 'time': time.time()})
    def get_messages(self, last_n=None):
        msgs = list(self.messages)
        return msgs[-last_n:] if last_n else msgs
    def search(self, keyword):
        return [m for m in self.messages if keyword in m.get('content','')]
    def clear(self):
        self.messages.clear()

if __name__ == '__main__':
    mem = ShortTermMemory(max_messages=10)
    mem.add('user', '你好')
    mem.add('assistant', '你好！')
    mem.add('user', '搜索Python')
    print(f'全部: {mem.get_messages()}')
    print(f'搜索: {mem.search("Python")}')
    print(f'最近2条: {mem.get_messages(2)}')
