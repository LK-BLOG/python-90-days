"""Day 30 - 滑动窗口记忆"""
from __future__ import annotations

from ai_assistant.memory.base import BaseMemory


class SlidingWindowMemory(BaseMemory):
    """滑动窗口记忆

    保留最近 N 条消息，超出时丢弃最旧的。
    System prompt 始终保留。
    """

    def __init__(self, window_size: int = 20, **kwargs):
        """初始化

        Args:
            window_size: 保留的消息窗口大小
        """
        super().__init__(**kwargs)
        self.window_size = window_size
        self._messages: list[dict] = []

    def add(self, role: str, content: str) -> None:
        """添加消息，超出窗口时丢弃旧消息"""
        # TODO: 添加消息到列表
        self._messages.append({"role": role, "content": content})
        # TODO: 如果超出窗口大小，移除最早的非 system 消息
        ...

    def get_messages(self) -> list[dict]:
        """获取当前窗口内的消息"""
        messages = []
        # TODO: 添加 system prompt
        if self.system_prompt:
            messages.append({"role": "system", "content": self.system_prompt})
        # TODO: 添加窗口内的消息
        messages.extend(self._messages[-self.window_size:])
        return messages

    def clear(self) -> None:
        """清空历史消息"""
        self._messages.clear()

    @property
    def token_count(self) -> int:
        """估算当前 token 数"""
        total = sum(len(m.get("content", "")) for m in self._messages)
        return total // 2  # 粗略估算
