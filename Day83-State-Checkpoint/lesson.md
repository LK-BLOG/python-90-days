# Day 83 课程：State & Checkpoint

## 1. Agent状态管理

`python
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
    REFLECTING = "reflecting"
    WAITING = "waiting"
    ERROR = "error"
    COMPLETED = "completed"


@dataclass
class StateTransition:
    '''状态转换'''
    from_state: AgentState
    to_state: AgentState
    trigger: str
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: dict = field(default_factory=dict)


class StateManager:
    '''状态管理器'''
    
    def __init__(self):
        self.current_state: AgentState = AgentState.IDLE
        self.state_history: list[StateTransition] = []
        self.state_data: dict[str, Any] = {}
        self.transitions: dict[AgentState, list[AgentState]] = {
            AgentState.IDLE: [AgentState.THINKING],
            AgentState.THINKING: [AgentState.ACTING, AgentState.WAITING],
            AgentState.ACTING: [AgentState.OBSERVING, AgentState.ERROR],
            AgentState.OBSERVING: [AgentState.THINKING, AgentState.REFLECTING],
            AgentState.REFLECTING: [AgentState.THINKING, AgentState.COMPLETED],
            AgentState.WAITING: [AgentState.THINKING],
            AgentState.ERROR: [AgentState.THINKING, AgentState.IDLE],
            AgentState.COMPLETED: [AgentState.IDLE]
        }
    
    def transition(self, to_state: AgentState, trigger: str, metadata: dict = None):
        '''执行状态转换'''
        # 检查转换是否合法
        valid_states = self.transitions.get(self.current_state, [])
        if to_state not in valid_states:
            raise ValueError(
                f"非法状态转换: {self.current_state.value} → {to_state.value}"
            )
        
        # 记录转换
        transition = StateTransition(
            from_state=self.current_state,
            to_state=to_state,
            trigger=trigger,
            metadata=metadata or {}
        )
        self.state_history.append(transition)
        
        # 更新状态
        self.current_state = to_state
        
        return transition
    
    def get_state_data(self, key: str, default: Any = None) -> Any:
        '''获取状态数据'''
        return self.state_data.get(key, default)
    
    def set_state_data(self, key: str, value: Any):
        '''设置状态数据'''
        self.state_data[key] = value
    
    def to_dict(self) -> dict:
        '''转换为字典'''
        return {
            "current_state": self.current_state.value,
            "state_data": self.state_data,
            "history": [
                {
                    "from": t.from_state.value,
                    "to": t.to_state.value,
                    "trigger": t.trigger,
                    "timestamp": t.timestamp.isoformat()
                }
                for t in self.state_history[-10:]  # 只保留最近10条
            ]
        }
    
    def from_dict(self, data: dict):
        '''从字典恢复'''
        self.current_state = AgentState(data["current_state"])
        self.state_data = data.get("state_data", {})
`

## 2. 状态持久化

`python
import sqlite3
from typing import Optional


class StatePersistence:
    '''状态持久化'''
    
    def __init__(self, db_path: str = "agent_state.db"):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        '''初始化数据库'''
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS checkpoints (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                agent_id TEXT NOT NULL,
                state TEXT NOT NULL,
                data TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS state_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                agent_id TEXT NOT NULL,
                from_state TEXT NOT NULL,
                to_state TEXT NOT NULL,
                trigger TEXT NOT NULL,
                metadata TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_checkpoint(self, agent_id: str, state: dict, data: dict):
        '''保存检查点'''
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO checkpoints (agent_id, state, data) VALUES (?, ?, ?)",
            (agent_id, json.dumps(state), json.dumps(data))
        )
        
        conn.commit()
        conn.close()
        
        return cursor.lastrowid
    
    def load_checkpoint(self, agent_id: str) -> Optional[dict]:
        '''加载最新检查点'''
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT state, data FROM checkpoints WHERE agent_id = ? ORDER BY id DESC LIMIT 1",
            (agent_id,)
        )
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                "state": json.loads(row[0]),
                "data": json.loads(row[1])
            }
        return None
    
    def save_state_transition(
        self, 
        agent_id: str, 
        transition: StateTransition
    ):
        '''保存状态转换'''
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO state_history (agent_id, from_state, to_state, trigger, metadata) VALUES (?, ?, ?, ?, ?)",
            (
                agent_id,
                transition.from_state.value,
                transition.to_state.value,
                transition.trigger,
                json.dumps(transition.metadata)
            )
        )
        
        conn.commit()
        conn.close()
    
    def get_state_history(self, agent_id: str, limit: int = 100) -> list[dict]:
        '''获取状态历史'''
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT from_state, to_state, trigger, metadata, created_at FROM state_history WHERE agent_id = ? ORDER BY id DESC LIMIT ?",
            (agent_id, limit)
        )
        
        rows = cursor.fetchall()
        conn.close()
        
        return [
            {
                "from_state": row[0],
                "to_state": row[1],
                "trigger": row[2],
                "metadata": json.loads(row[3]) if row[3] else {},
                "timestamp": row[4]
            }
            for row in rows
        ]
`

## 3. 检查点与恢复

