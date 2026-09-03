# Day 80: Context Engineering — 完整知识点

## 1. 什么是上下文工程？

上下文工程（Context Engineering）是**精心设计输入给LLM的信息**的系统化方法。
核心理念：LLM的能力上限取决于你给它的上下文质量，而不是模型本身。

```
┌─────────────────────────────────────────┐
│            上下文窗口 (Context Window)     │
│  ┌───────────────────────────────────┐  │
│  │ System Prompt      [固定]          │  │
│  ├───────────────────────────────────┤  │
│  │ 工具定义          [固定]          │  │
│  ├───────────────────────────────────┤  │
│  │ 工作记忆          [半固定]         │  │
│  ├───────────────────────────────────┤  │
│  │ 对话历史          [滑动窗口]       │  │
│  ├───────────────────────────────────┤  │
│  │ 当前用户消息       [固定]          │  │
│  └───────────────────────────────────┘  │
│         Token Budget: 128K              │
└─────────────────────────────────────────┘
```

## 2. Token预算管理

### 2.1 为什么需要预算管理？

每个模型有固定的上下文窗口大小（如GPT-4: 128K, Claude: 200K）。
如果塞满了，要么报错，要么截断丢失信息。

### 2.2 Token计数

```python
# 方式1: 字符级近似（1 token ≈ 4字符 英文 / ≈ 1.5字符 中文）
def approx_tokens(text: str) -> int:
    ascii_count = sum(1 for c in text if ord(c) < 128)
    non_ascii_count = len(text) - ascii_count
    return (ascii_count / 4 + non_ascii_count / 1.5).__ceil__()

# 方式2: tiktoken精确计数
import tiktoken
def exact_tokens(text: str, model: str = "gpt-4") -> int:
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))
```

### 2.3 预算分配策略

```python
class TokenBudget:
    """Token预算分配器"""
    def __init__(self, total: int):
        self.total = total
        self.allocations = {}

    def allocate(self, name: str, ratio: float):
        """按比例分配预算"""
        self.allocations[name] = int(self.total * ratio)

    def remaining(self, name: str, used: int) -> int:
        return self.allocations.get(name, 0) - used

# 典型分配
budget = TokenBudget(128000)
budget.allocate("system_prompt", 0.05)   # 5% = 6400
budget.allocate("tools", 0.10)           # 10% = 12800
budget.allocate("working_memory", 0.05)  # 5% = 6400
budget.allocate("history", 0.70)         # 70% = 89600
budget.allocate("current_msg", 0.10)     # 10% = 12800
```

## 3. System Prompt工程

### 3.1 System Prompt的核心作用
- 定义角色和行为边界
- 注入领域知识
- 设置输出格式约束
- 安全规则与过滤

### 3.2 模板化System Prompt

```python
import re
from typing import Dict

class SystemPromptBuilder:
    """可参数化的System Prompt构建器"""

    def __init__(self, template: str):
        self.template = template
        self.variables: Dict[str, str] = {}
        self.conditionals: Dict[str, bool] = {}

    def set_var(self, key: str, value: str):
        self.variables[key] = value
        return self

    def set_conditional(self, name: str, enabled: bool):
        self.conditionals[name] = enabled
        return self

    def build(self) -> str:
        result = self.template
        # 替换变量
        for key, value in self.variables.items():
            placeholder = "${" + key + "}"
            result = result.replace(placeholder, value)
        # 处理条件块
        for name, enabled in self.conditionals.items():
            pattern = r"\[\[IF " + name + r"\]\](.*?)\[\[ENDIF\]\]"
            if enabled:
                result = re.sub(pattern, r"\1", result, flags=re.DOTALL)
            else:
                result = re.sub(pattern, "", result, flags=re.DOTALL)
        return result.strip()

# 使用示例
builder = SystemPromptBuilder("""
你是一个${role}助手。
你的专长是${expertise}。
[[IF language_zh]]
请用中文回答。
[[ENDIF]]
[[IF verbose]]
请详细解释你的推理过程。
[[ENDIF]]
""")
builder.set_var("role", "数据分析")
builder.set_var("expertise", "Python和SQL")
builder.set_conditional("language_zh", True)
builder.set_conditional("verbose", False)
prompt = builder.build()
print(prompt)
```

