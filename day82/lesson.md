# Day 82: Agent State — 状态机与持久化

## 1. 什么是Agent State？

Agent在执行任务过程中需要记住"自己在哪"、"做了什么"、"接下来干什么"。这些信息构成了Agent的**状态**。

没有状态管理的Agent就像一个失忆的工人——每次醒来都不记得昨天干了啥。

### 核心概念
- **State（状态）**：Agent在某一时刻的完整快照
- **Transition（转换）**：从一个状态到另一个状态的动作
- **FSM（有限状态机）**：用有限的状态和转换规则描述Agent行为
- **Checkpoint（检查点）**：状态的持久化快照，用于恢复
- **Serialization（序列化）**：将状态转为可存储格式

## 2. 有限状态机（FSM）设计

### 基础FSM实现

```python
from enum import Enum, auto
from typing import Dict, Callable, Optional, Any

class AgentState(Enum):
    """Agent可能处于的状态"""
    IDLE = auto()           # 空闲
    THINKING = auto()       # 思考中
    TOOL_CALLING = auto()   # 调用工具中
    WAITING_INPUT = auto()  # 等待用户输入
    ERROR = auto()          # 错误状态
    DONE = auto()           # 任务完成

class AgentStateMachine:
    """Agent状态机"""

    def __init__(self):
        self.state = AgentState.IDLE
        self.transitions: Dict[tuple, AgentState] = {}
        self.on_enter: Dict[AgentState, Callable] = {}
        self.on_exit: Dict[AgentState, Callable] = {}
        self.history: list = []  # 状态历史

    def add_transition(self, from_state: AgentState, event: str, to_state: AgentState):
        """添加状态转换规则"""
        self.transitions[(from_state, event)] = to_state

    def on_enter_state(self, state: AgentState, callback: Callable):
        """注册进入状态时的回调"""
        self.on_enter[state] = callback

    def on_exit_state(self, state: AgentState, callback: Callable):
        """注册退出状态时的回调"""
        self.on_exit[state] = callback

    def send_event(self, event: str) -> AgentState:
        """发送事件触发状态转换"""
        key = (self.state, event)
        if key not in self.transitions:
            raise ValueError(f"非法转换: {self.state.name} + {event}")

        old_state = self.state
        # 执行退出回调
        if old_state in self.on_exit:
            self.on_exit[old_state]()

        # 转换状态
        self.state = self.transitions[key]

        # 记录历史
        self.history.append({
            "from": old_state.name,
            "event": event,
            "to": self.state.name,
            "timestamp": __import__("time").time()
        })

        # 执行进入回调
        if self.state in self.on_enter:
            self.on_enter[self.state]()

        return self.state

    def get_state(self) -> str:
        return self.state.name

# 使用示例
fsm = AgentStateMachine()
fsm.add_transition(AgentState.IDLE, "user_message", AgentState.THINKING)
fsm.add_transition(AgentState.THINKING, "need_tool", AgentState.TOOL_CALLING)
fsm.add_transition(AgentState.THINKING, "answer_ready", AgentState.DONE)
fsm.add_transition(AgentState.TOOL_CALLING, "tool_result", AgentState.THINKING)
fsm.add_transition(AgentState.THINKING, "need_input", AgentState.WAITING_INPUT)
fsm.add_transition(AgentState.WAITING_INPUT, "user_message", AgentState.THINKING)

fsm.send_event("user_message")  # IDLE -> THINKING
fsm.send_event("need_tool")     # THINKING -> TOOL_CALLING
fsm.send_event("tool_result")   # TOOL_CALLING -> THINKING
fsm.send_event("answer_ready")  # THINKING -> DONE
```

### 带错误恢复的FSM

