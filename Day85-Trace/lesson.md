# Day 85: Trace - Agent 执行追踪系统

## 1. Trace 概念

追踪系统让你能看到 Agent 的"大脑"是怎么运转的——每一步做了什么、花了多少时间、消耗了多少 token。

### 核心术语

| 概念 | 说明 | 类比 |
|------|------|------|
| **Trace** | 一次完整的执行过程 | 一本书 |
| **Span** | Trace 中的一个操作 | 书中的一个章节 |
| **SpanContext** | 跨边界的追踪上下文 | 书签，标记你在哪 |
| **Parent Span** | 当前 Span 的上级 | 章节的父级（卷） |
| **Exporter** | 导出追踪数据 | 评论家，把内容发布出去 |

### 为什么 Agent 需要 Trace？

```
用户提问 → LLM 思考 → 调用工具 → 获取结果 → 再次思考 → 回答

这里面有多个 LLM 调用、工具调用、等待时间……
没有追踪，你根本不知道时间花在哪了、token 花了多少、哪个工具调用出错了。
```

## 2. Span 实现

Span 是追踪的基本单元：

```python
import time
import uuid
from dataclasses import dataclass, field
from typing import Optional, Dict, List, Any
from enum import Enum
from contextlib import contextmanager


class SpanStatus(Enum):
    OK = "ok"
    ERROR = "error"
    UNSET = "unset"


@dataclass
class SpanEvent:
    """Span 内部事件（瞬时记录）"""
    name: str
    timestamp: float
    attributes: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Span:
    """追踪单元"""
    name: str
    trace_id: str
    span_id: str = field(default_factory=lambda: uuid.uuid4().hex[:16])
    parent_id: Optional[str] = None
    start_time: float = field(default_factory=time.time)
    end_time: Optional[float] = None
    status: SpanStatus = SpanStatus.UNSET
    attributes: Dict[str, Any] = field(default_factory=dict)
    events: List[SpanEvent] = field(default_factory=list)
    children: List["Span"] = field(default_factory=list)

    @property
    def duration_ms(self) -> float:
        """持续时间（毫秒）"""
        if self.end_time is None:
            return (time.time() - self.start_time) * 1000
        return (self.end_time - self.start_time) * 1000

    @property
    def is_recording(self) -> bool:
        return self.end_time is None

    def set_attribute(self, key: str, value: Any):
        """设置 Span 属性"""
        self.attributes[key] = value

    def add_event(self, name: str, **attrs):
        """添加瞬时事件"""
        self.events.append(SpanEvent(
            name=name, timestamp=time.time(), attributes=attrs
        ))

    def set_status(self, status: SpanStatus, message: str = ""):
        self.status = status
        if message:
            self.attributes["error.message"] = message

    def end(self):
        """结束 Span"""
        self.end_time = time.time()

    def to_dict(self) -> dict:
        """序列化为字典"""
        return {
            "trace_id": self.trace_id,
            "span_id": self.span_id,
            "parent_id": self.parent_id,
            "name": self.name,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "duration_ms": self.duration_ms,
            "status": self.status.value,
            "attributes": self.attributes,
            "events": [
                {"name": e.name, "timestamp": e.timestamp, "attributes": e.attributes}
                for e in self.events
            ],
            "children": [c.to_dict() for c in self.children],
        }
```

## 3. Agent 调用链追踪

把追踪集成到 Agent 的执行流程中：

```python
import threading

class Tracer:
    """追踪器：管理 Span 的生命周期"""

    def __init__(self, service_name: str = "agent"):
        self.service_name = service_name
        self._active_spans: Dict[str, Span] = {}  # thread_id → Span
        self._completed_traces: List[Dict] = []
        self._lock = threading.Lock()

    def start_span(self, name: str, parent: Optional[Span] = None) -> Span:
        """创建并开始一个新 Span"""
        trace_id = parent.trace_id if parent else uuid.uuid4().hex
        span = Span(
            name=name,
            trace_id=trace_id,
            parent_id=parent.span_id if parent else None,
        )
        if parent:
            parent.children.append(span)
        thread_key = f"{threading.current_thread().ident}"
        self._active_spans[thread_key] = span
        return span

    @contextmanager
    def span(self, name: str, **attrs):
        """上下文管理器：自动管理 Span 生命周期"""
        parent = self._active_spans.get(
            f"{threading.current_thread().ident}"
        )
        s = self.start_span(name, parent)
        for k, v in attrs.items():
            s.set_attribute(k, v)
        try:
            yield s
        except Exception as e:
            s.set_status(SpanStatus.ERROR, str(e))
            raise
        else:
            s.set_status(SpanStatus.OK)
        finally:
            s.end()
            # 恢复父 Span
            if parent:
                self._active_spans[
                    f"{threading.current_thread().ident}"
                ] = parent
            elif not parent:
                # 根 Span 结束，保存 trace
                self._completed_traces.append(s.to_dict())
                self._active_spans.pop(
                    f"{threading.current_thread().ident}", None
                )

    def get_traces(self) -> List[Dict]:
        return self._completed_traces
```

