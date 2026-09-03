# Day 82 课程：Memory 系统

## 1. 短期记忆（对话历史）

`python
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from collections import deque


@dataclass
class MemoryItem:
    '''记忆项'''
    content: str
    role: str  # "user", "assistant", "system"
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: dict = field(default_factory=dict)
    importance: float = 0.5  # 重要性评分 0-1


class ShortTermMemory:
    '''短期记忆（对话历史）'''
    
    def __init__(self, max_items: int = 50):
        self.max_items = max_items
        self.items: deque[MemoryItem] = deque(maxlen=max_items)
    
    def add(self, content: str, role: str, metadata: dict = None):
        '''添加记忆'''
        item = MemoryItem(
            content=content,
            role=role,
            metadata=metadata or {}
        )
        self.items.append(item)
    
    def get_recent(self, n: int = 10) -> list[MemoryItem]:
        '''获取最近n条记忆'''
        return list(self.items)[-n:]
    
    def get_by_role(self, role: str) -> list[MemoryItem]:
        '''按角色获取记忆'''
        return [item for item in self.items if item.role == role]
    
    def search(self, query: str) -> list[MemoryItem]:
        '''简单搜索'''
        query_lower = query.lower()
        return [
            item for item in self.items
            if query_lower in item.content.lower()
        ]
    
    def clear(self):
        '''清除记忆'''
        self.items.clear()
    
    def to_prompt(self, n: int = 10) -> str:
        '''转换为提示格式'''
        recent = self.get_recent(n)
        lines = []
        for item in recent:
            lines.append(f"{item.role}: {item.content}")
        return "\n".join(lines)
`

## 2. 长期记忆（向量存储）

`python
import numpy as np
from typing import Optional
import json
import os


class SimpleVectorStore:
    '''简单的向量存储'''
    
    def __init__(self, dimension: int = 384):
        self.dimension = dimension
        self.vectors: list[np.ndarray] = []
        self.metadata: list[dict] = []
    
    def add(self, vector: np.ndarray, metadata: dict):
        '''添加向量'''
        if vector.shape[0] != self.dimension:
            raise ValueError(f"向量维度错误: {vector.shape[0]} != {self.dimension}")
        
        self.vectors.append(vector)
        self.metadata.append(metadata)
    
    def search(
        self, 
        query_vector: np.ndarray, 
        top_k: int = 5
    ) -> list[dict]:
        '''搜索相似向量'''
        if not self.vectors:
            return []
        
        # 计算余弦相似度
        similarities = []
        query_norm = query_vector / np.linalg.norm(query_vector)
        
        for i, vector in enumerate(self.vectors):
            vector_norm = vector / np.linalg.norm(vector)
            similarity = np.dot(query_norm, vector_norm)
            similarities.append((similarity, i))
        
        # 排序并返回top-k
        similarities.sort(reverse=True, key=lambda x: x[0])
        
        results = []
        for score, idx in similarities[:top_k]:
            results.append({
                "score": float(score),
                "metadata": self.metadata[idx]
            })
        
        return results
    
    def save(self, path: str):
        '''保存到文件'''
        data = {
            "dimension": self.dimension,
            "vectors": [v.tolist() for v in self.vectors],
            "metadata": self.metadata
        }
        with open(path, 'w') as f:
            json.dump(data, f)
    
    def load(self, path: str):
        '''从文件加载'''
        with open(path, 'r') as f:
            data = json.load(f)
        
        self.dimension = data["dimension"]
        self.vectors = [np.array(v) for v in data["vectors"]]
        self.metadata = data["metadata"]


class LongTermMemory:
    '''长期记忆'''
    
    def __init__(self, embedding_provider=None):
        self.vector_store = SimpleVectorStore()
        self.embedding_provider = embedding_provider or self._default_embedding
        self.memories: list[dict] = []
    
    def _default_embedding(self, text: str) -> np.ndarray:
        '''默认的嵌入函数（模拟）'''
        # 实际使用时替换为真实的嵌入模型
        np.random.seed(hash(text) % 2**32)
        return np.random.randn(self.vector_store.dimension)
    
    def store(self, content: str, metadata: dict = None):
        '''存储记忆'''
        # 生成嵌入
        embedding = self.embedding_provider(content)
        
        # 存储
        memory_metadata = {
            "content": content,
            "timestamp": datetime.now().isoformat(),
            **(metadata or {})
        }
        
        self.vector_store.add(embedding, memory_metadata)
        self.memories.append(memory_metadata)
    
    def retrieve(self, query: str, top_k: int = 5) -> list[dict]:
        '''检索相关记忆'''
        query_embedding = self.embedding_provider(query)
        return self.vector_store.search(query_embedding, top_k)
    
    def save(self, path: str):
        '''保存记忆'''
        self.vector_store.save(path)
    
    def load(self, path: str):
        '''加载记忆'''
        self.vector_store.load(path)
        self.memories = self.vector_store.metadata.copy()
`

