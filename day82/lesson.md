# Day 82: Memory 系统

## 1. 记忆系统的三大层次

`
┌─────────────────────────────────┐
│         Working Memory          │  ← 当前任务上下文
│    (当前对话 + 工具结果)          │
├─────────────────────────────────┤
│        Short-Term Memory        │  ← 对话历史
│     (最近N轮对话记录)             │
├─────────────────────────────────┤
│        Long-Term Memory         │  ← 跨对话持久化
│  (向量数据库 + 知识图谱)          │
└─────────────────────────────────┘
`

### 1.1 短期记忆（对话历史）

`python
from collections import deque
from typing import List, Dict, Optional
import time


class ShortTermMemory:
    \"\"\"短期记忆 - 对话历史管理\"\"\"
    
    def __init__(self, max_messages: int = 100, max_tokens: int = 8000):
        self.messages: deque = deque(maxlen=max_messages)
        self.max_tokens = max_tokens
        self.metadata: List[Dict] = []
    
    def add(self, role: str, content: str, **meta):
        msg = {"role": role, "content": content, "timestamp": time.time()}
        self.messages.append(msg)
        self.metadata.append(meta)
    
    def get_messages(self, last_n: Optional[int] = None) -> List[Dict]:
        msgs = list(self.messages)
        if last_n:
            msgs = msgs[-last_n:]
        return msgs
    
    def search(self, keyword: str) -> List[Dict]:
        return [m for m in self.messages if keyword in m.get("content", "")]
    
    def get_context_window(self) -> str:
        \"\"\"将记忆格式化为上下文\"\"\"
        messages = self.get_messages(last_n=20)
        context = ""
        for msg in messages:
            role = msg["role"]
            content = msg["content"][:200]  # 截断
            context += f"[{role}]: {content}\n"
        return context
    
    def clear(self):
        self.messages.clear()
        self.metadata.clear()
`

### 1.2 长期记忆（向量存储）

`python
import json
import hashlib
from typing import List, Dict, Tuple
from pathlib import Path


class EmbeddingCache:
    \"\"\"简单的向量缓存（模拟向量数据库）\"\"\"
    
    def __init__(self, db_path: str = "./memory_db.json"):
        self.db_path = Path(db_path)
        self.entries: Dict[str, Dict] = {}
        self._load()
    
    def _load(self):
        if self.db_path.exists():
            self.entries = json.loads(self.db_path.read_text(encoding="utf-8"))
    
    def _save(self):
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.db_path.write_text(json.dumps(self.entries, ensure_ascii=False, indent=2))
    
    def _hash(self, text: str) -> str:
        return hashlib.md5(text.encode()).hexdigest()
    
    def _simple_embedding(self, text: str) -> List[float]:
        \"\"\"简单的词频向量（实际中用模型生成）\"\"\"
        import re
        words = re.findall(r'\w+', text.lower())
        vocab = list(set(words))
        vec = [words.count(w) / max(len(words), 1) for w in vocab[:100]]
        # 补齐到100维
        vec.extend([0.0] * (100 - len(vec)))
        return vec[:100]
    
    def _cosine_similarity(self, a: List[float], b: List[float]) -> float:
        \"\"\"余弦相似度\"\"\"
        dot = sum(x * y for x, y in zip(a, b))
        norm_a = sum(x ** 2 for x in a) ** 0.5
        norm_b = sum(x ** 2 for x in b) ** 0.5
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return dot / (norm_a * norm_b)
    
    def store(self, text: str, metadata: dict = None):
        \"\"\"存储记忆\"\"\"
        key = self._hash(text)
        self.entries[key] = {
            "text": text,
            "embedding": self._simple_embedding(text),
            "metadata": metadata or {},
            "timestamp": time.time()
        }
        self._save()
    
    def query(self, query_text: str, top_k: int = 5) -> List[Dict]:
        \"\"\"查询相似记忆\"\"\"
        query_vec = self._simple_embedding(query_text)
        
        results = []
        for key, entry in self.entries.items():
            sim = self._cosine_similarity(query_vec, entry["embedding"])
            results.append({
                "text": entry["text"],
                "score": sim,
                "metadata": entry["metadata"]
            })
        
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_k]
`

## 2. 工作记忆

`python
class WorkingMemory:
    \"\"\"工作记忆 - 当前任务的临时存储\"\"\"
    
    def __init__(self):
        self.variables: Dict[str, any] = {}
        self.stack: List[Dict] = []  # 嵌套上下文栈
        self.current_goal: str = ""
        self.intermediate_results: List[any] = []
    
    def set(self, key: str, value: any):
        self.variables[key] = value
    
    def get(self, key: str, default=None):
        return self.variables.get(key, default)
    
    def push_context(self, context_name: str):
        \"\"\"压入新的上下文层\"\"\"
        self.stack.append(dict(self.variables))
    
    def pop_context(self):
        \"\"\"弹出上下文层\"\"\"
        if self.stack:
            self.variables = self.stack.pop()
    
    def set_goal(self, goal: str):
        self.current_goal = goal
        self.intermediate_results = []
    
    def add_result(self, result: any):
        self.intermediate_results.append(result)
    
    def summarize(self) -> str:
        \"\"\"总结当前工作记忆\"\"\"
        parts = [f"当前目标: {self.current_goal}"]
        
        if self.variables:
            parts.append(f"变量: {list(self.variables.keys())}")
        
        if self.intermediate_results:
            parts.append(f"中间结果: {len(self.intermediate_results)} 个")
        
        return "\n".join(parts)
`

