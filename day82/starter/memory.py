# Day 82 骨架代码
class ShortTermMemory:
    def __init__(self, max_messages=100):
        pass
    def add(self, role, content): pass
    def get_messages(self, last_n=None): pass
    def search(self, keyword): pass

class SimpleVectorStore:
    def store(self, text, metadata=None): pass
    def query(self, query_text, top_k=3): pass

class MemorySystem:
    def __init__(self):
        pass
    def remember(self, content, important=False): pass
    def recall(self, query): pass
    def get_context(self): pass
