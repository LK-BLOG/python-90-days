# Day 83: State & Checkpoint

## 1. Agent 状态管理

### 1.1 为什么需要状态管理？

Agent 长时间运行时需要：
- **断点续传**：网络断了能接着跑
- **错误恢复**：某步失败能回退重试
- **多轮持久**：用户关闭后下次还能继续
- **并发控制**：多个 Agent 不冲突

### 1.2 状态数据结构

`python
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from enum import Enum
import time
import json


class AgentState(Enum):
    IDLE = "idle"
    PLANNING = "planning"
    EXECUTING = "executing"
    WAITING = "waiting"
    ERROR = "error"
    COMPLETED = "completed"


@dataclass
class StepCheckpoint:
    \"\"\"步骤检查点\"\"\"
    step_id: str
    step_type: str
    input_data: Dict[str, Any]
    output_data: Any = None
    status: str = "pending"
    timestamp: float = 0.0
    error: str = ""
    duration: float = 0.0


@dataclass
class AgentCheckpoint:
    \"\"\"Agent 完整检查点\"\"\"
    agent_id: str
    state: str
    goal: str
    current_step: int = 0
    steps: List[StepCheckpoint] = field(default_factory=list)
    memory: Dict[str, Any] = field(default_factory=dict)
    context: List[Dict] = field(default_factory=list)
    timestamp: float = 0.0
    
    def to_dict(self) -> dict:
        return {
            "agent_id": self.agent_id,
            "state": self.state,
            "goal": self.goal,
            "current_step": self.current_step,
            "steps": [
                {
                    "step_id": s.step_id,
                    "step_type": s.step_type,
                    "input_data": s.input_data,
                    "output_data": s.output_data,
                    "status": s.status,
                    "timestamp": s.timestamp,
                    "error": s.error,
                    "duration": s.duration,
                }
                for s in self.steps
            ],
            "memory": self.memory,
            "context": self.context,
            "timestamp": self.timestamp,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'AgentCheckpoint':
        steps = [
            StepCheckpoint(**s) for s in data.get("steps", [])
        ]
        return cls(
            agent_id=data["agent_id"],
            state=data["state"],
            goal=data["goal"],
            current_step=data.get("current_step", 0),
            steps=steps,
            memory=data.get("memory", {}),
            context=data.get("context", []),
            timestamp=data.get("timestamp", 0),
        )
`

## 2. 检查点管理器

`python
class CheckpointManager:
    \"\"\"检查点管理器 - 保存和恢复状态\"\"\"
    
    def __init__(self, storage_path: str = "./checkpoints"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
    
    def save(self, checkpoint: AgentCheckpoint):
        \"\"\"保存检查点\"\"\"
        checkpoint.timestamp = time.time()
        filepath = self.storage_path / f"{checkpoint.agent_id}.json"
        filepath.write_text(
            json.dumps(checkpoint.to_dict(), ensure_ascii=False, indent=2)
        )
        print(f"  💾 检查点已保存: {filepath}")
    
    def load(self, agent_id: str) -> Optional[AgentCheckpoint]:
        \"\"\"加载检查点\"\"\"
        filepath = self.storage_path / f"{agent_id}.json"
        if not filepath.exists():
            return None
        
        data = json.loads(filepath.read_text(encoding="utf-8"))
        return AgentCheckpoint.from_dict(data)
    
    def list_checkpoints(self) -> List[str]:
        \"\"\"列出所有检查点\"\"\"
        return [f.stem for f in self.storage_path.glob("*.json")]
    
    def delete(self, agent_id: str):
        filepath = self.storage_path / f"{agent_id}.json"
        if filepath.exists():
            filepath.unlink()
    
    def save_step(self, checkpoint: AgentCheckpoint, step_result: Any):
        \"\"\"保存步骤结果\"\"\"
        if checkpoint.current_step < len(checkpoint.steps):
            step = checkpoint.steps[checkpoint.current_step]
            step.output_data = step_result
            step.status = "completed"
            step.timestamp = time.time()
            checkpoint.current_step += 1
        
        self.save(checkpoint)
`

## 3. 持久化后端

