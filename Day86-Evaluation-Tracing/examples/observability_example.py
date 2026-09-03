'''
Day 86 示例：可观测性系统
'''

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
import time


@dataclass
class Span:
    '''追踪 Span'''
    name: str
    start_time: float = field(default_factory=time.time)
    end_time: float | None = None
    attributes: dict = field(default_factory=dict)
    
    def finish(self):
        self.end_time = time.time()
    
    @property
    def duration(self) -> float:
        if self.end_time:
            return self.end_time - self.start_time
        return 0.0


class Tracer:
    '''简易追踪器'''
    
    def __init__(self):
        self.spans: list[Span] = []
        self.current: Span | None = None
    
    def start(self, name: str) -> Span:
        '''开始追踪'''
        span = Span(name=name)
        self.spans.append(span)
        self.current = span
        return span
    
    def end(self):
        '''结束追踪'''
        if self.current:
            self.current.finish()
            self.current = None
    
    def get_summary(self) -> dict:
        '''获取摘要'''
        return {
            "total_spans": len(self.spans),
            "total_duration": sum(s.duration for s in self.spans),
            "avg_duration": sum(s.duration for s in self.spans) / len(self.spans) if self.spans else 0
        }


class MetricsCollector:
    '''指标收集器'''
    
    def __init__(self):
        self.metrics: dict[str, list[float]] = {}
    
    def record(self, name: str, value: float):
        '''记录指标'''
        if name not in self.metrics:
            self.metrics[name] = []
        self.metrics[name].append(value)
    
    def get_average(self, name: str) -> float:
        '''获取平均值'''
        values = self.metrics.get(name, [])
        return sum(values) / len(values) if values else 0.0
    
    def get_summary(self) -> dict:
        '''获取摘要'''
        summary = {}
        for name, values in self.metrics.items():
            summary[name] = {
                "count": len(values),
                "avg": sum(values) / len(values) if values else 0,
                "min": min(values) if values else 0,
                "max": max(values) if values else 0
            }
        return summary


class CostTracker:
    '''成本追踪器'''
    
    def __init__(self, budget: float = 10.0):
        self.budget = budget
        self.costs: list[dict] = []
    
    def track(self, operation: str, cost: float):
        '''追踪成本'''
        self.costs.append({
            "operation": operation,
            "cost": cost,
            "timestamp": datetime.now().isoformat()
        })
    
    def get_total(self) -> float:
        '''获取总成本'''
        return sum(c["cost"] for c in self.costs)
    
    def check_budget(self) -> bool:
        '''检查预算'''
        return self.get_total() <= self.budget


def main():
    '''演示可观测性系统'''
    print("=" * 60)
    print("可观测性系统演示")
    print("=" * 60)
    
    # 追踪器
    print("\n1. 追踪系统:")
    tracer = Tracer()
    
    tracer.start("agent_think")
    time.sleep(0.1)
    tracer.end()
    
    tracer.start("agent_act")
    time.sleep(0.05)
    tracer.end()
    
    summary = tracer.get_summary()
    print(f"   总Span数: {summary['total_spans']}")
    print(f"   总耗时: {summary['total_duration']:.3f}秒")
    print(f"   平均耗时: {summary['avg_duration']:.3f}秒")
    
    # 指标收集
    print("\n2. 指标收集:")
    metrics = MetricsCollector()
    
    for i in range(5):
        metrics.record("response_time", 0.1 + i * 0.02)
        metrics.record("token_count", 100 + i * 10)
    
    summary = metrics.get_summary()
    print(f"   响应时间: {summary['response_time']}")
    print(f"   Token数: {summary['token_count']}")
    
    # 成本追踪
    print("\n3. 成本追踪:")
    cost_tracker = CostTracker(budget=1.0)
    
    cost_tracker.track("api_call_1", 0.002)
    cost_tracker.track("api_call_2", 0.003)
    cost_tracker.track("api_call_3", 0.001)
    
    print(f"   总成本: ")
    print(f"   预算剩余: ")
    print(f"   预算充足: {cost_tracker.check_budget()}")
    
    print("\n" + "=" * 60)
    print("演示完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
