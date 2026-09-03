"""Day 30 示例：Memory系统参考实现"""

from __future__ import annotations
import json
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path


class BaseMemory(ABC):
    """Memory接口 — 策略模式"""
    
    @abstractmethod
    def add(self, role: str, content: str) -> None: ...
    
    @abstractmethod
    def get_messages(self) -> list[dict]: ...
    
    @abstractmethod
    def clear(self) -> None: ...
    
    def get_token_count(self) -> int:
        """估算当前token数"""
        return sum(len(m.get("content", "")) // 3 for m in self.get_messages())


class SlidingWindowMemory(BaseMemory):
    """滑动窗口：保留最近N条消息"""
    
    def __init__(self, system_prompt: str = "你是AI助手。", max_messages: int = 20):
        self.system_prompt = system_prompt
        self.max_messages = max_messages
        self._messages: list[dict] = []
    
    def add(self, role: str, content: str) -> None:
        self._messages.append({"role": role, "content": content})
    
    def get_messages(self) -> list[dict]:
        messages = [{"role": "system", "content": self.system_prompt}]
        messages.extend(self._messages[-self.max_messages:])
        return messages
    
    def clear(self) -> None:
        self._messages.clear()


class TokenAwareMemory(BaseMemory):
    """Token感知：根据估算token数控制上下文"""
    
    def __init__(self, system_prompt: str = "你是AI助手。", max_tokens: int = 4000):
        self.system_prompt = system_prompt
        self.max_tokens = max_tokens
        self._messages: list[dict] = []
    
    def _estimate_tokens(self, text: str) -> int:
        # 中文约1字1token，英文约4字符1token
        return len(text) // 3
    
    def add(self, role: str, content: str) -> None:
        self._messages.append({"role": role, "content": content})
    
    def get_messages(self) -> list[dict]:
        messages = [{"role": "system", "content": self.system_prompt}]
        total = self._estimate_tokens(self.system_prompt)
        
        for msg in reversed(self._messages):
            msg_tokens = self._estimate_tokens(msg.get("content", ""))
            if total + msg_tokens > self.max_tokens:
                break
            messages.insert(1, msg)
            total += msg_tokens
        
        return messages
    
    def clear(self) -> None:
        self._messages.clear()


class SummaryMemory(BaseMemory):
    """摘要压缩：消息过多时用AI压缩历史"""
    
    def __init__(
        self,
        system_prompt: str = "你是AI助手。",
        max_recent: int = 20,
        compress_threshold: int = 30,
    ):
        self.system_prompt = system_prompt
        self.max_recent = max_recent
        self.compress_threshold = compress_threshold
        self.summary: str = ""
        self._recent: list[dict] = []
        self._client = None
    
    def _get_client(self):
        if self._client is None:
            from openai import AsyncOpenAI
            import os
            self._client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY", ""))
        return self._client
    
    def add(self, role: str, content: str) -> None:
        self._recent.append({"role": role, "content": content})
    
    async def compress(self) -> None:
        """压缩旧消息为摘要"""
        if len(self._recent) <= self.compress_threshold:
            return
        
        old = self._recent[:len(self._recent) // 2]
        self._recent = self._recent[len(self._recent) // 2:]
        
        client = self._get_client()
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "将以下对话压缩为简洁摘要，保留关键信息："},
                *old,
            ],
            max_tokens=200,
        )
        new_summary = response.choices[0].message.content
        
        if self.summary:
            self.summary = f"{self.summary}\n{new_summary}"
        else:
            self.summary = new_summary
    
    def get_messages(self) -> list[dict]:
        messages = [{"role": "system", "content": self.system_prompt}]
        if self.summary:
            messages.append({"role": "system", "content": f"[对话摘要] {self.summary}"})
        messages.extend(self._recent[-self.max_recent:])
        return messages
    
    def clear(self) -> None:
        self.summary = ""
        self._recent.clear()
    
    def save(self, path: str) -> None:
        data = {"summary": self.summary, "messages": self._recent}
        Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    
    def load(self, path: str) -> None:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        self.summary = data.get("summary", "")
        self._recent = data.get("messages", [])


if __name__ == "__main__":
    # 测试滑动窗口
    mem = SlidingWindowMemory(max_messages=3)
    for i in range(10):
        mem.add("user" if i % 2 == 0 else "assistant", f"消息{i}")
    
    msgs = mem.get_messages()
    print(f"总消息数: {len(msgs)}")  # 4 (system + 3 recent)
    for m in msgs:
        print(f"  [{m['role']}] {m['content']}")
    
    # 测试Token感知
    mem2 = TokenAwareMemory(max_tokens=20)
    mem2.add("user", "hello")
    mem2.add("user", "x" * 100)
    mem2.add("user", "y" * 100)
    msgs2 = mem2.get_messages()
    print(f"\nToken感知: {len(msgs2)}条消息")
