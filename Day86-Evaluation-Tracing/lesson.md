# Day 86 课程：Evaluation & Tracing

## 1. Agent评估方法

`python
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable
from enum import Enum
import time


class MetricType(Enum):
    '''指标类型'''
    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"


@dataclass
class EvaluationResult:
    '''评估结果'''
    metric_name: str
    value: float
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: dict = field(default_factory=dict)


class AgentEvaluator:
    '''Agent评估器'''
    
    def __init__(self):
        self.metrics: dict[str, list[float]] = {}
        self.evaluations: list[EvaluationResult] = []
    
    def track_metric(self, name: str, value: float, metadata: dict = None):
        '''追踪指标'''
        if name not in self.metrics:
            self.metrics[name] = []
        self.metrics[name].append(value)
        
        result = EvaluationResult(
            metric_name=name,
            value=value,
            metadata=metadata or {}
        )
        self.evaluations.append(result)
    
    def get_average(self, metric_name: str) -> float:
        '''获取平均值'''
        values = self.metrics.get(metric_name, [])
        return sum(values) / len(values) if values else 0.0
    
    def get_summary(self) -> dict:
        '''获取摘要'''
        summary = {}
        for name, values in self.metrics.items():
            if values:
                summary[name] = {
                    "count": len(values),
                    "mean": sum(values) / len(values),
                    "min": min(values),
                    "max": max(values),
                    "latest": values[-1]
                }
        return summary


class ResponseTimeTracker:
    '''响应时间追踪器'''
    
    def __init__(self):
        self.evaluator = AgentEvaluator()
    
    def track(self, func: Callable):
        '''追踪函数执行时间'''
        async def wrapper(*args, **kwargs):
            start = time.time()
            result = await func(*args, **kwargs)
            duration = time.time() - start
            
            self.evaluator.track_metric("response_time", duration, {
                "function": func.__name__
            })
            
            return result
        return wrapper
    
    def get_average_response_time(self) -> float:
        '''获取平均响应时间'''
        return self.evaluator.get_average("response_time")


class TokenCounter:
    '''Token计数器'''
    
    def __init__(self, cost_per_1k_input: float = 0.002, cost_per_1k_output: float = 0.002):
        self.cost_per_1k_input = cost_per_1k_input
        self.cost_per_1k_output = cost_per_1k_output
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.evaluator = AgentEvaluator()
    
    def count(self, input_tokens: int, output_tokens: int, model: str = "default"):
        '''计数Token'''
        self.total_input_tokens += input_tokens
        self.total_output_tokens += output_tokens
        
        cost = self.calculate_cost(input_tokens, output_tokens)
        
        self.evaluator.track_metric("token_cost", cost, {
            "model": model,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens
        })
    
    def calculate_cost(self, input_tokens: int, output_tokens: int) -> float:
        '''计算成本'''
        input_cost = (input_tokens / 1000) * self.cost_per_1k_input
        output_cost = (output_tokens / 1000) * self.cost_per_1k_output
        return input_cost + output_cost
    
    def get_total_cost(self) -> float:
        '''获取总成本'''
        return sum(self.evaluator.metrics.get("token_cost", [0]))
`

## 2. Trace系统

`python
import uuid
from typing import Optional


@dataclass
class Span:
    '''追踪 Span'''
    trace_id: str
    span_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    parent_span_id: str | None = None
    name: str = ""
    start_time: datetime = field(default_factory=datetime.now)
    end_time: datetime | None = None
    attributes: dict[str, Any] = field(default_factory=dict)
    events: list[dict] = field(default_factory=list)
    status: str = "ok"
    
    def finish(self, status: str = "ok"):
        '''结束 Span'''
        self.end_time = datetime.now()
        self.status = status
    
    def add_event(self, name: str, attributes: dict = None):
        '''添加事件'''
        self.events.append({
            "name": name,
            "timestamp": datetime.now().isoformat(),
            "attributes": attributes or {}
        })
    
    @property
    def duration(self) -> float:
        '''持续时间（秒）'''
        if self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return 0.0


@dataclass
class Trace:
    '''追踪'''
    trace_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    spans: list[Span] = field(default_factory=list)
    start_time: datetime = field(default_factory=datetime.now)
    end_time: datetime | None = None
    attributes: dict[str, Any] = field(default_factory=dict)
    
    def add_span(self, span: Span):
        '''添加 Span'''
        self.spans.append(span)
    
    def finish(self):
        '''结束追踪'''
        self.end_time = datetime.now()
    
    def get_duration(self) -> float:
        '''获取总持续时间'''
        if self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return 0.0


class Tracer:
    '''追踪器'''
    
    def __init__(self):
        self.traces: list[Trace] = []
        self.current_trace: Trace | None = None
        self.span_stack: list[Span] = []
    
    def start_trace(self, name: str) -> Trace:
        '''开始追踪'''
        trace = Trace(name=name)
        self.traces.append(trace)
        self.current_trace = trace
        return trace
    
    def start_span(self, name: str, attributes: dict = None) -> Span:
        '''开始 Span'''
        if not self.current_trace:
            self.start_trace("auto")
        
        parent_id = self.span_stack[-1].span_id if self.span_stack else None
        
        span = Span(
            trace_id=self.current_trace.trace_id,
            parent_span_id=parent_id,
            name=name,
            attributes=attributes or {}
        )
        
        self.current_trace.add_span(span)
        self.span_stack.append(span)
        
        return span
    
    def end_span(self, status: str = "ok"):
        '''结束 Span'''
        if self.span_stack:
            span = self.span_stack.pop()
            span.finish(status)
    
    def end_trace(self):
        '''结束追踪'''
        if self.current_trace:
            self.current_trace.finish()
            self.current_trace = None
    
    def get_trace(self, trace_id: str) -> Trace | None:
        '''获取追踪'''
        for trace in self.traces:
            if trace.trace_id == trace_id:
                return trace
        return None
    
    def export_traces(self) -> list[dict]:
        '''导出追踪数据'''
        result = []
        for trace in self.traces:
            trace_data = {
                "trace_id": trace.trace_id,
                "name": trace.name,
                "start_time": trace.start_time.isoformat(),
                "end_time": trace.end_time.isoformat() if trace.end_time else None,
                "duration": trace.get_duration(),
                "spans": [
                    {
                        "span_id": span.span_id,
                        "parent_span_id": span.parent_span_id,
                        "name": span.name,
                        "start_time": span.start_time.isoformat(),
                        "end_time": span.end_time.isoformat() if span.end_time else None,
                        "duration": span.duration,
                        "status": span.status,
                        "attributes": span.attributes
                    }
                    for span in trace.spans
                ]
            }
            result.append(trace_data)
        
        return result
`

