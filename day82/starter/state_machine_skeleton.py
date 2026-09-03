"""Day 82 骨架: Agent状态机 - 请实现以下类"""

from enum import Enum, auto
from typing import Dict, Callable, Optional, Any


class AgentState(Enum):
    """Agent状态"""
    IDLE = auto()
    THINKING = auto()
    TOOL_CALLING = auto()
    WAITING = auto()
    ERROR = auto()
    DONE = auto()


class AgentStateMachine:
    """Agent有限状态机 - 请实现"""

    def __init__(self, name: str = "agent"):
        self.name = name
        self.state = AgentState.IDLE
        self.transitions: Dict[tuple, AgentState] = {}
        self.history: list = []

    def add_transition(self, from_state: AgentState, event: str, to_state: AgentState):
        """注册状态转换规则"""
        # TODO: 实现
        pass

    def send_event(self, event: str) -> AgentState:
        """发送事件触发状态转换"""
        # TODO: 实现
        # 1. 检查转换是否合法
        # 2. 记录历史
        # 3. 执行转换
        # 4. 返回新状态
        pass

    def get_legal_events(self) -> list:
        """获取当前状态的所有合法事件"""
        # TODO: 实现
        pass

    def print_history(self):
        """打印状态转换历史"""
        # TODO: 实现
        pass