`python
from typing import Callable


class CheckpointManager:
    '''检查点管理器'''
    
    def __init__(self, persistence: StatePersistence = None):
        self.persistence = persistence or StatePersistence()
        self.checkpoints: list[dict] = []
        self.current_checkpoint_id: int | None = None
    
    def save(
        self, 
        agent_id: str, 
        state: StateManager,
        additional_data: dict = None
    ) -> int:
        '''保存检查点'''
        checkpoint_data = {
            "state_manager": state.to_dict(),
            "additional_data": additional_data or {},
            "timestamp": datetime.now().isoformat()
        }
        
        checkpoint_id = self.persistence.save_checkpoint(
            agent_id,
            {"checkpoint_id": len(self.checkpoints)},
            checkpoint_data
        )
        
        self.checkpoints.append({
            "id": checkpoint_id,
            "data": checkpoint_data
        })
        
        self.current_checkpoint_id = checkpoint_id
        
        return checkpoint_id
    
    def load(
        self, 
        agent_id: str
    ) -> tuple[StateManager, dict] | None:
        '''加载检查点'''
        checkpoint = self.persistence.load_checkpoint(agent_id)
        
        if not checkpoint:
            return None
        
        data = checkpoint["data"]
        
        # 恢复StateManager
        state_manager = StateManager()
        state_manager.from_dict(data["state_manager"])
        
        return state_manager, data.get("additional_data", {})
    
    def rollback(self, agent_id: str, checkpoint_id: int) -> bool:
        '''回滚到指定检查点'''
        conn = sqlite3.connect(self.persistence.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT state, data FROM checkpoints WHERE agent_id = ? AND id = ?",
            (agent_id, checkpoint_id)
        )
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            # 删除之后的检查点
            conn = sqlite3.connect(self.persistence.db_path)
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM checkpoints WHERE agent_id = ? AND id > ?",
                (agent_id, checkpoint_id)
            )
            conn.commit()
            conn.close()
            
            return True
        
        return False
`

## 4. 断点续传

`python
class ResumableAgent:
    '''支持断点续传的Agent'''
    
    def __init__(
        self, 
        agent_id: str,
        state_manager: StateManager = None,
        checkpoint_manager: CheckpointManager = None
    ):
        self.agent_id = agent_id
        self.state_manager = state_manager or StateManager()
        self.checkpoint_manager = checkpoint_manager or CheckpointManager()
        
        # 尝试恢复状态
        self._try_resume()
    
    def _try_resume(self):
        '''尝试从检查点恢复'''
        result = self.checkpoint_manager.load(self.agent_id)
        
        if result:
            self.state_manager, additional_data = result
            print(f"从检查点恢复: {additional_data.get('last_step', 'unknown')}")
    
    def save_checkpoint(self, step_name: str, additional_data: dict = None):
        '''保存检查点'''
        data = additional_data or {}
        data["last_step"] = step_name
        
        self.checkpoint_manager.save(
            self.agent_id,
            self.state_manager,
            data
        )
        print(f"保存检查点: {step_name}")
    
    async def execute(self, task: str, steps: list[Callable]):
        '''执行任务，支持断点续传'''
        # 设置初始状态
        self.state_manager.set_state_data("task", task)
        
        # 从上次中断的地方继续
        start_index = self.state_manager.get_state_data("current_step_index", 0)
        
        for i in range(start_index, len(steps)):
            step = steps[i]
            
            try:
                # 更新状态
                self.state_manager.set_state_data("current_step_index", i)
                self.state_manager.transition(
                    AgentState.ACTING,
                    f"开始执行步骤 {i}"
                )
                
                # 执行步骤
                result = await step(task, self.state_manager)
                
                # 保存检查点
                self.save_checkpoint(f"step_{i}", {"result": str(result)})
                
                # 更新状态
                self.state_manager.transition(
                    AgentState.OBSERVING,
                    f"完成步骤 {i}"
                )
            
            except Exception as e:
                self.state_manager.transition(
                    AgentState.ERROR,
                    f"步骤 {i} 失败: {str(e)}"
                )
                raise
        
        self.state_manager.transition(AgentState.COMPLETED, "任务完成")
`

## 5. 状态机模式

`python
from abc import ABC, abstractmethod


class State(ABC):
    '''状态基类'''
    
    @abstractmethod
    def enter(self, context: 'StateMachine'):
        '''进入状态'''
        pass
    
    @abstractmethod
    def execute(self, context: 'StateMachine'):
        '''执行状态'''
        pass
    
    @abstractmethod
    def exit(self, context: 'StateMachine'):
        '''退出状态'''
        pass


class StateMachine:
    '''状态机'''
    
    def __init__(self):
        self.states: dict[str, State] = {}
        self.current_state: State | None = None
        self.state_history: list[str] = []
    
    def add_state(self, name: str, state: State):
        '''添加状态'''
        self.states[name] = state
    
    def set_initial_state(self, name: str):
        '''设置初始状态'''
        if name not in self.states:
            raise ValueError(f"状态不存在: {name}")
        self.current_state = self.states[name]
        self.current_state.enter(self)
    
    def transition_to(self, name: str):
        '''转换到新状态'''
        if name not in self.states:
            raise ValueError(f"状态不存在: {name}")
        
        if self.current_state:
            self.current_state.exit(self)
        
        self.state_history.append(name)
        self.current_state = self.states[name]
        self.current_state.enter(self)
    
    def execute(self):
        '''执行当前状态'''
        if self.current_state:
            self.current_state.execute(self)
`

## 6. 本日总结

- StateManager管理Agent状态转换
- StatePersistence实现状态持久化
- CheckpointManager管理检查点
- ResumableAgent支持断点续传
- StateMachine实现状态机模式

明天我们将学习Multi-Agent系统。
