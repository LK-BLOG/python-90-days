# Day 81: Memory System — 完整知识点

## 1. 记忆系统概述

Agent的记忆系统模仿人类记忆的三层结构：
```
┌─────────────────────────────────────┐
│ 短期记忆 (Short-term Memory)        │ ← 当前对话历史
│ 保留在上下文窗口中，会话结束即丢失    │
├─────────────────────────────────────┤
│ 工作记忆 (Working Memory)           │ ← 当前任务状态
│ Agent正在处理的任务信息，跨轮保持     │
├─────────────────────────────────────┤
│ 长期记忆 (Long-term Memory)         │ ← 持久化存储
│ 向量数据库/知识图谱，跨会话保持       │
└─────────────────────────────────────┘
```

## 2. 短期记忆：对话历史管理

```python
from typing import List, Dict, Optional
from datetime import datetime, timedelta

class ConversationMemory:
    """短期记忆：管理当前会话的对话历史"""

    def __init__(self, max_turns: int = 50, max_tokens: int = 8000):
        self.max_turns = max_turns
        self.max_tokens = max_tokens
        self.messages: List[Dict] = []
        self.metadata: List[Dict] = []

    def add(self, role: str, content: str, **kwargs):
        """添加一条消息"""
        msg = {"role": role, "content": content, **kwargs}
        self.messages.append(msg)
        self.metadata.append({
            "timestamp": datetime.now().isoformat(),
            "token_estimate": len(content) // 3,
            "importance": kwargs.get("importance", 0.5)
        })
        self._trim()

    def _trim(self):
        """自动裁剪"""
        # 按轮次裁剪
        while len(self.messages) > self.max_turns:
            self.messages.pop(0)
            self.metadata.pop(0)
        # 按Token裁剪
        total = sum(m["token_estimate"] for m in self.metadata)
        while total > self.max_tokens and len(self.messages) > 1:
            removed = self.metadata.pop(0)
            self.messages.pop(0)
            total -= removed["token_estimate"]

    def search(self, keyword: str) -> List[Dict]:
        """关键词搜索历史消息"""
        return [m for m in self.messages if keyword in m.get("content", "")]

    def get_recent(self, n: int = 5) -> List[Dict]:
        """获取最近n轮对话"""
        return self.messages[-n*2:]  # 每轮=2条(user+assistant)

    def get_messages(self) -> List[Dict]:
        return self.messages.copy()

    def clear(self):
        self.messages.clear()
        self.metadata.clear()
```

## 3. 长期记忆：向量存储

### 3.1 向量相似度计算

```python
import math
from typing import List

def cosine_similarity(a: List[float], b: List[float]) -> float:
    """余弦相似度"""
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)

def simple_embedding(text: str, dim: int = 128) -> List[float]:
    """简易文本嵌入（基于字符频率的哈希）"""
    import hashlib
    vec = [0.0] * dim
    for i, char in enumerate(text):
        h = int(hashlib.md5(f"{char}{i}".encode()).hexdigest(), 16)
        idx = h % dim
        vec[idx] += 1.0
        # 归一化
    norm = math.sqrt(sum(x * x for x in vec))
    if norm > 0:
        vec = [x / norm for x in vec]
    return vec
```

### 3.2 向量存储

```python
class VectorStore:
    """简易向量数据库"""

    def __init__(self, dimension: int = 128):
        self.dimension = dimension
        self.vectors: List[List[float]] = []
        self.documents: List[Dict] = []
        self.ids: List[str] = []

    def add(self, doc_id: str, text: str, metadata: Dict = None):
        """添加文档"""
        embedding = simple_embedding(text, self.dimension)
        self.ids.append(doc_id)
        self.vectors.append(embedding)
        self.documents.append({
            "id": doc_id,
            "text": text,
            "metadata": metadata or {}
        })

    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """语义搜索"""
        query_vec = simple_embedding(query, self.dimension)
        scores = []
        for i, vec in enumerate(self.vectors):
            score = cosine_similarity(query_vec, vec)
            scores.append((score, i))
        scores.sort(reverse=True)
        results = []
        for score, idx in scores[:top_k]:
            result = self.documents[idx].copy()
            result["score"] = score
            results.append(result)
        return results

    def delete(self, doc_id: str):
        if doc_id in self.ids:
            idx = self.ids.index(doc_id)
            self.ids.pop(idx)
            self.vectors.pop(idx)
            self.documents.pop(idx)

    def update(self, doc_id: str, text: str, metadata: Dict = None):
        self.delete(doc_id)
        self.add(doc_id, text, metadata)

    def count(self) -> int:
        return len(self.ids)
```

## 4. 知识图谱

