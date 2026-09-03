"""
Challenge 05: AI 应用架构 (Boss)
整合速率限制、重试、异步调用和成本追踪为完整框架。
"""
import time
import asyncio
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Callable, Any
from collections import deque
from datetime import datetime, timedelta


@dataclass
class ModelConfig:
    """模型配置"""
    name: str
    api_key: str = ""
    rpm_limit: int = 60  # 每分钟请求数
    tpm_limit: int = 90000  # 每分钟 token 数
    cost_per_1k_input: float = 0.001
    cost_per_1k_output: float = 0.002
    priority: int = 0  # 优先级，0 最高


@dataclass
class RequestMetrics:
    """请求指标"""
    model: str
    latency_ms: float
    tokens_used: int
    cost: float
    success: bool
    timestamp: str = ""


class TokenBucket:
    """令牌桶限流器"""

    def __init__(self, capacity: int, refill_rate: float):
        self.capacity = capacity
        self.tokens = capacity
        self.refill_rate = refill_rate  # tokens per second
        self.last_refill = time.time()

    def consume(self, tokens: int = 1) -> bool:
        """尝试消费令牌"""
        # TODO: 补充令牌 + 消费
        pass

    @property
    def available(self) -> int:
        return int(self.tokens)


class RetryEngine:
    """重试引擎"""

    def __init__(self, max_retries: int = 3, base_delay: float = 1.0):
        self.max_retries = max_retries
        self.base_delay = base_delay

    def execute(self, func: Callable, *args, **kwargs) -> Any:
        """带指数退避的重试执行"""
        # TODO:
        pass


class CostTracker:
    """成本追踪器"""

    def __init__(self, monthly_budget: float = 100.0):
        self.monthly_budget = monthly_budget
        self.total_cost = 0.0
        self.records: List[Dict] = []
        self.alerts: List[str] = []

    def record(self, model: str, input_tokens: int, output_tokens: int,
               cost_per_1k_in: float, cost_per_1k_out: float) -> float:
        """记录一次调用的成本"""
        # TODO: 计算费用，检查预算
        pass

    def check_budget(self) -> bool:
        """检查是否超预算"""
        # TODO:
        pass

    def get_summary(self) -> Dict:
        """获取成本汇总"""
        # TODO:
        pass


class HealthChecker:
    """健康检查器"""

    def __init__(self):
        self.status: Dict[str, bool] = {}
        self.last_check: Dict[str, str] = {}

    def check(self, model: str, check_func: Callable) -> bool:
        """检查模型健康状态"""
        # TODO:
        pass

    def get_healthy_models(self, models: List[str]) -> List[str]:
        """获取可用模型列表"""
        # TODO:
        pass


class AIAppFramework:
    """AI 应用框架"""

    def __init__(self, models: List[ModelConfig] = None,
                 monthly_budget: float = 100.0):
        self.models: Dict[str, ModelConfig] = {}
        self.buckets: Dict[str, TokenBucket] = {}
        self.retry = RetryEngine()
        self.cost_tracker = CostTracker(monthly_budget)
        self.health_checker = HealthChecker()
        self.metrics: List[RequestMetrics] = []

        if models:
            for m in models:
                self.add_model(m)

    def add_model(self, config: ModelConfig):
        """注册模型"""
        # TODO:
        pass

    def chat(self, model: str, messages: List[Dict],
             stream: bool = False) -> Dict:
        """
        统一调用接口。
        管道: 限流 → 预算检查 → 健康检查 → 重试调用 → 记录成本
        """
        # TODO:
        pass

    def _select_model(self, preferred: str) -> Optional[str]:
        """选择可用模型（支持降级）"""
        # TODO: 按优先级找可用模型
        pass

    def _call_model(self, model: str, messages: List[Dict]) -> Dict:
        """实际调用模型（模拟）"""
        # TODO: 模拟 LLM 调用
        pass

    def batch_call(self, requests: List[Dict]) -> List[Dict]:
        """批量并发调用"""
        # TODO:
        pass

    def get_metrics(self) -> Dict:
        """获取监控指标"""
        # TODO:
        pass


# 测试
if __name__ == "__main__":
    framework = AIAppFramework(models=[
        ModelConfig("gpt-4", rpm_limit=30, cost_per_1k_input=0.03, cost_per_1k_output=0.06, priority=0),
        ModelConfig("gpt-3.5-turbo", rpm_limit=60, cost_per_1k_input=0.001, cost_per_1k_output=0.002, priority=1),
    ], monthly_budget=10.0)

    result = framework.chat("gpt-4", [{"role": "user", "content": "Hello"}])
    print(f"调用结果: {result}")
    print(f"成本汇总: {framework.cost_tracker.get_summary()}")
    print(f"监控指标: {framework.get_metrics()}")