## 3. 工作记忆（当前任务状态）

`python
from enum import Enum


class TaskState(Enum):
    '''任务状态'''
    IDLE = "idle"
    PLANNING = "planning"
    EXECUTING = "executing"
    WAITING = "waiting"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class WorkingMemory:
    '''工作记忆'''
    current_task: str | None = None
    task_state: TaskState = TaskState.IDLE
    context: dict = field(default_factory=dict)
    variables: dict = field(default_factory=dict)
    scratch_pad: list[str] = field(default_factory=list)
    
    def set_task(self, task: str, state: TaskState = TaskState.PLANNING):
        '''设置当前任务'''
        self.current_task = task
        self.task_state = state
    
    def update_state(self, state: TaskState):
        '''更新状态'''
        self.task_state = state
    
    def set_variable(self, key: str, value: Any):
        '''设置变量'''
        self.variables[key] = value
    
    def get_variable(self, key: str, default: Any = None) -> Any:
        '''获取变量'''
        return self.variables.get(key, default)
    
    def add_note(self, note: str):
        '''添加便签'''
        self.scratch_pad.append(note)
    
    def clear(self):
        '''清除工作记忆'''
        self.current_task = None
        self.task_state = TaskState.IDLE
        self.context.clear()
        self.variables.clear()
        self.scratch_pad.clear()
    
    def to_dict(self) -> dict:
        '''转换为字典'''
        return {
            "current_task": self.current_task,
            "task_state": self.task_state.value,
            "context": self.context,
            "variables": self.variables,
            "scratch_pad": self.scratch_pad
        }
`

## 4. 记忆检索与遗忘

`python
class MemoryRetriever:
    '''记忆检索器'''
    
    def __init__(self, short_term: ShortTermMemory, long_term: LongTermMemory):
        self.short_term = short_term
        self.long_term = long_term
    
    def retrieve(self, query: str, top_k: int = 10) -> list[dict]:
        '''检索相关记忆'''
        results = []
        
        # 从短期记忆检索
        short_results = self.short_term.search(query)
        for item in short_results:
            results.append({
                "content": item.content,
                "source": "short_term",
                "score": 1.0,  # 短期记忆优先级高
                "timestamp": item.timestamp
            })
        
        # 从长期记忆检索
        long_results = self.long_term.retrieve(query, top_k=top_k)
        for item in long_results:
            results.append({
                "content": item["metadata"]["content"],
                "source": "long_term",
                "score": item["score"],
                "timestamp": item["metadata"]["timestamp"]
            })
        
        # 排序
        results.sort(key=lambda x: x["score"], reverse=True)
        
        return results[:top_k]


class ForgettingStrategy:
    '''遗忘策略'''
    
    def __init__(self, decay_rate: float = 0.1):
        self.decay_rate = decay_rate
    
    def calculate_importance(
        self, 
        memory: dict, 
        current_time: datetime = None
    ) -> float:
        '''计算记忆重要性'''
        if current_time is None:
            current_time = datetime.now()
        
        # 时间衰减
        timestamp = datetime.fromisoformat(memory["timestamp"])
        time_diff = (current_time - timestamp).total_seconds() / 3600  # 小时
        time_decay = 1.0 / (1.0 + self.decay_rate * time_diff)
        
        # 访问频率（简化）
        access_count = memory.get("access_count", 1)
        frequency_boost = min(access_count / 10, 1.0)
        
        # 综合评分
        importance = 0.5 * time_decay + 0.5 * frequency_boost
        
        return importance
    
    def should_forget(self, memory: dict) -> bool:
        '''是否应该遗忘'''
        importance = self.calculate_importance(memory)
        return importance < 0.2
`

