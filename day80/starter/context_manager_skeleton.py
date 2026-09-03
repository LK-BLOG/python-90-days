# Day 80 - Starter: 上下文管理系统骨架
# 你的任务：补全所有标记为 TODO 的部分

from typing import List, Dict, Optional, Callable
from abc import ABC, abstractmethod
import re


class TokenCounter:
    """Token计数器"""

    def __init__(self, method: str = "approximate"):
        """
        method: "approximate" 或 "tiktoken"
        """
        self.method = method
        self._tiktoken_encoding = None

        if method == "tiktoken":
            try:
                import tiktoken
                self._tiktoken_encoding = tiktoken.get_encoding("cl100k_base")
            except ImportError:
                print("tiktoken未安装，回退到近似计数")
                self.method = "approximate"

    def count(self, text: str) -> int:
        """计算文本的Token数"""
        if self.method == "tiktoken" and self._tiktoken_encoding:
            return len(self._tiktoken_encoding.encode(text))
        # TODO: 实现字符级近似计数
        # ASCII字符约4个=1token，非ASCII约1.5个=1token
        pass


class TokenBudget:
    """Token预算分配器"""

    def __init__(self, total: int):
        self.total = total
        self.allocations: Dict[str, int] = {}
        self.usage: Dict[str, int] = {}

    def allocate(self, name: str, ratio: float):
        """按比例分配预算"""
        # TODO: 计算并存储分配量
        pass

    def used(self, name: str) -> int:
        """返回已使用的Token数"""
        # TODO
        pass

    def remaining(self, name: str) -> int:
        """返回剩余可用Token数"""
        # TODO
        pass

    def record_usage(self, name: str, tokens: int):
        """记录使用量"""
        # TODO
        pass


class CompressionStrategy(ABC):
    """压缩策略基类"""

    @abstractmethod
    def compress(self, messages: List[Dict], target_tokens: int, count_fn: Callable) -> List[Dict]:
        """压缩消息列表到目标Token数以内"""
        pass


class SummaryCompression(CompressionStrategy):
    """摘要压缩策略"""

    def __init__(self, llm_fn: Optional[Callable] = None):
        self.llm_fn = llm_fn

    def compress(self, messages, target_tokens, count_fn):
        """
        TODO:
        1. 将消息分为"保留区"（最近30%）和"压缩区"
        2. 对压缩区生成摘要（用llm_fn或简单截断）
        3. 返回 [摘要消息] + 保留区
        """
        pass


class TruncationCompression(CompressionStrategy):
    """截断压缩策略"""

    def compress(self, messages, target_tokens, count_fn):
        """
        TODO:
        从最新的消息开始保留，直到达到target_tokens
        """
        pass


class SystemPromptBuilder:
    """System Prompt模板构建器"""

    def __init__(self, template: str):
        self.template = template
        self.variables: Dict[str, str] = {}
        self.conditionals: Dict[str, bool] = {}

    def set_var(self, key: str, value: str) -> 'SystemPromptBuilder':
        # TODO
        pass

    def set_conditional(self, name: str, enabled: bool) -> 'SystemPromptBuilder':
        # TODO
        pass

    def build(self) -> str:
        """
        TODO:
        1. 替换  格式的变量
        2. 处理 [[IF name]] ... [[ENDIF]] 条件块
        3. 清理多余空行并返回
        """
        pass


class ContextManager:
    """
    生产级上下文管理器
    整合所有组件：预算 + 压缩 + 窗口 + 注入
    """

    def __init__(self, total_token_budget: int, counter_method: str = "approximate"):
        self.counter = TokenCounter(counter_method)
        self.budget = TokenBudget(total_token_budget)

        # 设置默认预算分配
        # TODO: 分配 system(8%), tools(12%), memory(5%), history(65%), current(10%)

        self.system_prompt: str = ""
        self.tool_definitions: List[Dict] = []
        self.working_memory: Dict[str, str] = {}
        self.conversation_history: List[Dict] = []
        self.compression_strategy: Optional[CompressionStrategy] = None

    def set_system_prompt(self, prompt: str):
        self.system_prompt = prompt

    def set_tools(self, tools: List[Dict]):
        self.tool_definitions = tools

    def add_memory(self, key: str, value: str):
        """添加工作记忆"""
        # TODO
        pass

    def add_message(self, role: str, content: str):
        """添加对话消息"""
        # TODO
        pass

    def set_compression(self, strategy: CompressionStrategy):
        """设置压缩策略"""
        self.compression_strategy = strategy

    def build_context(self) -> List[Dict]:
        """
        TODO: 构建最终发给LLM的消息列表

        步骤:
        1. 添加system prompt
        2. 添加工作记忆（如有）
        3. 计算历史可用Token
        4. 如果历史超限，用压缩策略压缩
        5. 添加对话历史（窗口裁剪后）
        6. 返回完整消息列表
        """
        pass

    def get_stats(self) -> Dict:
        """返回上下文统计信息"""
        # TODO: 返回各区域的Token使用情况
        pass


# ===== 测试 =====
if __name__ == "__main__":
    manager = ContextManager(10000)
    manager.set_system_prompt("你是一个测试助手。")

    # 添加对话
    for i in range(20):
        role = "user" if i % 2 == 0 else "assistant"
        manager.add_message(role, f"这是第{i+1}轮对话，内容" * 10)

    # 构建上下文
    context = manager.build_context()
    print(f"构建了 {len(context)} 条消息")
    print(f"统计: {manager.get_stats()}")