### 3.3 常见错误
- ❌ System Prompt太长浪费Token预算
- ❌ 没有明确的输出格式约束
- ❌ 指令矛盾或模糊
- ✅ 分层组织：角色 → 规则 → 格式 → 示例
- ✅ 用XML/Markdown标签分隔不同部分

## 4. 上下文压缩与摘要

### 4.1 为什么需要压缩？

对话进行到第50轮时：
- 原始历史: ~50,000 tokens
- 可用预算: ~90,000 tokens
- 需要压缩: 把旧对话压缩，给新消息留空间

### 4.2 三种压缩策略

```python
from abc import ABC, abstractmethod
from typing import List, Dict

class CompressionStrategy(ABC):
    @abstractmethod
    def compress(self, messages: List[Dict], target_tokens: int) -> List[Dict]:
        pass

class SummaryCompression(CompressionStrategy):
    """摘要压缩：让LLM总结旧对话"""
    def __init__(self, llm_fn):
        self.llm_fn = llm_fn

    def compress(self, messages, target_tokens):
        keep_ratio = 0.3
        split = int(len(messages) * (1 - keep_ratio))
        to_compress = messages[:split]
        to_keep = messages[split:]
        summary = self.llm_fn(f"请总结以下对话的要点：\n{to_compress}")
        return [{"role": "system", "content": f"[对话摘要] {summary}"}] + to_keep

class ExtractiveCompression(CompressionStrategy):
    """提取压缩：只保留关键信息"""
    def compress(self, messages, target_tokens):
        important_keywords = ["重要", "决定", "结论", "TODO", "记住"]
        result = []
        for msg in messages:
            content = msg.get("content", "")
            if any(kw in content for kw in important_keywords) or msg["role"] == "user":
                result.append(msg)
        return result

class TruncationCompression(CompressionStrategy):
    """裁剪压缩：按Token数截断"""
    def __init__(self, count_fn):
        self.count_fn = count_fn

    def compress(self, messages, target_tokens):
        result = []
        current = 0
        for msg in reversed(messages):
            tokens = self.count_fn(msg.get("content", ""))
            if current + tokens > target_tokens:
                break
            current += tokens
            result.insert(0, msg)
        return result
```

### 4.3 上下文摘要存储

```python
import datetime
from typing import List, Tuple

class ContextSummary:
    """管理对话的历史摘要"""

    def __init__(self):
        self.summaries = []
        self.summary_metadata = []

    def add_summary(self, summary: str, message_range: Tuple[int, int]):
        self.summaries.append(summary)
        self.summary_metadata.append({
            "start": message_range[0],
            "end": message_range[1],
            "timestamp": datetime.datetime.now().isoformat()
        })

    def get_full_summary(self) -> str:
        if not self.summaries:
            return ""
        return "\n".join(f"[{i+1}] {s}" for i, s in enumerate(self.summaries))

    def should_compress(self, messages: List, threshold: float = 0.7) -> bool:
        total_chars = sum(len(m.get("content", "")) for m in messages)
        return total_chars > threshold * 50000
```

## 5. 动态上下文注入

### 5.1 关键词驱动注入

```python
from typing import List, Dict

class DynamicInjector:
    """根据用户意图动态注入上下文"""

    def __init__(self):
        self.injection_rules: List[Dict] = []

    def add_rule(self, keyword: str, context: str, priority: int = 0):
        self.injection_rules.append({
            "keyword": keyword,
            "context": context,
            "priority": priority
        })
        self.injection_rules.sort(key=lambda r: r["priority"], reverse=True)

    def inject(self, user_message: str, max_tokens: int) -> str:
        injected = []
        remaining = max_tokens
        for rule in self.injection_rules:
            if rule["keyword"].lower() in user_message.lower():
                tokens_needed = len(rule["context"]) // 2
                if tokens_needed <= remaining:
                    injected.append(rule["context"])
                    remaining -= tokens_needed
        return "\n---\n".join(injected)
```

### 5.2 RAG注入模式

```python
class RAGInjector:
    """基于检索的上下文注入"""

    def __init__(self, vector_store):
        self.vector_store = vector_store

    def build_context(self, query: str, top_k: int = 5) -> str:
        results = self.vector_store.search(query, top_k=top_k)
        context_parts = []
        for i, doc in enumerate(results):
            context_parts.append(f"[文档{i+1}] {doc['title']}\n{doc['content']}")
        return "\n\n".join(context_parts)
```