`python
class MemoryBackend:
    \"\"\"内存后端（测试用）\"\"\"
    
    def __init__(self):
        self._store = {}
    
    def save(self, key: str, value: dict):
        self._store[key] = value
    
    def load(self, key: str):
        return self._store.get(key)
    
    def delete(self, key: str):
        self._store.pop(key, None)
    
    def list_keys(self):
        return list(self._store.keys())


class JSONFileBackend:
    \"\"\"文件后端\"\"\"
    
    def __init__(self, directory: str = "./state"):
        self.dir = Path(directory)
        self.dir.mkdir(parents=True, exist_ok=True)
    
    def save(self, key: str, value: dict):
        filepath = self.dir / f"{key}.json"
        filepath.write_text(json.dumps(value, ensure_ascii=False, indent=2))
    
    def load(self, key: str):
        filepath = self.dir / f"{key}.json"
        if not filepath.exists():
            return None
        return json.loads(filepath.read_text(encoding="utf-8"))
    
    def delete(self, key: str):
        filepath = self.dir / f"{key}.json"
        if filepath.exists():
            filepath.unlink()
    
    def list_keys(self):
        return [f.stem for f in self.dir.glob("*.json")]


class SQLiteBackend:
    \"\"\"SQLite 后端\"\"\"
    
    def __init__(self, db_path: str = "./state.db"):
        import sqlite3
        self.conn = sqlite3.connect(db_path)
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS agent_state (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL,
                updated_at REAL NOT NULL
            )
        ''')
        self.conn.commit()
    
    def save(self, key: str, value: dict):
        import time
        self.conn.execute(
            'INSERT OR REPLACE INTO agent_state VALUES (?, ?, ?)',
            (key, json.dumps(value, ensure_ascii=False), time.time())
        )
        self.conn.commit()
    
    def load(self, key: str):
        cursor = self.conn.execute(
            'SELECT value FROM agent_state WHERE key = ?', (key,)
        )
        row = cursor.fetchone()
        return json.loads(row[0]) if row else None
    
    def delete(self, key: str):
        self.conn.execute('DELETE FROM agent_state WHERE key = ?', (key,))
        self.conn.commit()
    
    def list_keys(self):
        cursor = self.conn.execute('SELECT key FROM agent_state')
        return [row[0] for row in cursor.fetchall()]
`

## 4. 断点续传执行器

`python
class ResumableExecutor:
    \"\"\"支持断点续传的执行器\"\"\"
    
    def __init__(self, tools: dict, checkpoint_manager: CheckpointManager):
        self.tools = tools
        self.cm = checkpoint_manager
    
    def execute(self, agent_id: str, steps: list, resume: bool = True) -> str:
        \"\"\"执行任务，支持从检查点恢复\"\"\"
        checkpoint = None
        
        # 尝试恢复
        if resume:
            checkpoint = self.cm.load(agent_id)
            if checkpoint:
                print(f"🔄 从检查点恢复 (步骤 {checkpoint.current_step}/{len(checkpoint.steps)})")
            else:
                print("📝 创建新检查点")
                checkpoint = self._create_checkpoint(agent_id, steps)
        else:
            checkpoint = self._create_checkpoint(agent_id, steps)
        
        # 从上次中断的地方继续
        for i in range(checkpoint.current_step, len(checkpoint.steps)):
            step = checkpoint.steps[i]
            print(f"\n▶ 步骤 {i+1}: {step.step_type}")
            
            try:
                tool = self.tools.get(step.step_type)
                if not tool:
                    step.status = "failed"
                    step.error = f"工具不存在: {step.step_type}"
                    self.cm.save(checkpoint)
                    continue
                
                start = time.time()
                result = tool(**step.input_data)
                step.duration = time.time() - start
                
                step.output_data = result
                step.status = "completed"
                checkpoint.current_step = i + 1
                
                # 保存检查点
                self.cm.save(checkpoint)
                print(f"  ✅ 完成 (耗时 {step.duration:.2f}s)")
                
            except Exception as e:
                step.status = "failed"
                step.error = str(e)
                self.cm.save(checkpoint)
                print(f"  ❌ 失败: {e}")
                
                # 可以选择继续或中止
                if "fatal" in str(e).lower():
                    return f"致命错误，停止执行"
                continue
        
        checkpoint.state = AgentState.COMPLETED.value
        self.cm.save(checkpoint)
        return f"所有步骤完成！"
    
    def _create_checkpoint(self, agent_id: str, steps: list) -> AgentCheckpoint:
        step_checkpoints = [
            StepCheckpoint(
                step_id=f"step_{i}",
                step_type=s.get("tool", ""),
                input_data=s.get("params", {}),
                timestamp=time.time()
            )
            for i, s in enumerate(steps)
        ]
        
        return AgentCheckpoint(
            agent_id=agent_id,
            state=AgentState.EXECUTING.value,
            goal=steps[0].get("goal", "") if steps else "",
            steps=step_checkpoints,
            timestamp=time.time()
        )
`

## 5. 常见错误

1. **检查点太频繁**：每次操作都保存 → 每 N 步保存一次
2. **不清理旧检查点**：磁盘爆满 → 定期清理
3. **并发冲突**：多 Agent 同时写同一文件 → 加锁
4. **状态不一致**：部分保存 → 用事务
5. **没有版本号**：新旧格式不兼容 → 添加版本字段

## 6. 动手练习

### 练习 1：实现 Checkpoint 数据结构
### 练习 2：实现 JSON 文件后端
### 练习 3：实现断点续传执行器
