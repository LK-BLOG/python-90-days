"""Day 29 starter: Memory系统骨架"""

from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field


class BaseMemory(ABC):
    """Memory基类 —— 策略模式"""
    
    @abstractmethod
    def add(self, role: str, content: str) -> None:
        """添加一条消息"""
        ...
    
    @abstractmethod
    def get_messages(self) -> list[dict]:
        """获取当前消息列表"""
        ...
    
    @abstractmethod
    def clear(self) -> None:
        """清空记忆"""
        ...


class SlidingWindowMemory(BaseMemory):
    """滑动窗口Memory：保留最近N条消息"""
    
    def __init__(self, system_prompt: str = "你是一个有用的助手。", max_messages: int = 20):
        self.system_prompt = system_prompt
        self.max_messages = max_messages
        self._messages: list[dict] = []
    
    def add(self, role: str, content: str) -> None:
        # TODO: 添加消息到历史
        ...
    
    def get_messages(self) -> list[dict]:
        # TODO: 返回system prompt + 最近N条消息
        ...
    
    def clear(self) -> None:
        # TODO: 清空消息
        ...


class TokenAwareMemory(BaseMemory):
    """Token感知Memory：根据token数控制上下文"""
    
    def __init__(self, system_prompt: str = "你是一个有用的助手。", max_tokens: int = 4000):
        self.system_prompt = system_prompt
        self.max_tokens = max_tokens
        self._messages: list[dict] = []
    
    def _estimate_tokens(self, text: str) -> int:
        # TODO: 粗略估计token数
        ...
    
    def add(self, role: str, content: str) -> None:
        ...
    
    def get_messages(self) -> list[dict]:
        # TODO: 从最新消息向前添加，直到token超限
        ...
    
    def clear(self) -> None:
        ...
