"""Day 82 Example 01: Agent状态机基础"""
from enum import Enum, auto
from typing import Dict, Callable, Optional
import time


class AgentState(Enum):
    """Agent状态枚举"""
    IDLE = auto()
    THINKING = auto()
    TOOL_CALLING = auto()
    WAITING_INPUT = auto()
    ERROR = auto()
    DONE = auto()


class Transition:
    """状态转换定义"""
    def __init__(self, from_state, event, to_state, guard=None, effect=None):
        self.from_state = from_state
        self.event = event
        self.to_state = to_state
        self.guard = guard      # 守卫条件
        self.effect = effect    # 副作用回调

    def __repr__(self):
        return f"{self.from_state.name} --[{self.event}]--> {self.to_state.name}"


class AgentStateMachine:
    """Agent有限状态机"""

    def __init__(self, name: str = "agent"):
        self.name = name
        self.state = AgentState.IDLE
        self.transitions_map: Dict[tuple, Transition] = {}
        self.history: list = []
        self._on_enter: Dict[AgentState, list] = {}
        self._on_exit: Dict[AgentState, list] = {}

    def add_transition(self, from_state: AgentState, event: str,
                       to_state: AgentState, guard=None, effect=None):
        """注册状态转换规则"""
        t = Transition(from_state, event, to_state, guard, effect)
        self.transitions_map[(from_state, event)] = t
        return self

    def on_enter(self, state: AgentState, callback: Callable):
        """注册进入状态回调"""
        self._on_enter.setdefault(state, []).append(callback)
        return self

    def on_exit(self, state: AgentState, callback: Callable):
        """注册退出状态回调"""
        self._on_exit.setdefault(state, []).append(callback)
        return self

    def send_event(self, event: str) -> AgentState:
        """发送事件，触发状态转换"""
        key = (self.state, event)
        if key not in self.transitions_map:
            raise ValueError(
                f"[{self.name}] 非法转换: {self.state.name} + '{event}'"
            )

        transition = self.transitions_map[key]

        # 检查守卫条件
        if transition.guard and not transition.guard():
            raise PermissionError(
                f"[{self.name}] 守卫条件拒绝: {self.state.name} + '{event}'"
            )

        old_state = self.state

        # 退出回调
        for cb in self._on_exit.get(old_state, []):
            cb(old_state, event)

        # 执行副作用
        if transition.effect:
            transition.effect(old_state, transition.to_state, event)

        # 状态切换
        self.state = transition.to_state

        # 记录历史
        self.history.append({
            "from": old_state.name,
            "event": event,
            "to": self.state.name,
            "timestamp": time.time()
        })

        # 进入回调
        for cb in self._on_enter.get(self.state, []):
            cb(self.state, event)

        return self.state

    def get_legal_events(self) -> list:
        """获取当前状态下所有合法事件"""
        return [
            key[1] for key in self.transitions_map
            if key[0] == self.state
        ]

    def print_history(self):
        """打印状态转换历史"""
        print(f"\n{'='*50}")
        print(f"[{self.name}] 状态转换历史")
        print(f"{'='*50}")
        for i, h in enumerate(self.history, 1):
            print(f"  {i}. {h['from']} --[{h['event']}]--> {h['to']}")


def demo():
    """演示状态机使用"""
    # 创建状态机
    fsm = AgentStateMachine("demo-agent")

    # 注册转换规则
    fsm.add_transition(AgentState.IDLE, "user_message", AgentState.THINKING)
    fsm.add_transition(AgentState.THINKING, "need_tool", AgentState.TOOL_CALLING)
    fsm.add_transition(AgentState.THINKING, "answer_ready", AgentState.DONE)
    fsm.add_transition(AgentState.THINKING, "need_input", AgentState.WAITING_INPUT)
    fsm.add_transition(AgentState.TOOL_CALLING, "tool_result", AgentState.THINKING)
    fsm.add_transition(AgentState.TOOL_CALLING, "tool_error", AgentState.ERROR)
    fsm.add_transition(AgentState.WAITING_INPUT, "user_message", AgentState.THINKING)
    fsm.add_transition(AgentState.ERROR, "retry", AgentState.THINKING)

    # 注册回调
    fsm.on_enter(AgentState.THINKING, lambda s, e: print(f"  >> 开始思考..."))
    fsm.on_enter(AgentState.TOOL_CALLING, lambda s, e: print(f"  >> 调用工具..."))
    fsm.on_enter(AgentState.DONE, lambda s, e: print(f"  >> 任务完成!"))
    fsm.on_exit(AgentState.THINKING, lambda s, e: print(f"  << 退出思考"))

    # 模拟对话流程
    print("=== Agent状态机演示 ===\n")

    fsm.send_event("user_message")      # IDLE -> THINKING
    print(f"当前状态: {fsm.state.name}")

    fsm.send_event("need_tool")         # THINKING -> TOOL_CALLING
    print(f"当前状态: {fsm.state.name}")

    fsm.send_event("tool_result")       # TOOL_CALLING -> THINKING
    print(f"当前状态: {fsm.state.name}")

    fsm.send_event("answer_ready")      # THINKING -> DONE
    print(f"当前状态: {fsm.state.name}")

    fsm.print_history()
    print(f"\n合法事件: {fsm.get_legal_events()}")


if __name__ == "__main__":
    demo()
