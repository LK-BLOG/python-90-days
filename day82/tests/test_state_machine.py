"""Day 82 测试: Agent状态机"""
import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "examples"))


def test_state_transition():
    """测试基本状态转换"""
    from importlib import import_module
    mod = import_module("01_state_machine")

    fsm = mod.AgentStateMachine("test")
    fsm.add_transition(mod.AgentState.IDLE, "start", mod.AgentState.THINKING)
    fsm.add_transition(mod.AgentState.THINKING, "finish", mod.AgentState.DONE)

    assert fsm.state == mod.AgentState.IDLE
    fsm.send_event("start")
    assert fsm.state == mod.AgentState.THINKING
    fsm.send_event("finish")
    assert fsm.state == mod.AgentState.DONE


def test_invalid_transition():
    """测试非法状态转换应报错"""
    from importlib import import_module
    mod = import_module("01_state_machine")

    fsm = mod.AgentStateMachine("test")
    fsm.add_transition(mod.AgentState.IDLE, "start", mod.AgentState.THINKING)

    with pytest.raises(ValueError):
        fsm.send_event("finish")  # 非法事件


def test_history_recorded():
    """测试历史记录"""
    from importlib import import_module
    mod = import_module("01_state_machine")

    fsm = mod.AgentStateMachine("test")
    fsm.add_transition(mod.AgentState.IDLE, "go", mod.AgentState.THINKING)
    fsm.send_event("go")

    assert len(fsm.history) == 1
    assert fsm.history[0]["from"] == "IDLE"
    assert fsm.history[0]["event"] == "go"
    assert fsm.history[0]["to"] == "THINKING"


def test_legal_events():
    """测试合法事件列表"""
    from importlib import import_module
    mod = import_module("01_state_machine")

    fsm = mod.AgentStateMachine("test")
    fsm.add_transition(mod.AgentState.IDLE, "start", mod.AgentState.THINKING)
    fsm.add_transition(mod.AgentState.IDLE, "skip", mod.AgentState.DONE)

    events = fsm.get_legal_events()
    assert "start" in events
    assert "skip" in events
    assert "finish" not in events


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
