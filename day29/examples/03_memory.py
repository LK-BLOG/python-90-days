"""Day 29 示例3：Memory系统"""

from __future__ import annotations
import asyncio
from dataclasses import dataclass, field
from typing import Protocol
from openai import AsyncOpenAI


# ======== Memory接口（策略模式） ========

class MemoryStrategy(Protocol):
    def add(self, role: str, content: str) -> None: ...
    def get_messages(self) -> list[dict]: ...
    def clear(self) -> None: ...


# ======== 实现1：滑动窗口 ========

@dataclass
class SlidingWindowMemory:
    """保留最近N条消息"""
    system_prompt: str = "你是一个有用的助手。"
    max_messages: int = 20
    _messages: list[dict] = field(default_factory=list, init=False)
    
    def add(self, role: str, content: str) -> None:
        self._messages.append({"role": role, "content": content})
    
    def get_messages(self) -> list[dict]:
        messages = [{"role": "system", "content": self.system_prompt}]
        # 保留最近的消息
        messages.extend(self._messages[-self.max_messages:])
        return messages
    
    def clear(self) -> None:
        self._messages.clear()


# ======== 实现2：摘要压缩 ========

@dataclass
class SummaryMemory:
    """历史过长时用AI压缩为摘要"""
    client: AsyncOpenAI
    system_prompt: str = "你是一个有用的助手。"
    max_recent: int = 10
    summary: str = ""
    _recent: list[dict] = field(default_factory=list, init=False)
    
    def add(self, role: str, content: str) -> None:
        self._recent.append({"role": role, "content": content})
    
    async def maybe_compress(self) -> None:
        """如果最近消息太多，压缩旧消息为摘要"""
        if len(self._recent) <= self.max_recent:
            return
        
        # 取前半部分进行压缩
        old_messages = self._recent[:self.max_recent // 2]
        self._recent = self._recent[self.max_recent // 2:]
        
        # 用小模型压缩
        response = await self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "请将以下对话总结为一段简洁的摘要，保留关键信息："},
                *old_messages,
            ],
            max_tokens=200,
        )
        new_summary = response.choices[0].message.content
        
        # 合并旧摘要
        if self.summary:
            self.summary = f"{self.summary}\n{new_summary}"
        else:
            self.summary = new_summary
    
    def get_messages(self) -> list[dict]:
        messages = [{"role": "system", "content": self.system_prompt}]
        if self.summary:
            messages.append({
                "role": "system",
                "content": f"[对话摘要] {self.summary}"
            })
        messages.extend(self._recent)
        return messages
    
    def clear(self) -> None:
        self.summary = ""
        self._recent.clear()


# ======== 实现3：Token感知Memory ========

@dataclass
class TokenAwareMemory:
    """根据token数量控制上下文"""
    system_prompt: str = "你是一个有用的助手。"
    max_tokens: int = 4000
    _messages: list[dict] = field(default_factory=list, init=False)
    
    def add(self, role: str, content: str) -> None:
        self._messages.append({"role": role, "content": content})
    
    def _estimate_tokens(self, text: str) -> int:
        """粗略估计token数（中文约1字1token，英文约4字符1token）"""
        return len(text) // 3
    
    def get_messages(self) -> list[dict]:
        messages = [{"role": "system", "content": self.system_prompt}]
        total = self._estimate_tokens(self.system_prompt)
        
        # 从最新消息向前添加，直到超限
        for msg in reversed(self._messages):
            msg_tokens = self._estimate_tokens(msg["content"])
            if total + msg_tokens > self.max_tokens:
                break
            messages.insert(1, msg)  # 插入到system prompt之后
            total += msg_tokens
        
        return messages
    
    def clear(self) -> None:
        self._messages.clear()


if __name__ == "__main__":
    # 测试滑动窗口
    mem = SlidingWindowMemory(max_messages=5)
    for i in range(10):
        mem.add("user" if i % 2 == 0 else "assistant", f"消息{i}")
    print(f"滑动窗口: 保留了{len(mem.get_messages())}条消息")
    for m in mem.get_messages():
        print(f"  {m['role']}: {m['content']}")