## 3. 可观测性系统

`python
import logging
from collections import defaultdict


class ObservabilitySystem:
    '''可观测性系统'''
    
    def __init__(self, service_name: str = "agent"):
        self.service_name = service_name
        self.logger = self._setup_logger()
        self.tracer = Tracer()
        self.evaluator = AgentEvaluator()
        self.token_counter = TokenCounter()
    
    def _setup_logger(self) -> logging.Logger:
        '''设置日志'''
        logger = logging.getLogger(self.service_name)
        logger.setLevel(logging.DEBUG)
        
        # 控制台输出
        handler = logging.StreamHandler()
        handler.setLevel(logging.INFO)
        
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        
        logger.addHandler(handler)
        
        return logger
    
    def log(self, level: str, message: str, **kwargs):
        '''记录日志'''
        log_func = getattr(self.logger, level.lower())
        log_func(f"{message} {kwargs if kwargs else ''}")
    
    def trace(self, name: str):
        '''追踪上下文管理器'''
        return self.tracer.start_span(name)
    
    def record_metric(self, name: str, value: float, **tags):
        '''记录指标'''
        self.evaluator.track_metric(name, value, tags)
    
    def count_tokens(self, input_tokens: int, output_tokens: int, model: str = "default"):
        '''计数Token'''
        self.token_counter.count(input_tokens, output_tokens, model)
    
    def get_dashboard(self) -> dict:
        '''获取仪表板数据'''
        return {
            "service": self.service_name,
            "metrics_summary": self.evaluator.get_summary(),
            "total_cost": self.token_counter.get_total_cost(),
            "total_traces": len(self.tracer.traces),
            "total_spans": sum(len(t.spans) for t in self.tracer.traces)
        }
`

## 4. LangSmith/Phoenix基础

`python
class LangSmithIntegration:
    '''LangSmith集成（模拟）'''
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        self.runs: list[dict] = []
    
    def create_run(self, name: str, run_type: str = "chain") -> str:
        '''创建运行'''
        run_id = str(uuid.uuid4())
        self.runs.append({
            "run_id": run_id,
            "name": name,
            "run_type": run_type,
            "start_time": datetime.now().isoformat(),
            "status": "started"
        })
        return run_id
    
    def end_run(self, run_id: str, status: str = "success", output: Any = None):
        '''结束运行'''
        for run in self.runs:
            if run["run_id"] == run_id:
                run["end_time"] = datetime.now().isoformat()
                run["status"] = status
                run["output"] = str(output)[:1000] if output else None
                break
    
    def get_runs(self) -> list[dict]:
        '''获取所有运行'''
        return self.runs


class PhoenixIntegration:
    '''Phoenix集成（模拟）'''
    
    def __init__(self):
        self.traces: list[dict] = []
    
    def ingest_trace(self, trace_data: dict):
        '''摄入追踪数据'''
        self.traces.append(trace_data)
    
    def query_traces(self, filter_criteria: dict = None) -> list[dict]:
        '''查询追踪'''
        if not filter_criteria:
            return self.traces
        # 简单过滤
        return self.traces  # 实际实现中应该有过滤逻辑
`

## 5. 成本追踪

`python
class CostTracker:
    '''成本追踪器'''
    
    def __init__(self):
        self.costs: list[dict] = []
        self.budget: float | None = None
    
    def set_budget(self, budget: float):
        '''设置预算'''
        self.budget = budget
    
    def track_cost(
        self, 
        operation: str, 
        cost: float, 
        metadata: dict = None
    ):
        '''追踪成本'''
        self.costs.append({
            "operation": operation,
            "cost": cost,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        })
        
        # 检查预算
        if self.budget and self.get_total_cost() > self.budget:
            print(f"警告：已超出预算！当前: , 预算: ")
    
    def get_total_cost(self) -> float:
        '''获取总成本'''
        return sum(c["cost"] for c in self.costs)
    
    def get_cost_by_operation(self) -> dict:
        '''按操作统计成本'''
        costs_by_op = defaultdict(float)
        for cost in self.costs:
            costs_by_op[cost["operation"]] += cost["cost"]
        return dict(costs_by_op)
    
    def get_report(self) -> dict:
        '''获取成本报告'''
        return {
            "total_cost": self.get_total_cost(),
            "budget": self.budget,
            "remaining": self.budget - self.get_total_cost() if self.budget else None,
            "by_operation": self.get_cost_by_operation(),
            "num_transactions": len(self.costs)
        }
`

## 6. 本日总结

- AgentEvaluator评估Agent表现
- Tracer实现分布式追踪
- ObservabilitySystem整合可观测性
- CostTracker追踪API成本
- 集成LangSmith/Phoenix

明天我们将学习Agent安全与Guardrails。
