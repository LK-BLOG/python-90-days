# Challenge 3 Starter: Memory系统

from __future__ import annotations
from abc import ABC, abstractmethod


class BaseMemory(ABC):
    @abstractmethod
    def add(self, role: str, content: str) -> None: ...
    @abstractmethod
    def get_messages(self) -> list[dict]: ...
    @abstractmethod
    def clear(self) -> None: ...
    def get_token_count(self) -> int:
        return sum(len(m.get("", "")) // 3 for m in self.get_messages())


class SlidingWindowMemory(BaseMemory):
    def __init__(self, system_prompt: str = "你是助手。", max_messages: int = 20):
        self.system_prompt = system_prompt
        self.max_messages = max_messages
        self._messages: list[dict] = []

    def add(self, role: str, content: str) -> None:
        # TODO
        ...

    def get_messages(self) -> list[dict]:
        # TODO: system + 最近N条
        ...

    def clear(self) -> None:
        # TODO
        ...


class TokenAwareMemory(BaseMemory):
    def __init__(self, system_prompt: str = "你是助手。", max_tokens: int = 4000):
        self.system_prompt = system_prompt
        self.max_tokens = max_tokens
        self._messages: list[dict] = []

    def _estimate_tokens(self, text: str) -> int:
        # TODO
        ...

    def add(self, role: str, content: str) -> None:
        ...

    def get_messages(self) -> list[dict]:
        # TODO: 从最新向前添加
        ...

    def clear(self) -> None:
        ...
