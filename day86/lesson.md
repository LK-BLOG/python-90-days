# Day 86: Evaluation & Tracing

## 1. Agent 评估

### 1.1 评估维度

`python
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from datetime import datetime
import time


@dataclass
class EvaluationResult:
    \"\"\"评估结果\"\"\"
    task_id: str
    success: bool
    score: float  # 0-1
    metrics: Dict[str, float] = field(default_factory=dict)
    details: str = ""
    duration: float = 0.0
    token_usage: int = 0
    cost: float = 0.0


class AgentEvaluator:
    \"\"\"Agent 评估器\"\"\"
    
    def __init__(self):
        self.results: List[EvaluationResult] = []
    
    def evaluate(
        self,
        task_id: str,
        agent_output: str,
        expected_output: str,
        tools_used: List[str] = None,
        duration: float = 0,
        tokens: int = 0
    ) -> EvaluationResult:
        \"\"\"评估 Agent 输出\"\"\"
        metrics = {}
        
        # 1. 正确性
        if expected_output:
            match_score = self._exact_match(agent_output, expected_output)
            similarity_score = self._similarity(agent_output, expected_output)
            metrics["correctness"] = (match_score + similarity_score) / 2
        
        # 2. 完整性
        metrics["completeness"] = self._check_completeness(agent_output)
        
        # 3. 格式
        metrics["format"] = self._check_format(agent_output)
        
        # 4. 效率
        metrics["efficiency"] = self._calc_efficiency(duration, tokens)
        
        # 5. 工具使用
        if tools_used:
            metrics["tool_usage"] = len(tools_used) / 5  # 假设5个工具为满分
        
        # 综合得分
        weights = {"correctness": 0.4, "completeness": 0.2, "format": 0.1, "efficiency": 0.15, "tool_usage": 0.15}
        score = sum(metrics.get(k, 0) * w for k, w in weights.items())
        
        result = EvaluationResult(
            task_id=task_id,
            success=score >= 0.6,
            score=score,
            metrics=metrics,
            duration=duration,
            token_usage=tokens,
        )
        
        self.results.append(result)
        return result
    
    def _exact_match(self, output: str, expected: str) -> float:
        if not expected: return 0.5
        return 1.0 if output.strip() == expected.strip() else 0.0
    
    def _similarity(self, a: str, b: str) -> float:
        if not b: return 0.0
        common = set(a.lower().split()) & set(b.lower().split())
        total = set(a.lower().split()) | set(b.lower().split())
        return len(common) / max(len(total), 1)
    
    def _check_completeness(self, output: str) -> float:
        if len(output) > 100: return 0.9
        if len(output) > 50: return 0.7
        if len(output) > 10: return 0.5
        return 0.2
    
    def _check_format(self, output: str) -> float:
        score = 0.5
        if '\n' in output: score += 0.1
        if any(c in output for c in ['1', '2', '3']): score += 0.1
        if len(output.split('\n')) >= 3: score += 0.2
        return min(score, 1.0)
    
    def _calc_efficiency(self, duration: float, tokens: int) -> float:
        score = 1.0
        if duration > 30: score -= 0.3
        if duration > 60: score -= 0.3
        if tokens > 5000: score -= 0.2
        return max(score, 0.0)
    
    def get_summary(self) -> Dict:
        if not self.results: return {}
        total = len(self.results)
        success = sum(1 for r in self.results if r.success)
        avg_score = sum(r.score for r in self.results) / total
        avg_tokens = sum(r.token_usage for r in self.results) / total
        total_cost = sum(r.cost for r in self.results)
        
        return {
            "total_tasks": total,
            "success_rate": f"{success/total*100:.1f}%",
            "avg_score": f"{avg_score:.2f}",
            "avg_tokens": f"{avg_tokens:.0f}",
            "total_cost": f"",
        }
`

## 2. Trace 系统