## 6. 滑动窗口策略

### 6.1 固定窗口

```python
class FixedWindow:
    def __init__(self, max_messages: int):
        self.max_messages = max_messages
        self.messages = []

    def add(self, message: dict):
        self.messages.append(message)
        while len(self.messages) > self.max_messages:
            self.messages.pop(0)

    def get_messages(self) -> list:
        return self.messages.copy()
```

### 6.2 重要性加权窗口

```python
class ImportanceWindow:
    """基于重要性分数的智能窗口"""

    def __init__(self, max_tokens: int, count_fn):
        self.max_tokens = max_tokens
        self.count_fn = count_fn
        self.messages = []

    def score_message(self, msg: dict, position: int, total: int) -> float:
        score = 0.0
        score += (position / total) * 0.3  # 位置权重
        if msg["role"] == "user":
            score += 0.2
        elif msg["role"] == "assistant":
            score += 0.1
        content = msg.get("content", "")
        if any(kw in content for kw in ["重要", "决定", "结论", "TODO"]):
            score += 0.2
        return score

    def select_messages(self) -> list:
        scored = []
        for i, msg in enumerate(self.messages):
            score = self.score_message(msg, i, len(self.messages))
            tokens = self.count_fn(msg.get("content", ""))
            scored.append((score, i, tokens, msg))
        scored.sort(key=lambda x: x[0], reverse=True)
        selected = []
        total_tokens = 0
        for score, idx, tokens, msg in scored:
            if total_tokens + tokens <= self.max_tokens:
                selected.append(msg)
                total_tokens += tokens
        selected.sort(key=lambda m: self.messages.index(m))
        return selected
```

## 7. 完整的上下文管理器

```python
class ContextManager:
    """生产级上下文管理器"""

    def __init__(self, total_token_budget: int):
        self.budget = TokenBudget(total_token_budget)
        self.budget.allocate("system", 0.08)
        self.budget.allocate("tools", 0.12)
        self.budget.allocate("working_memory", 0.05)
        self.budget.allocate("history", 0.65)
        self.budget.allocate("current", 0.10)
        self.system_prompt = ""
        self.tool_definitions = []
        self.working_memory = {}
        self.conversation_history = []
        self.summary_store = ContextSummary()

    def set_system_prompt(self, prompt: str):
        self.system_prompt = prompt

    def add_message(self, role: str, content: str):
        self.conversation_history.append({"role": role, "content": content})

    def build_context(self) -> list:
        messages = []
        messages.append({"role": "system", "content": self.system_prompt})
        if self.working_memory:
            memory_text = "\n".join(f"- {k}: {v}" for k, v in self.working_memory.items())
            messages.append({"role": "system", "content": f"[工作记忆]\n{memory_text}"})
        summary = self.summary_store.get_full_summary()
        if summary:
            messages.append({"role": "system", "content": f"[对话摘要]\n{summary}"})
        available = self.budget.remaining("history", self._count_tokens(str(messages)))
        history_window = self._apply_window(self.conversation_history, available)
        messages.extend(history_window)
        return messages

    def _count_tokens(self, text: str) -> int:
        return len(text) // 3

    def _apply_window(self, messages: list, max_tokens: int) -> list:
        result = []
        total = 0
        for msg in reversed(messages):
            tokens = self._count_tokens(msg.get("content", ""))
            if total + tokens > max_tokens:
                break
            result.insert(0, msg)
            total += tokens
        return result
```

## 8. 实际应用
- 聊天机器人：System Prompt定义角色 + 对话历史滑动窗口 + 用户画像
- RAG系统：检索结果动态注入 + Token预算管理
- 多工具Agent：工具调用结果保留 + 工具输出压缩

## 9. 常见错误汇总
| 错误 | 后果 | 正确做法 |
|------|------|---------|
| 不管Token限制 | API报错/截断 | 始终预算管理 |
| System Prompt太长 | 压缩历史空间 | 精简到核心指令 |
| 丢弃第一条消息 | 丢失角色设定 | 保护System Prompt |
| 压缩过度 | 关键信息丢失 | 保留最近+重要消息 |
| 不缓存摘要 | 重复压缩浪费 | 缓存已压缩的摘要 |
