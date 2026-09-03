"""
Challenge 05: 通用 LLM 客户端 (Boss)
将 Token 计数、多轮对话、参数调优、流式输出整合为统一客户端。
"""
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Generator
import time
import threading


@dataclass
class UsageStats:
    """Token 用量统计"""
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    estimated_cost: float = 0.0


@dataclass
class ChatMessage:
    """对话消息"""
    role: str
    content: str


class LLMClient:
    """通用 LLM 客户端"""

    # 模型价格表（每 1K tokens）
    PRICING = {
        "gpt-4": {"input": 0.03, "output": 0.06},
        "gpt-3.5-turbo": {"input": 0.001, "output": 0.002},
    }

    def __init__(self, model: str = "gpt-3.5-turbo",
                 max_tokens_budget: int = 4000,
                 max_retries: int = 3,
                 temperature: float = 0.7):
        self.model = model
        self.max_tokens_budget = max_tokens_budget
        self.max_retries = max_retries
        self.temperature = temperature
        self.history: List[ChatMessage] = []
        self.stats = UsageStats()
        self._lock = threading.Lock()

    # ---- Token 计数 ----
    def count_tokens(self, text: str) -> int:
        """估算 token 数（简易规则：中文每字1 token，英文每词1 token）"""
        # TODO: 实现 token 计数
        pass

    def fit_to_budget(self, messages: List[ChatMessage]) -> List[ChatMessage]:
        """确保消息总 token 不超过预算"""
        # TODO: 从最新消息开始保留，直到超出预算
        pass

    # ---- 对话管理 ----
    def add_message(self, role: str, content: str):
        """添加消息到历史"""
        # TODO:
        pass

    def get_messages(self, system_prompt: str = None) -> List[Dict]:
        """获取格式化消息列表"""
        # TODO: 返回 OpenAI 格式的消息列表
        pass

    def clear_history(self):
        """清空对话历史"""
        # TODO:
        pass

    # ---- 核心调用 ----
    def chat(self, user_input: str, system_prompt: str = None) -> Dict:
        """
        发送消息并获取完整回复。
        返回: {"reply": str, "usage": dict}
        """
        # TODO: 实现完整流程
        # 1. 添加用户消息
        # 2. 构建消息列表（含 system prompt）
        # 3. fit_to_budget
        # 4. 调用 LLM（带重试）
        # 5. 添加助手回复到历史
        # 6. 更新统计
        # 7. 返回结果
        pass

    def stream(self, user_input: str, system_prompt: str = None) -> Generator[str, None, None]:
        """流式输出（逐 token）"""
        # TODO: 实现流式调用
        yield ""

    def batch(self, inputs: List[str], system_prompt: str = None) -> List[Dict]:
        """批量并发调用"""
        # TODO: 使用 threading 或 asyncio 并发处理
        pass

    # ---- 内部方法 ----
    def _call_llm(self, messages: List[Dict], stream: bool = False):
        """实际调用 LLM API（带重试）"""
        # TODO: 实现指数退避重试
        pass

    def _update_stats(self, usage: Dict):
        """更新用量统计"""
        # TODO: 线程安全地更新 stats
        pass

    def _estimate_cost(self, usage: Dict) -> float:
        """估算本次调用费用"""
        # TODO: 根据模型价格表计算
        pass


# 测试
if __name__ == "__main__":
    client = LLMClient(model="gpt-3.5-turbo")
    print(f"Token 计数: {client.count_tokens('Hello World 你好世界')}")
    print(f"客户端初始化完成: model={client.model}")