`python
import uuid
from contextlib import contextmanager


@dataclass
class TraceSpan:
    \"\"\"追踪跨度\"\"\"
    span_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    parent_id: str = ""
    name: str = ""
    start_time: float = 0.0
    end_time: float = 0.0
    attributes: Dict[str, Any] = field(default_factory=dict)
    events: List[Dict] = field(default_factory=list)
    status: str = "ok"
    
    @property
    def duration_ms(self) -> float:
        return (self.end_time - self.start_time) * 1000


class Tracer:
    \"\"\"追踪器\"\"\"
    
    def __init__(self):
        self.spans: List[TraceSpan] = []
        self.current_span: Optional[TraceSpan] = None
        self.trace_id = str(uuid.uuid4())[:12]
    
    def start_span(self, name: str, attributes: Dict = None) -> TraceSpan:
        span = TraceSpan(
            name=name,
            start_time=time.time(),
            parent_id=self.current_span.span_id if self.current_span else "",
            attributes=attributes or {},
        )
        self.spans.append(span)
        self.current_span = span
        return span
    
    def end_span(self, status: str = "ok"):
        if self.current_span:
            self.current_span.end_time = time.time()
            self.current_span.status = status
            self.current_span = None
    
    def add_event(self, name: str, attributes: Dict = None):
        if self.current_span:
            self.current_span.events.append({
                "name": name,
                "time": time.time(),
                "attributes": attributes or {},
            })
    
    @contextmanager
    def span(self, name: str, **attributes):
        s = self.start_span(name, attributes)
        try:
            yield s
            self.end_span("ok")
        except Exception as e:
            self.current_span.attributes["error"] = str(e)
            self.end_span("error")
            raise
    
    def get_trace(self) -> List[Dict]:
        return [
            {
                "span_id": s.span_id,
                "parent_id": s.parent_id,
                "name": s.name,
                "duration_ms": s.duration_ms,
                "status": s.status,
                "attributes": s.attributes,
                "events": s.events,
            }
            for s in self.spans
        ]
    
    def print_trace(self):
        print(f"Trace: {self.trace_id}")
        for span in self.spans:
            indent = "  " if span.parent_id else ""
            status = "✅" if span.status == "ok" else "❌"
            print(f"{indent}{status} {span.name}: {span.duration_ms:.1f}ms")
`

## 3. 成本追踪

`python
class CostTracker:
    \"\"\"成本追踪器\"\"\"
    
    PRICE_PER_1K_TOKENS = {
        "gpt-4": {"input": 0.03, "output": 0.06},
        "gpt-3.5-turbo": {"input": 0.001, "output": 0.002},
    }
    
    def __init__(self):
        self.records: List[Dict] = []
        self.total_cost = 0.0
        self.total_tokens = 0
    
    def record(self, model: str, input_tokens: int, output_tokens: int, operation: str = ""):
        prices = self.PRICE_PER_1K_TOKENS.get(model, {"input": 0.01, "output": 0.02})
        cost = (input_tokens * prices["input"] + output_tokens * prices["output"]) / 1000
        
        self.records.append({
            "model": model,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "cost": cost,
            "operation": operation,
            "timestamp": time.time(),
        })
        
        self.total_cost += cost
        self.total_tokens += input_tokens + output_tokens
        
        return cost
    
    def get_summary(self) -> Dict:
        return {
            "total_calls": len(self.records),
            "total_tokens": self.total_tokens,
            "total_cost": f"",
            "avg_cost_per_call": f"",
        }
    
    def get_by_model(self) -> Dict:
        by_model = {}
        for r in self.records:
            m = r["model"]
            if m not in by_model:
                by_model[m] = {"calls": 0, "tokens": 0, "cost": 0}
            by_model[m]["calls"] += 1
            by_model[m]["tokens"] += r["input_tokens"] + r["output_tokens"]
            by_model[m]["cost"] += r["cost"]
        return by_model
`

## 4. 可观测性面板

`python
class ObservabilityPanel:
    \"\"\"可观测性面板\"\"\"
    
    def __init__(self):
        self.tracer = Tracer()
        self.evaluator = AgentEvaluator()
        self.cost_tracker = CostTracker()
        self.events: List[Dict] = []
    
    def log_event(self, event_type: str, data: Dict):
        self.events.append({
            "type": event_type,
            "data": data,
            "timestamp": time.time(),
        })
    
    def get_dashboard(self) -> Dict:
        return {
            "traces": len(self.tracer.spans),
            "evaluations": self.evaluator.get_summary(),
            "costs": self.cost_tracker.get_summary(),
            "recent_events": self.events[-10:],
        }
    
    def print_dashboard(self):
        dash = self.get_dashboard()
        print("=" * 50)
        print("📊 Agent 可观测性面板")
        print("=" * 50)
        print(f"  追踪数: {dash['traces']}")
        print(f"  评估: {dash['evaluations']}")
        print(f"  成本: {dash['costs']}")
        print(f"  最近事件: {len(dash['recent_events'])}")
`

## 5. 常见错误

1. **不记录 Trace**：出了问题没法排查 → 必须记录关键步骤
2. **成本不追踪**：月底才发现花了巨款 → 实时追踪
3. **评估太主观**：只看"感觉"好不好 → 用量化指标
4. **没有基线**：不知道改进了多少 → 记录初始评估结果
5. **日志太少**：调试时没信息 → 增加关键日志

## 6. 动手练习

### 练习 1：实现评估器
### 练习 2：实现追踪器
### 练习 3：实现成本追踪
