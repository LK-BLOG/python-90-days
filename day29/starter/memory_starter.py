# Day 29 - Challenge 4: Memory 系统
# 滑动窗口、摘要压缩、Token 计数、System Prompt 保留

import json
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Message:
    """对话消息"""
    role: str  # system / user / assistant
    content: str


class BaseMemory:
    """记忆系统基类"""

    def __init__(self, system_prompt: str = "", max_tokens: int = 4000):
        """初始化

        Args:
            system_prompt: 系统提示词（始终保留）
            max_tokens: 最大 token 限制
        """
        self.system_prompt = system_prompt
        self.max_tokens = max_tokens
        self._messages: list[Message] = []

    def add(self, role: str, content: str) -> None:
        """添加一条消息"""
        self._messages.append(Message(role=role, content=content))

    def get_messages(self) -> list[dict]:
        """获取当前消息列表（含 system prompt）

        Returns:
            消息字典列表，可直接传给 AI
        """
        # TODO: system prompt 始终在最前面
        # TODO: 返回格式 [{"role": ..., "content": ...}, ...]
        ...

    def clear(self) -> None:
        """清空历史消息（保留 system prompt）"""
        self._messages.clear()

    @property
    def token_count(self) -> int:
        """估算当前 token 数"""
        # TODO: 简单估算
        ...


class SlidingWindowMemory(BaseMemory):
    """滑动窗口记忆

    保留最近 N 条消息，超出时丢弃最旧的（保留 system prompt）。
    """

    def __init__(self, window_size: int = 20, **kwargs):
        """初始化

        Args:
            window_size: 保留的消息窗口大小
        """
        super().__init__(**kwargs)
        self.window_size = window_size

    def add(self, role: str, content: str) -> None:
        """添加消息，超出窗口时丢弃旧消息"""
        # TODO: 添加消息后，如果超出窗口大小，移除最早的非 system 消息
        ...

    def get_messages(self) -> list[dict]:
        """获取当前窗口内的消息"""
        # TODO: 返回 system prompt + 窗口内的消息
        ...


class SummaryMemory(BaseMemory):
    """摘要压缩记忆

    当历史过长时，用 AI 压缩旧消息为摘要。
    """

    def __init__(self, summary_threshold: int = 30, **kwargs):
        """初始化

        Args:
            summary_threshold: 触发压缩的消息数阈值
        """
        super().__init__(**kwargs)
        self.summary_threshold = summary_threshold
        self._summaries: list[str] = []
        self._recent_messages: list[Message] = []

    def add(self, role: str, content: str) -> None:
        """添加消息，必要时触发压缩"""
        # TODO: 添加到 recent_messages
        # TODO: 达到阈值时触发压缩
        ...

    def _compress(self) -> str:
        """将旧消息压缩为摘要

        Returns:
            摘要文本
        """
        # TODO: 选取最旧的消息，生成摘要
        # TODO: 可以用简单截断或 AI 生成
        ...

    def get_messages(self) -> list[dict]:
        """获取 摘要 + 最近消息"""
        # TODO: [system] + [摘要消息] + [最近消息]
        ...

    def clear(self) -> None:
        """清空所有记忆"""
        super().clear()
        self._summaries.clear()
        self._recent_messages.clear()


# ==================== 测试 ====================
if __name__ == "__main__":
    # 测试滑动窗口
    mem = SlidingWindowMemory(window_size=5, system_prompt="你是一个助手")
    for i in range(10):
        mem.add("user", f"问题 {i}")
        mem.add("assistant", f"回答 {i}")
    messages = mem.get_messages()
    print(f"滑动窗口: {len(messages)} 条消息（含 system）")

    # 测试摘要记忆
    smem = SummaryMemory(summary_threshold=6, system_prompt="你是一个助手")
    for i in range(8):
        smem.add("user", f"问题 {i}")
        smem.add("assistant", f"回答 {i}")
    messages = smem.get_messages()
    print(f"摘要记忆: {len(messages)} 条消息")
