"""
Challenge 05: AI 助手 (Boss)
整合工具注册、调用解析、多工具协调为完整助手系统。
"""
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional, Any
import re
import json


@dataclass
class Tool:
    """工具定义"""
    name: str
    description: str
    func: Callable
    parameters: Dict = field(default_factory=dict)
    fallback: Optional[str] = None  # 备用工具名


@dataclass
class ExecutionLog:
    """执行日志"""
    step: int
    thought: str
    action: str
    action_input: Dict
    observation: str
    timestamp: float = 0.0


class IntentParser:
    """意图解析器"""

    def __init__(self, tools: Dict[str, Tool]):
        self.tools = tools

    def parse(self, user_input: str) -> Dict:
        """
        解析用户输入，返回:
        {"tool": str, "params": Dict, "confidence": float}
        """
        # TODO: 基于关键词匹配的简单意图识别
        # 1. 提取用户输入中的关键信息
        # 2. 匹配最合适的工具
        # 3. 提取参数
        # 4. 返回解析结果
        pass


class AIAssistant:
    """AI 助手"""

    def __init__(self, name: str = "AI 助手"):
        self.name = name
        self.tools: Dict[str, Tool] = {}
        self.history: List[Dict] = []
        self.logs: List[ExecutionLog] = []

    # ---- 工具管理 ----
    def register_tool(self, name: str, description: str,
                      func: Callable, parameters: Dict = None,
                      fallback: str = None):
        """注册工具"""
        # TODO:
        pass

    def list_tools(self) -> List[str]:
        """列出所有可用工具"""
        # TODO:
        pass

    # ---- 核心交互 ----
    def chat(self, user_input: str) -> str:
        """
        与助手对话。
        流程: 理解意图 → 选择工具 → 提取参数 → 执行 → 汇总结果
        """
        # TODO:
        # 1. 记录用户输入到历史
        # 2. 解析意图
        # 3. 选择工具
        # 4. 提取参数
        # 5. 执行工具（失败则尝试 fallback）
        # 6. 汇总结果
        # 7. 记录执行日志
        pass

    def execute_tool(self, tool_name: str, params: Dict) -> str:
        """执行指定工具"""
        # TODO: 执行工具，捕获异常
        pass

    def _try_fallback(self, failed_tool: str, params: Dict) -> Optional[str]:
        """尝试备用工具"""
        # TODO:
        pass

    # ---- 对话管理 ----
    def get_history(self, last_n: int = None) -> List[Dict]:
        """获取对话历史"""
        # TODO:
        pass

    def clear_history(self):
        """清空历史"""
        # TODO:
        pass

    # ---- 日志 ----
    def get_logs(self) -> List[Dict]:
        """获取执行日志"""
        # TODO:
        pass

    def explain(self) -> str:
        """生成可解释性报告"""
        # TODO: 汇总所有执行步骤的 Thought/Action/Observation
        pass


# 测试
if __name__ == "__main__":
    assistant = AIAssistant("小助手")
    assistant.register_tool("calc", "数学计算", lambda expression: str(eval(expression)))
    assistant.register_tool("upper", "转大写", lambda text: text.upper())
    assistant.register_tool("reverse", "反转文字", lambda text: text[::-1])

    print("工具列表:", assistant.list_tools())
    print("执行:", assistant.execute_tool("calc", {"expression": "2**10"}))
    print("报告:\n", assistant.explain())