```python
class RobustAgentFSM(AgentStateMachine):
    """带自动错误恢复的状态机"""

    MAX_RETRIES = 3

    def __init__(self):
        super().__init__()
        self.retry_count = 0
        self.error_log = []

    def safe_transition(self, event: str) -> Optional[AgentState]:
        """安全转换，失败时进入ERROR状态"""
        try:
            self.retry_count = 0  # 成功则重置
            return self.send_event(event)
        except ValueError as e:
            self.error_log.append(str(e))
            # 尝试错误恢复路径
            if self.state != AgentState.ERROR:
                self.state = AgentState.ERROR
                return self.state
            raise

    def recover(self) -> AgentState:
        """从ERROR状态恢复"""
        self.retry_count += 1
        if self.retry_count > self.MAX_RETRIES:
            raise RuntimeError("重试次数超限，无法恢复")

        # 回退到上一个稳定状态
        if self.history:
            last_stable = AgentState.IDLE
            for h in reversed(self.history):
                if h["to"] != "ERROR":
                    last_stable = AgentState[h["to"]]
                    break
            self.state = last_stable
            return self.state
        self.state = AgentState.IDLE
        return self.state
```

## 3. 状态持久化

### 文件持久化

```python
import json
import os
import time
from typing import Dict, Any

class FileStateManager:
    """基于文件的状态持久化"""

    def __init__(self, storage_dir: str = "./agent_state"):
        self.storage_dir = storage_dir
        os.makedirs(storage_dir, exist_ok=True)

    def save(self, agent_id: str, state: Dict[str, Any]) -> str:
        """保存状态到文件"""
        state["_timestamp"] = time.time()
        state["_version"] = "1.0"
        filepath = os.path.join(self.storage_dir, f"{agent_id}.json")

        # 写临时文件再重命名，防止写到一半崩溃
        tmp_path = filepath + ".tmp"
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
        os.replace(tmp_path, filepath)  # 原子操作
        return filepath

    def load(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """加载状态"""
        filepath = os.path.join(self.storage_dir, f"{agent_id}.json")
        if not os.path.exists(filepath):
            return None
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)

    def list_agents(self) -> list:
        """列出所有保存了状态的agent"""
        if not os.path.exists(self.storage_dir):
            return []
        return [
            f[:-5] for f in os.listdir(self.storage_dir)
            if f.endswith(".json")
        ]

    def delete(self, agent_id: str):
        """删除agent状态"""
        filepath = os.path.join(self.storage_dir, f"{agent_id}.json")
        if os.path.exists(filepath):
            os.remove(filepath)
```

### Redis持久化

```python
import json
import redis
from typing import Optional, Dict, Any

class RedisStateManager:
    """基于Redis的状态持久化"""

    def __init__(self, host="localhost", port=6379, db=0, prefix="agent:"):
        self.client = redis.Redis(host=host, port=port, db=db)
        self.prefix = prefix

    def save(self, agent_id: str, state: Dict[str, Any], ttl: int = 3600):
        """保存状态到Redis，带TTL"""
        key = f"{self.prefix}{agent_id}"
        self.client.setex(key, ttl, json.dumps(state, ensure_ascii=False))

    def load(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """从Redis加载状态"""
        key = f"{self.prefix}{agent_id}"
        data = self.client.get(key)
        if data is None:
            return None
        return json.loads(data)

    def save_field(self, agent_id: str, field: str, value: Any):
        """保存单个字段"""
        key = f"{self.prefix}{agent_id}"
        self.client.hset(key, field, json.dumps(value))

    def load_field(self, agent_id: str, field: str) -> Optional[Any]:
        """加载单个字段"""
        key = f"{self.prefix}{agent_id}"
        data = self.client.hget(key, field)
        if data is None:
            return None
        return json.loads(data)

    def list_agents(self) -> list:
        """列出所有agent"""
        pattern = f"{self.prefix}*"
        keys = self.client.keys(pattern)
        return [k.decode().replace(self.prefix, "") for k in keys]
```

## 4. Checkpoint与恢复