```python
from collections import defaultdict
from typing import Set, Tuple

class KnowledgeGraph:
    """简易知识图谱"""

    def __init__(self):
        self.entities: Dict[str, Dict] = {}
        self.edges: List[Tuple[str, str, str, Dict]] = []  # (head, relation, tail, meta)
        self.adjacency: Dict[str, List] = defaultdict(list)  # entity -> [(relation, neighbor)]

    def add_entity(self, name: str, entity_type: str = "generic", **props):
        self.entities[name] = {"type": entity_type, **props}

    def add_relation(self, head: str, relation: str, tail: str, **props):
        self.edges.append((head, relation, tail, props))
        self.adjacency[head].append((relation, tail))
        self.adjacency[tail].append((f"inverse_{relation}", head))

    def get_neighbors(self, entity: str, relation: str = None) -> List[Tuple[str, str]]:
        """获取邻居"""
        if entity not in self.adjacency:
            return []
        if relation:
            return [(r, n) for r, n in self.adjacency[entity] if r == relation]
        return self.adjacency[entity]

    def bfs(self, start: str, max_depth: int = 3) -> Dict[str, int]:
        """广度优先搜索"""
        visited = {start: 0}
        queue = [start]
        while queue:
            current = queue.pop(0)
            depth = visited[current]
            if depth >= max_depth:
                continue
            for _, neighbor in self.adjacency[current]:
                if neighbor not in visited:
                    visited[neighbor] = depth + 1
                    queue.append(neighbor)
        return visited

    def find_path(self, start: str, end: str, max_depth: int = 5) -> Optional[List[str]]:
        """查找两点间路径"""
        if start == end:
            return [start]
        visited = {start}
        queue = [(start, [start])]
        while queue:
            current, path = queue.pop(0)
            if len(path) > max_depth:
                continue
            for _, neighbor in self.adjacency[current]:
                if neighbor == end:
                    return path + [neighbor]
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        return None

    def query_triple(self, head: str = None, relation: str = None, tail: str = None):
        """三元组查询"""
        results = []
        for h, r, t, meta in self.edges:
            if head and h != head:
                continue
            if relation and r != relation:
                continue
            if tail and t != tail:
                continue
            results.append((h, r, t, meta))
        return results
```

## 5. MemGPT模式的记忆管理

MemGPT的核心思想：像操作系统管理内存一样管理LLM的上下文。

```python
class MemGPTMemory:
    """
    MemGPT风格的记忆系统
    - Main Context: 当前上下文窗口（相当于RAM）
    - Archival Storage: 归档存储（相当于磁盘）
    """

    def __init__(self, main_context_size: int = 8000):
        self.main_context_size = main_context_size
        self.main_context: List[Dict] = []  # 主记忆
        self.archival: List[Dict] = []      # 归档记忆
        self.conversation_history: List[Dict] = []  # 对话历史
        self.working_context: Dict = {}     # 工作上下文

    def insert_to_main(self, content: str, source: str = "user"):
        """插入到主记忆"""
        self.main_context.append({
            "type": "memory",
            "content": content,
            "source": source,
            "timestamp": __import__('datetime').datetime.now().isoformat()
        })

    def append_to_archive(self, content: str, metadata: Dict = None):
        """归档到长期存储"""
        self.archival.append({
            "content": content,
            "metadata": metadata or {},
            "timestamp": __import__('datetime').datetime.now().isoformat()
        })

    def search_archive(self, query: str, top_k: int = 3) -> List[Dict]:
        """在归档中搜索"""
        # 简单关键词匹配（实际应用中用向量检索）
        results = []
        for item in self.archival:
            if any(word in item["content"] for word in query.split()):
                results.append(item)
        return results[:top_k]

    def conversation_search(self, query: str) -> List[Dict]:
        """搜索对话历史"""
        results = []
        for msg in self.conversation_history:
            if query.lower() in msg.get("content", "").lower():
                results.append(msg)
        return results

    def core_memory_replace(self, old: str, new: str):
        """替换核心记忆"""
        for ctx in self.main_context:
            if old in ctx["content"]:
                ctx["content"] = ctx["content"].replace(old, new)

    def get_system_prompt(self) -> str:
        """生成包含记忆的系统提示"""
        parts = []
        # 核心记忆
        if self.main_context:
            memories = "\n".join(m["content"] for m in self.main_context)
            parts.append(f"## 核心记忆\n{memories}")
        # 工作上下文
        if self.working_context:
            ctx = "\n".join(f"- {k}: {v}" for k, v in self.working_context.items())
            parts.append(f"## 当前工作\n{ctx}")
        return "\n\n".join(parts)
```

## 6. 实际应用

### 6.1 聊天机器人的记忆
- 短期：当前对话的滑动窗口
- 长期：用户偏好、过往需求的向量存储
- 工作：当前话题、用户情绪状态

### 6.2 RAG中的记忆
- 短期：检索结果缓存
- 长期：知识库（文档向量存储）
- 工作：当前查询的上下文

### 6.3 多Agent协作的记忆
- 共享长期记忆（全局知识）
- 私有短期记忆（各自对话）
- 协作工作记忆（共享任务状态）

## 7. 常见错误
| 错误 | 后果 | 正确做法 |
|------|------|---------|
| 不清理旧记忆 | Token溢出 | 滑动窗口+压缩 |
| 向量维度太低 | 检索不准确 | 至少128维 |
| 不持久化 | 会话间丢失 | 存到文件/数据库 |
| 记忆没有优先级 | 关键信息被丢弃 | 重要性评分 |
| 搜索不分层 | 效率低 | 短期/长期分开搜 |
