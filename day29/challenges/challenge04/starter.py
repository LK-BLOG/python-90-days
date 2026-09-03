"""Challenge 4: Memory系统
实现对话记忆管理。
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field


class BaseMemory(ABC):
    """Memory基类"""
    
    @abstractmethod
    def add(self, role: str, content: str) -> None: ...
    
    @abstractmethod
    def get_messages(self) -> list[dict]: ...
    
    @abstractmethod
    def clear(self) -> None: ...


class SlidingWindowMemory(BaseMemory):
    """滑动窗口：保留最近N条"""
    
    def __init__(self, system_prompt: str = "你是助手。", max_messages: int = 20):
        self.system_prompt = system_prompt
        self.max_messages = max_messages
        self._messages: list[dict] = []
    
    def add(self, role: str, content: str) -> None:
        # TODO
        ...
    
    def get_messages(self) -> list[dict]:
        # TODO: 返回 system + 最近N条
        ...
    
    def clear(self) -> None:
        # TODO
        ...


class TokenAwareMemory(BaseMemory):
    """Token感知：根据估算的token数限制"""
    
    def __init__(self, system_prompt: str = "你是助手。", max_tokens: int = 4000):
        self.system_prompt = system_prompt
        self.max_tokens = max_tokens
        self._messages: list[dict] = []
    
    def _estimate_tokens(self, text: str) -> int:
        # TODO: 粗略估计 (中文~1字/token, 英文~4字符/token)
        ...
    
    def add(self, role: str, content: str) -> None:
        # TODO
        ...
    
    def get_messages(self) -> list[dict]:
        # TODO: 从最新消息向前添加，不超过token限制
        ...
    
    def clear(self) -> None:
        # TODO
        ...


if __name__ == "__main__":
    # 测试
    mem = SlidingWindowMemory(max_messages=5)
    for i in range(10):
        mem.add("user" if i % 2 == 0 else "assistant", f"消息{i}")
    
    messages = mem.get_messages()
    print(f"总消息数: {len(messages)}")
    for m in messages:
        print(f"  [{m['role']}] {m['content']}")
