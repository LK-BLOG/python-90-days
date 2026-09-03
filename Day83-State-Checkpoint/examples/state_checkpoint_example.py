'''
Day 83 示例：状态与检查点系统
'''

from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
from typing import Any
import json


class AgentState(Enum):
    '''Agent状态'''
    IDLE = "idle"
    THINKING = "thinking"
    ACTING = "acting"
    OBSERVING = "observing"
    COMPLETED = "completed"
    ERROR = "error"


class StateManager:
    '''状态管理器'''
    
    def __init__(self):
        self.current_state: AgentState = AgentState.IDLE
        self.state_data: dict[str, Any] = {}
        self.history: list[dict] = []
    
    def transition(self, to_state: AgentState, trigger: str):
        '''状态转换'''
        self.history.append({
            "from": self.current_state.value,
            "to": to_state.value,
            "trigger": trigger,
            "timestamp": datetime.now().isoformat()
        })
        self.current_state = to_state
    
    def set_data(self, key: str, value: Any):
        '''设置状态数据'''
        self.state_data[key] = value
    
    def get_data(self, key: str, default: Any = None) -> Any:
        '''获取状态数据'''
        return self.state_data.get(key, default)
    
    def to_dict(self) -> dict:
        '''转换为字典'''
        return {
            "current_state": self.current_state.value,
            "state_data": self.state_data,
            "history": self.history[-5:]
        }
    
    def from_dict(self, data: dict):
        '''从字典恢复'''
        self.current_state = AgentState(data["current_state"])
        self.state_data = data.get("state_data", {})
        self.history = data.get("history", [])


class CheckpointManager:
    '''检查点管理器'''
    
    def __init__(self):
        self.checkpoints: list[dict] = []
    
    def save(self, state_manager: StateManager, step_name: str):
        '''保存检查点'''
        checkpoint = {
            "id": len(self.checkpoints),
            "step": step_name,
            "state": state_manager.to_dict(),
            "timestamp": datetime.now().isoformat()
        }
        self.checkpoints.append(checkpoint)
        print(f"保存检查点: {step_name}")
        return checkpoint["id"]
    
    def load(self, checkpoint_id: int) -> dict | None:
        '''加载检查点'''
        if 0 <= checkpoint_id < len(self.checkpoints):
            return self.checkpoints[checkpoint_id]
        return None
    
    def get_latest(self) -> dict | None:
        '''获取最新检查点'''
        if self.checkpoints:
            return self.checkpoints[-1]
        return None


def main():
    '''演示状态与检查点系统'''
    print("=" * 60)
    print("状态与检查点系统演示")
    print("=" * 60)
    
    state_manager = StateManager()
    checkpoint_mgr = CheckpointManager()
    
    # 模拟任务执行
    print("\n1. 开始任务:")
    state_manager.transition(AgentState.THINKING, "开始分析任务")
    print(f"   状态: {state_manager.current_state.value}")
    
    # 保存检查点
    checkpoint_mgr.save(state_manager, "分析完成")
    
    # 执行步骤
    steps = ["步骤1: 搜索信息", "步骤2: 处理数据", "步骤3: 生成结果"]
    
    for i, step in enumerate(steps):
        print(f"\n   执行: {step}")
        state_manager.transition(AgentState.ACTING, step)
        state_manager.set_data(f"step_{i}_result", f"{step}的完成结果")
        
        # 每步保存检查点
        checkpoint_mgr.save(state_manager, step)
    
    # 完成
    state_manager.transition(AgentState.COMPLETED, "任务完成")
    print(f"\n最终状态: {state_manager.current_state.value}")
    
    # 显示检查点历史
    print("\n2. 检查点历史:")
    for cp in checkpoint_mgr.checkpoints:
        print(f"   [{cp['id']}] {cp['step']} - {cp['timestamp']}")
    
    # 模拟恢复
    print("\n3. 从检查点恢复:")
    latest = checkpoint_mgr.get_latest()
    if latest:
        restored_state = StateManager()
        restored_state.from_dict(latest["state"])
        print(f"   恢复状态: {restored_state.current_state.value}")
        print(f"   状态数据: {restored_state.state_data}")
    
    print("\n" + "=" * 60)
    print("演示完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
