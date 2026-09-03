"""Day 30 - Memory 基类"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional


class BaseMemory(ABC):
    """记忆系统抽象基类"""

    def __init__(self, system_prompt: str = "", max_tokens: int = 4000):
        """初始化

        Args:
            system_prompt: 系统提示词（始终保留）
            max_tokens: 最大 token 限制
        """
        self.system_prompt = system_prompt
        self.max_tokens = max_tokens

    @abstractmethod
    def add(self, role: str, content: str) -> None:
        """添加一条消息"""
        ...

    @abstractmethod
    def get_messages(self) -> list[dict]:
        """获取消息列表（可直接传给 AI）"""
        ...

    @abstractmethod
    def clear(self) -> None:
        """清空历史（保留 system prompt）"""
        ...

    @property
    @abstractmethod
    def token_count(self) -> int:
        """当前 token 估算"""
        ...
