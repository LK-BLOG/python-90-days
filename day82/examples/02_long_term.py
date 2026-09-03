# Day 82 示例 2: 简单向量存储
import json, hashlib, re
from pathlib import Path

class SimpleVectorStore:
    def __init__(self, db_path='memory_db.json'):
        self.db_path = Path(db_path)
        self.entries = {}
        self._load()
    
    def _load(self):
        if self.db_path.exists():
            self.entries = json.loads(self.db_path.read_text())
    
    def _save(self):
        self.db_path.write_text(json.dumps(self.entries, ensure_ascii=False))
    
    def _embed(self, text):
        words = re.findall(r'\w+', text.lower())
        vocab = list(set(words))[:100]
        vec = [words.count(w)/max(len(words),1) for w in vocab]
        vec.extend([0.0]*(100-len(vec)))
        return vec[:100]
    
    def _similarity(self, a, b):
        dot = sum(x*y for x,y in zip(a,b))
        na = sum(x**2 for x in a)**0.5
        nb = sum(x**2 for x in b)**0.5
        return dot/(na*nb) if na and nb else 0
    
    def store(self, text, metadata=None):
        key = hashlib.md5(text.encode()).hexdigest()
        self.entries[key] = {'text': text, 'embedding': self._embed(text), 'meta': metadata or {}}
        self._save()
    
    def query(self, query_text, top_k=3):
        q_vec = self._embed(query_text)
        results = []
        for e in self.entries.values():
            score = self._similarity(q_vec, e['embedding'])
            results.append({'text': e['text'], 'score': score})
        results.sort(key=lambda x: x['score'], reverse=True)
        return results[:top_k]

if __name__ == '__main__':
    store = SimpleVectorStore('/tmp/test_mem.json')
    store.store('Python是一种编程语言')
    store.store('Java也是一种编程语言')
    store.store('今天天气很好')
    print(store.query('编程'))
    import os; os.remove('/tmp/test_mem.json')
