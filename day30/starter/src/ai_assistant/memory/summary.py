"""Day 30 - 摘要压缩记忆"""
from __future__ import annotations

from ai_assistant.memory.base import BaseMemory


class SummaryMemory(BaseMemory):
    """摘要压缩记忆

    当历史消息过多时，自动压缩旧消息为摘要。
    """

    def __init__(self, summary_threshold: int = 30, **kwargs):
        super().__init__(**kwargs)
        self.summary_threshold = summary_threshold
        self._summaries: list[str] = []
        self._recent: list[dict] = []

    def add(self, role: str, content: str) -> None:
        """添加消息，必要时触发压缩"""
        self._recent.append({"role": role, "content": content})
        if len(self._recent) >= self.summary_threshold:
            self._compress()

    def _compress(self) -> None:
        """将旧消息压缩为摘要"""
        # TODO: 选取前半部分消息，生成简单摘要
        # TODO: 将摘要存入 _summaries
        # TODO: 保留后半部分到 _recent
        half = len(self._recent) // 2
        old_messages = self._recent[:half]
        summary = "之前的对话摘要：" + "; ".join(
            m["content"][:50] for m in old_messages
        )
        self._summaries.append(summary)
        self._recent = self._recent[half:]

    def get_messages(self) -> list[dict]:
        """获取 摘要 + 最近消息"""
        messages = []
        if self.system_prompt:
            messages.append({"role": "system", "content": self.system_prompt})
        for s in self._summaries:
            messages.append({"role": "system", "content": s})
        messages.extend(self._recent)
        return messages

    def clear(self) -> None:
        self._summaries.clear()
        self._recent.clear()

    @property
    def token_count(self) -> int:
        total = sum(len(s) for s in self._summaries)
        total += sum(len(m.get("content", "")) for m in self._recent)
        return total // 2