## 4. Token 计数与成本追踪

Agent 调用大模型时，追踪 token 用量和费用：

```python
@dataclass
class TokenUsage:
    """Token 使用统计"""
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0

    def __add__(self, other: "TokenUsage") -> "TokenUsage":
        return TokenUsage(
            prompt_tokens=self.prompt_tokens + other.prompt_tokens,
            completion_tokens=self.completion_tokens + other.completion_tokens,
            total_tokens=self.total_tokens + other.total_tokens,
        )


@dataclass
class CostRate:
    """模型定价"""
    model: str
    input_price_per_1k: float   # 每1000 input tokens 价格（美元）
    output_price_per_1k: float  # 每1000 output tokens 价格（美元）

    def calculate_cost(self, usage: TokenUsage) -> float:
        """计算调用成本"""
        input_cost = (usage.prompt_tokens / 1000) * self.input_price_per_1k
        output_cost = (usage.completion_tokens / 1000) * self.output_price_per_1k
        return round(input_cost + output_cost, 6)


class CostTracker:
    """成本追踪器"""

    # 预设定价
    PRICING = {
        "gpt-4o": CostRate("gpt-4o", 2.50 / 1000, 10.00 / 1000),
        "gpt-4o-mini": CostRate("gpt-4o-mini", 0.15 / 1000, 0.60 / 1000),
        "gpt-3.5-turbo": CostRate("gpt-3.5-turbo", 0.50 / 1000, 1.50 / 1000),
    }

    def __init__(self):
        self._records: List[dict] = []
        self._total_cost: float = 0.0
        self._total_tokens: TokenUsage = TokenUsage()

    def record(self, model: str, usage: TokenUsage,
               operation: str = "", trace_id: str = ""):
        """记录一次调用"""
        rate = self.PRICING.get(model)
        cost = rate.calculate_cost(usage) if rate else 0.0

        self._records.append({
            "timestamp": time.time(),
            "model": model,
            "operation": operation,
            "trace_id": trace_id,
            "usage": usage,
            "cost": cost,
        })
        self._total_cost += cost
        self._total_tokens = self._total_tokens + usage
        return cost

    def summary(self) -> dict:
        """成本摘要"""
        return {
            "total_cost_usd": round(self._total_cost, 4),
            "total_calls": len(self._records),
            "total_tokens": {
                "prompt": self._total_tokens.prompt_tokens,
                "completion": self._total_tokens.completion_tokens,
                "total": self._total_tokens.total_tokens,
            },
            "by_model": self._by_model(),
        }

    def _by_model(self) -> dict:
        result = {}
        for r in self._records:
            model = r["model"]
            if model not in result:
                result[model] = {"calls": 0, "tokens": 0, "cost": 0.0}
            result[model]["calls"] += 1
            result[model]["tokens"] += r["usage"].total_tokens
            result[model]["cost"] += r["cost"]
        for v in result.values():
            v["cost"] = round(v["cost"], 4)
        return result
```

## 5. 日志聚合

把追踪数据、日志、指标聚合在一起：

```python
import json
from pathlib import Path
from datetime import datetime


class LogAggregator:
    """日志聚合器：统一收集追踪、日志、指标"""

    def __init__(self, output_dir: str = "trace_logs"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self._logs: List[dict] = []

    def emit(self, level: str, message: str,
             trace_id: str = "", span_id: str = "",
             **extra):
        """发射一条日志"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "level": level,
            "message": message,
            "trace_id": trace_id,
            "span_id": span_id,
            **extra,
        }
        self._logs.append(entry)
        return entry

    def info(self, msg, **kw): return self.emit("INFO", msg, **kw)
    def warn(self, msg, **kw): return self.emit("WARN", msg, **kw)
    def error(self, msg, **kw): return self.emit("ERROR", msg, **kw)

    def query(self, trace_id: str = None,
              level: str = None) -> List[dict]:
        """查询日志"""
        logs = self._logs
        if trace_id:
            logs = [l for l in logs if l["trace_id"] == trace_id]
        if level:
            logs = [l for l in logs if l["level"] == level]
        return logs

    def flush(self):
        """持久化到文件"""
        date_str = datetime.now().strftime("%Y-%m-%d")
        path = self.output_dir / f"logs_{date_str}.jsonl"
        with open(path, "a", encoding="utf-8") as f:
            for log in self._logs:
                f.write(json.dumps(log, ensure_ascii=False) + "\n")
        self._logs.clear()
```

## 关键要点

1. **Span 是基础**：每个操作一个 Span，记录开始/结束/属性/事件
2. **Trace 是全貌**：Span 通过 parent_id 组成树，构成完整 Trace
3. **Context 传递**：追踪上下文需要跨函数、跨线程、跨服务传递
4. **Token 成本**：Agent 每次 LLM 调用都要计数和计费
5. **日志聚合**：追踪数据 + 日志 + 指标，三合一才有价值

## 下一步

完成 [挑战练习](challenge.md) 和 [终极挑战](ultimate_challenge.md)。