## 3. 统一记忆系统

`python
class MemorySystem:
    \"\"\"统一记忆系统\"\"\"
    
    def __init__(self):
        self.short_term = ShortTermMemory()
        self.long_term = EmbeddingCache()
        self.working = WorkingMemory()
    
    def remember(self, role: str, content: str, important: bool = False):
        \"\"\"存储一条记忆\"\"\"
        # 短期记忆
        self.short_term.add(role, content)
        
        # 如果重要，存入长期记忆
        if important:
            self.long_term.store(content, {"role": role})
    
    def recall(self, query: str, scope: str = "all") -> List:
        \"\"\"回忆相关信息\"\"\"
        results = []
        
        if scope in ("all", "short"):
            # 在短期记忆中搜索
            short_results = self.short_term.search(query)
            results.extend([{"text": m["content"], "source": "short"} for m in short_results])
        
        if scope in ("all", "long"):
            # 在长期记忆中搜索
            long_results = self.long_term.query(query, top_k=5)
            results.extend([{"text": r["text"], "source": "long", "score": r["score"]} for r in long_results])
        
        return results
    
    def get_context(self) -> str:
        \"\"\"获取记忆上下文\"\"\"
        parts = []
        
        # 工作记忆
        if self.working.current_goal:
            parts.append(f"[工作记忆] {self.working.summarize()}")
        
        # 最近对话
        recent = self.short_term.get_messages(last_n=5)
        if recent:
            history = "\n".join([f"  [{m['role']}]: {m['content'][:80]}" for m in recent])
            parts.append(f"[短期记忆] 最近对话:\n{history}")
        
        return "\n\n".join(parts)
    
    def forget(self, scope: str = "all"):
        \"\"\"清除记忆\"\"\"
        if scope in ("all", "short"):
            self.short_term.clear()
        if scope in ("all", "working"):
            self.working = WorkingMemory()
`

## 4. MemGPT 概念

### 4.1 核心思想

MemGPT 的核心是：像操作系统的虚拟内存一样管理 LLM 的上下文：

`
┌───────────────────────────────────────┐
│              Main Context             │  ← LLM 直接访问
│  (System Prompt + 工作集 + 最近消息)   │
├───────────────────────────────────────┤
│           archival storage             │  ← 需要时检索
│     (向量数据库, 所有历史记忆)          │
├───────────────────────────────────────┤
│            recall storage              │  ← 对话历史
│         (所有对话记录)                  │
└───────────────────────────────────────┘
`

### 4.2 简化版 MemGPT

`python
class SimpleMemGPT:
    \"\"\"简化版 MemGPT - 模拟虚拟内存管理\"\"\"
    
    def __init__(self, main_context_size: int = 10):
        self.main_context: List[Dict] = []  # 主上下文（类似 RAM）
        self.archival: List[Dict] = []      # 归档存储（类似磁盘）
        self.context_size = main_context_size
    
    def user_message(self, content: str) -> str:
        \"\"\"处理用户消息\"\"\"
        self.main_context.append({"role": "user", "content": content})
        return self._run_agent_step()
    
    def _run_agent_step(self) -> str:
        \"\"\"Agent 执行一步\"\"\"
        # 检查是否需要内存管理
        if len(self.main_context) > self.context_size:
            self._memory_pressure()
        
        # 模拟 LLM 响应
        response = f"处理了 {len(self.main_context)} 条消息"
        self.main_context.append({"role": "assistant", "content": response})
        
        return response
    
    def _memory_pressure(self):
        \"\"\"内存压力时，将旧消息移到归档\"\"\"
        # 保留最近的消息
        keep = self.main_context[-5:]
        archive = self.main_context[:-5]
        
        # 移到归档
        self.archival.extend(archive)
        
        # 主上下文只保留摘要 + 最近消息
        summary = f"归档了 {len(archive)} 条消息到长期存储"
        self.main_context = [
            {"role": "system", "content": summary}
        ] + keep
    
    def search_archival(self, query: str) -> List[Dict]:
        \"\"\"从归档中检索\"\"\"
        return [m for m in self.archival if query in m.get("content", "")]
    
    def core_memory_append(self, content: str):
        \"\"\"追加到核心记忆（永不删除）\"\"\"
        self.main_context.insert(0, {"role": "core_memory", "content": content})
    
    def context_size(self) -> Dict:
        return {
            "main": len(self.main_context),
            "archival": len(self.archival),
        }
`

## 5. 常见错误

1. **短期记忆无限增长** → 设置 max_messages 和滑动窗口
2. **长期记忆噪音太多** → 设置重要性阈值
3. **工作记忆污染** → 用 push/pop 管理上下文层
4. **检索不精确** → 改进 embedding 模型或加 Reranker
5. **没有遗忘机制** → 过时的记忆应该被清理

## 6. 动手练习

### 练习 1：实现短期记忆管理
### 练习 2：实现简单向量存储
### 练习 3：实现统一记忆系统
