# Memory基类
from __future__ import annotations
from abc import ABC, abstractmethod


class BaseMemory(ABC):
    """Memory接口 — 策略模式"""

    @abstractmethod
    def add(self, role: str, content: str) -> None:
        """添加一条消息"""
        ...

    @abstractmethod
    def get_messages(self) -> list[dict]:
        """获取当前消息列表（包含system prompt）"""
        ...

    @abstractmethod
    def clear(self) -> None:
        """清空所有记忆"""
        ...

    def get_token_count(self) -> int:
        """估算当前token数"""
        return sum(len(m.get("content", "")) // 3 for m in self.get_messages())