```python
import json
import time
import copy
from typing import Dict, Any, Optional, List

class CheckpointManager:
    """检查点管理器 - 支持断点续传"""

    def __init__(self, storage_dir: str = "./checkpoints"):
        self.storage_dir = storage_dir
        import os
        os.makedirs(storage_dir, exist_ok=True)
        self.storage_dir_path = storage_dir

    def save_checkpoint(self, agent_id: str, state: Dict[str, Any],
                        task_id: str, step: int) -> str:
        """保存检查点"""
        checkpoint = {
            "agent_id": agent_id,
            "task_id": task_id,
            "step": step,
            "state": copy.deepcopy(state),
            "timestamp": time.time(),
            "version": "1.0"
        }
        filepath = os.path.join(
            self.storage_dir_path,
            f"{agent_id}_{task_id}_step{step}.json"
        )
        tmp = filepath + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(checkpoint, f, ensure_ascii=False, indent=2)
        os.replace(tmp, filepath)
        return filepath

    def load_latest_checkpoint(self, agent_id: str, task_id: str) -> Optional[Dict]:
        """加载最新的检查点"""
        import glob
        pattern = os.path.join(
            self.storage_dir_path,
            f"{agent_id}_{task_id}_step*.json"
        )
        files = glob.glob(pattern)
        if not files:
            return None

        # 按step排序取最新的
        files.sort(key=lambda f: int(f.split("_step")[-1].split(".")[0]))
        with open(files[-1], "r", encoding="utf-8") as f:
            return json.load(f)

    def list_checkpoints(self, agent_id: str, task_id: str) -> List[Dict]:
        """列出某任务的所有检查点"""
        import glob
        pattern = os.path.join(
            self.storage_dir_path,
            f"{agent_id}_{task_id}_step*.json"
        )
        results = []
        for fp in sorted(glob.glob(pattern)):
            with open(fp, "r", encoding="utf-8") as f:
                ckpt = json.load(f)
                results.append({
                    "step": ckpt["step"],
                    "timestamp": ckpt["timestamp"],
                    "file": fp
                })
        return results

    def cleanup_old(self, agent_id: str, task_id: str, keep_last: int = 5):
        """清理旧检查点，只保留最近N个"""
        import glob
        pattern = os.path.join(
            self.storage_dir_path,
            f"{agent_id}_{task_id}_step*.json"
        )
        files = sorted(glob.glob(pattern),
                      key=lambda f: int(f.split("_step")[-1].split(".")[0]))
        for f in files[:-keep_last]:
            os.remove(f)
```

## 5. 断点续传Agent

```python
class ResumableAgent:
    """支持断点续传的Agent"""

    def __init__(self, agent_id: str, checkpoint_manager: CheckpointManager):
        self.agent_id = agent_id
        self.ckpt_mgr = checkpoint_manager
        self.current_step = 0
        self.state = {
            "messages": [],
            "tool_results": [],
            "variables": {}
        }

    def resume_or_start(self, task_id: str, initial_input: str) -> Dict:
        """恢复检查点或从头开始"""
        checkpoint = self.ckpt_mgr.load_latest_checkpoint(self.agent_id, task_id)

        if checkpoint:
            self.state = checkpoint["state"]
            self.current_step = checkpoint["step"]
            print(f"[RESUME] 从步骤 {self.current_step} 恢复")
        else:
            self.state["messages"].append({
                "role": "user",
                "content": initial_input
            })
            self.current_step = 0
            print("[START] 从头开始")

        return self.state

    def process_step(self, task_id: str) -> Dict:
        """处理一个步骤并保存检查点"""
        self.current_step += 1
        print(f"[STEP {self.current_step}] 处理中...")

        # 模拟处理（实际应调用LLM或工具）
        result = {
            "step": self.current_step,
            "status": "processed",
            "output": f"Step {self.current_step} completed"
        }
        self.state["tool_results"].append(result)

        # 每步都保存检查点
        self.ckpt_mgr.save_checkpoint(
            self.agent_id, self.state, task_id, self.current_step
        )

        return result

    def run(self, task_id: str, initial_input: str, total_steps: int = 5):
        """运行完整任务，支持断点续传"""
        self.resume_or_start(task_id, initial_input)

        while self.current_step < total_steps:
            try:
                self.process_step(task_id)
            except Exception as e:
                print(f"[ERROR] 步骤 {self.current_step} 失败: {e}")
                print("[RECOVERY] 等待恢复...")
                # 实际中这里会等待外部恢复信号
                raise

        print(f"[DONE] 任务完成，共 {self.current_step} 步")
        return self.state
```

