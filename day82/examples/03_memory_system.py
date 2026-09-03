# Day 82 示例 3: 统一记忆系统
class MemorySystem:
    def __init__(self):
        self.short_term = []
        self.long_term = []
        self.working = {}
    
    def remember(self, content, important=False):
        self.short_term.append({'content': content, 'important': important})
        if important:
            self.long_term.append(content)
    
    def recall(self, query):
        results = []
        for m in self.short_term:
            if query in m['content']:
                results.append({'text': m['content'], 'source': 'short'})
        for m in self.long_term:
            if query in m:
                results.append({'text': m, 'source': 'long'})
        return results
    
    def get_context(self):
        recent = self.short_term[-5:]
        return '\n'.join([f"  {m['content'][:80]}" for m in recent])

if __name__ == '__main__':
    mem = MemorySystem()
    mem.remember('用户想要搜索信息')
    mem.remember('使用了搜索工具', important=True)
    mem.remember('找到了结果')
    print(f'回忆"搜索": {mem.recall("搜索")}')
    print(f'上下文:\n{mem.get_context()}')
