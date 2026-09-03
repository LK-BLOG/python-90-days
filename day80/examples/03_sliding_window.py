# Day 80 - Example 3: 滑动窗口策略演示

from typing import List, Dict, Callable
from collections import deque
import random

def simple_token_count(text: str) -> int:
    """简单Token估算"""
    return len(text) // 3

# ===== 策略1: 固定消息数窗口 =====
class FixedMessageWindow:
    """固定消息数的滑动窗口"""

    def __init__(self, max_messages: int):
        self.max_messages = max_messages
        self.messages: List[Dict] = []

    def add(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})
        # 从头部丢弃最早的
        while len(self.messages) > self.max_messages:
            removed = self.messages.pop(0)
            print(f"  [窗口] 丢弃: {removed['content'][:30]}...")

    def get_messages(self) -> List[Dict]:
        return self.messages.copy()

    def stats(self) -> Dict:
        total_tokens = sum(simple_token_count(m["content"]) for m in self.messages)
        return {
            "count": len(self.messages),
            "max": self.max_messages,
            "tokens": total_tokens,
        }


# ===== 策略2: Token预算窗口 =====
class TokenBudgetWindow:
    """基于Token预算的滑动窗口"""

    def __init__(self, max_tokens: int, count_fn: Callable = simple_token_count):
        self.max_tokens = max_tokens
        self.count_fn = count_fn
        self.messages: List[Dict] = []

    def add(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})
        self._trim()

    def _trim(self):
        """裁剪到预算范围内，保留最新的"""
        total = sum(self.count_fn(m["content"]) for m in self.messages)
        while total > self.max_tokens and len(self.messages) > 1:
            removed = self.messages.pop(0)
            total -= self.count_fn(removed["content"])
            print(f"  [Token窗口] 裁剪: {removed['content'][:30]}... (剩余≈{total} tokens)")

    def get_messages(self) -> List[Dict]:
        return self.messages.copy()


# ===== 策略3: 重要性加权窗口 =====
class ImportanceWindow:
    """基于重要性分数的智能窗口"""

    def __init__(self, max_tokens: int, count_fn: Callable = simple_token_count):
        self.max_tokens = max_tokens
        self.count_fn = count_fn
        self.messages: List[Dict] = []

    def _score(self, msg: Dict, idx: int, total: int) -> float:
        score = 0.0
        # 位置：越新越重要
        score += (idx / max(total, 1)) * 0.4
        # 角色：用户>系统>助手
        role_scores = {"user": 0.3, "system": 0.2, "assistant": 0.1}
        score += role_scores.get(msg["role"], 0)
        # 关键词加分
        content = msg.get("content", "")
        important_words = ["重要", "决定", "结论", "TODO", "注意", "总结"]
        if any(w in content for w in important_words):
            score += 0.3
        return score

    def add(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})

    def select(self) -> List[Dict]:
        """选择最重要的消息，保持时间顺序"""
        if not self.messages:
            return []

        scored = []
        for i, msg in enumerate(self.messages):
            s = self._score(msg, i, len(self.messages))
            t = self.count_fn(msg.get("content", ""))
            scored.append((s, i, t, msg))

        # 按分数降序，贪心选择
        scored.sort(key=lambda x: x[0], reverse=True)
        selected = []
        budget_left = self.max_tokens
        for s, idx, tokens, msg in scored:
            if budget_left - tokens >= 0:
                selected.append(msg)
                budget_left -= tokens

        # 恢复时间顺序
        msg_to_idx = {id(m): i for i, m in enumerate(self.messages)}
        selected.sort(key=lambda m: msg_to_idx.get(id(m), 0))
        return selected


if __name__ == "__main__":
    print("=" * 60)
    print("策略1: 固定消息数窗口 (max=5)")
    print("=" * 60)
    win1 = FixedMessageWindow(max_messages=5)
    for i in range(8):
        role = "user" if i % 2 == 0 else "assistant"
        win1.add(role, f"第{i+1}轮对话内容: {'x' * random.randint(20, 60)}")
        print(f"  添加后: {win1.stats()}")
    print(f"最终消息: {len(win1.get_messages())} 条")

    print("\n" + "=" * 60)
    print("策略2: Token预算窗口 (max=200 tokens)")
    print("=" * 60)
    win2 = TokenBudgetWindow(max_tokens=200)
    for i in range(8):
        role = "user" if i % 2 == 0 else "assistant"
        content = f"第{i+1}轮: {'长内容' * random.randint(5, 20)}"
        win2.add(role, content)
        tokens = sum(simple_token_count(m["content"]) for m in win2.get_messages())
        print(f"  添加后: {len(win2.get_messages())}条, ~{tokens} tokens")

    print("\n" + "=" * 60)
    print("策略3: 重要性加权窗口 (max=150 tokens)")
    print("=" * 60)
    win3 = ImportanceWindow(max_tokens=150)
    # 模拟对话
    messages = [
        ("system", "你是一个助手。"),
        ("user", "你好"),
        ("assistant", "你好！有什么可以帮你的？"),
        ("user", "请记住这个重要信息：项目截止日期是12月30日"),
        ("assistant", "好的，我记住了。项目截止日期12月30日。"),
        ("user", "今天天气怎么样？"),
        ("assistant", "抱歉，我无法获取实时天气数据。"),
        ("user", "那帮我总结一下之前的对话"),
        ("assistant", "根据之前的对话，你提到了重要事项：项目截止日期12月30日。"),
        ("user", "好的，谢谢"),
    ]
    for role, content in messages:
        win3.add(role, content)
    selected = win3.select()
    print(f"原始: {len(win3.messages)}条, 选择后: {len(selected)}条")
    for m in selected:
        print(f"  [{m['role']}] {m['content'][:50]}")