## 5. MemGPT基础

`python
class MemGPTStyleMemory:
    '''MemGPT风格的记忆系统'''
    
    def __init__(self, max_core_memory: int = 10, max_archival: int = 1000):
        self.core_memory: list[dict] = []  # 核心记忆（始终在上下文中）
        self.archival_memory: list[dict] = []  # 归档记忆（可检索）
        self.max_core = max_core_memory
        self.max_archival = max_archival
    
    def add_core_memory(self, content: str, category: str = "general"):
        '''添加核心记忆'''
        if len(self.core_memory) >= self.max_core:
            # 移动到归档
            oldest = self.core_memory.pop(0)
            self.archival_memory.append(oldest)
        
        self.core_memory.append({
            "content": content,
            "category": category,
            "type": "core"
        })
    
    def add_archival_memory(self, content: str):
        '''添加归档记忆'''
        if len(self.archival_memory) >= self.max_archival:
            self.archival_memory.pop(0)  # 删除最旧的
        
        self.archival_memory.append({
            "content": content,
            "type": "archival"
        })
    
    def search(self, query: str, top_k: int = 5) -> list[dict]:
        '''搜索记忆'''
        # 简单的关键词匹配
        results = []
        
        # 先搜索核心记忆
        for mem in self.core_memory:
            if query.lower() in mem["content"].lower():
                results.append({**mem, "score": 1.0})
        
        # 再搜索归档记忆
        for mem in self.archival_memory:
            if query.lower() in mem["content"].lower():
                results.append({**mem, "score": 0.5})
        
        # 排序
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_k]
    
    def get_context_string(self) -> str:
        '''获取上下文字符串'''
        lines = ["核心记忆:"]
        for mem in self.core_memory:
            lines.append(f"  - [{mem['category']}] {mem['content']}")
        return "\n".join(lines)
`

## 6. 完整的多层记忆系统

`python
class MultiLayerMemory:
    '''多层记忆系统'''
    
    def __init__(self):
        self.short_term = ShortTermMemory(max_items=50)
        self.working = WorkingMemory()
        self.long_term = LongTermMemory()
        self.retriever = MemoryRetriever(self.short_term, self.long_term)
        self.forgetting = ForgettingStrategy()
    
    def add_conversation(self, role: str, content: str):
        '''添加对话记忆'''
        self.short_term.add(content, role)
    
    def store_knowledge(self, content: str, metadata: dict = None):
        '''存储知识到长期记忆'''
        self.long_term.store(content, metadata)
    
    def recall(self, query: str, top_k: int = 5) -> list[dict]:
        '''回忆相关记忆'''
        return self.retriever.retrieve(query, top_k)
    
    def set_task(self, task: str):
        '''设置当前任务'''
        self.working.set_task(task)
    
    def update_task_state(self, state: TaskState):
        '''更新任务状态'''
        self.working.update_state(state)
    
    def get_memory_summary(self) -> dict:
        '''获取记忆摘要'''
        return {
            "short_term_count": len(self.short_term.items),
            "long_term_count": len(self.long_term.memories),
            "current_task": self.working.current_task,
            "task_state": self.working.task_state.value
        }
`

## 7. 本日总结

- ShortTermMemory管理对话历史
- LongTermMemory使用向量存储
- WorkingMemory跟踪任务状态
- MemoryRetriever实现跨层检索
- ForgettingStrategy管理记忆遗忘

明天我们将学习State & Checkpoint系统。