## 6. 状态序列化与版本兼容

```python
import json
from typing import Dict, Any, Optional

class StateSerializer:
    """带版本兼容的状态序列化器"""

    def __init__(self):
        self.migrations = {}  # version -> migration_func

    def register_migration(self, from_version: str, to_version: str, func):
        """注册版本迁移函数"""
        self.migrations[(from_version, to_version)] = func

    def serialize(self, state: Dict[str, Any]) -> str:
        """序列化状态"""
        output = {
            "__version__": "2.0",
            "__type__": state.get("__type__", "agent_state"),
            "data": {k: v for k, v in state.items()
                    if not k.startswith("__")}
        }
        return json.dumps(output, ensure_ascii=False, indent=2)

    def deserialize(self, data: str) -> Dict[str, Any]:
        """反序列化状态，自动处理版本迁移"""
        parsed = json.loads(data)
        version = parsed.get("__version__", "0.1")

        # 版本迁移链
        while version != "2.0":
            migrated = False
            for (from_v, to_v), migrator in self.migrations.items():
                if from_v == version:
                    parsed["data"] = migrator(parsed["data"])
                    version = to_v
                    parsed["__version__"] = to_v
                    migrated = True
                    break
            if not migrated:
                raise ValueError(f"无法从版本 {version} 迁移到 2.0")

        return parsed["data"]

# 注册迁移函数
def migrate_0_1_to_1_0(data: Dict) -> Dict:
    """0.1 -> 1.0: messages格式变更"""
    if "messages" in data:
        data["messages"] = [
            m if isinstance(m, dict) else {"role": "user", "content": m}
            for m in data["messages"]
        ]
    data["metadata"] = {}  # 新增字段
    return data

def migrate_1_0_to_2_0(data: Dict) -> Dict:
    """1.0 -> 2.0: 增加trace_id"""
    data["trace_id"] = ""
    data["checkpoint_count"] = 0
    return data

serializer = StateSerializer()
serializer.register_migration("0.1", "1.0", migrate_0_1_to_1_0)
serializer.register_migration("1.0", "2.0", migrate_1_0_to_2_0)
```

## 7. 常见错误

### 1. 状态不一致
```python
# 错误：转换和保存不同步
def bad_transition(self, event):
    self.state = self.transitions[(self.state, event)]  # 状态变了
    # 但如果这里崩溃，状态已变但未持久化
    self.save()  # 太晚了

# 正确：先持久化再转换，或用事务
def good_transition(self, event):
    old_state = self.state
    new_state = self.transitions[(self.state, event)]
    # 先保存目标状态
    self.save_checkpoint({"state": new_state, "old_state": old_state})
    self.state = new_state  # 再实际切换
```

### 2. 并发状态冲突
```python
# 错误：两个进程同时修改状态
# 正确：用分布式锁或乐观锁
def safe_update(self, agent_id, state, expected_version):
    current = self.load(agent_id)
    if current.get("version") != expected_version:
        raise ConflictError("状态已被其他进程修改")
    state["version"] = expected_version + 1
    self.save(agent_id, state)
```

### 3. 序列化丢失类型信息
```python
# 错误：直接json.dumps datetime对象
json.dumps({"time": datetime.now()})  # TypeError!

# 正确：自定义序列化
def custom_serializer(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, set):
        return list(obj)
    raise TypeError(f"无法序列化 {type(obj)}")
```

## 8. 实际应用场景

- **多轮对话Agent**：记住对话历史，支持上下文延续
- **长任务Agent**：复杂任务分步执行，随时可恢复
- **分布式Agent**：状态在多节点间共享和同步
- **调试与回放**：保存完整状态轨迹，支持问题重现

## 9. 动手练习

1. 实现一个支持3种以上状态的FSM
2. 用文件持久化保存Agent状态，支持加载和恢复
3. 实现CheckpointManager，支持断点续传
4. 实现带版本迁移的StateSerializer
5. 组合以上组件创建一个完整的ResumableAgent
