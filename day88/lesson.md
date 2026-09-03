# Day 88: AI Assistant Runtime ① - 架构与核心引擎

## 1. 项目架构

`
AI Assistant Runtime
├── core/
│   ├── agent_loop.py      # Agent 主循环
│   ├── config.py          # 配置管理
│   └── events.py          # 事件系统
├── tools/
│   ├── base.py            # 工具基类
│   ├── registry.py        # 工具注册表
│   ├── file_tools.py      # 文件工具
│   ├── code_tools.py      # 代码工具
│   └── search_tool.py     # 搜索工具
├── memory/
│   ├── short_term.py      # 短期记忆
│   └── long_term.py       # 长期记忆
├── planning/
│   ├── planner.py         # 规划器
│   └── executor.py        # 执行器
├── safety/
│   ├── input_guard.py     # 输入守卫
│   └── output_guard.py    # 输出守卫
├── evaluation/
│   ├── evaluator.py       # 评估器
│   └── tracer.py          # 追踪器
└── main.py                # 入口
`

## 2. 核心引擎 - Agent Loop

`python
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Callable
from enum import Enum
import time
import uuid


class AgentState(Enum):
    IDLE = "idle"
    THINKING = "thinking"
    ACTING = "acting"
    OBSERVING = "observing"
    COMPLETE = "complete"
    ERROR = "error"


@dataclass
class AgentStep:
    step_id: str
    thought: str = ""
    action: str = ""
    action_input: Dict = field(default_factory=dict)
    observation: str = ""
    timestamp: float = 0.0
    duration: float = 0.0
    token_count: int = 0


@dataclass
class AgentConfig:
    max_steps: int = 20
    max_retries: int = 3
    model: str = "gpt-4"
    temperature: float = 0.7
    cost_limit: float = 10.0


class AgentLoop:
    \"\"\"Agent 核心循环\"\"\"
    
    def __init__(self, config: AgentConfig = None):
        self.config = config or AgentConfig()
        self.state = AgentState.IDLE
        self.steps: List[AgentStep] = []
        self.memory: List[Dict] = []
        self.tools: Dict[str, Any] = {}
        self.cost_tracker = {"total_tokens": 0, "total_cost": 0.0}
        self._on_step: Optional[Callable] = None
        self._on_error: Optional[Callable] = None
    
    def register_tool(self, name: str, tool: Any):
        self.tools[name] = tool
    
    def on_step(self, callback: Callable):
        self._on_step = callback
    
    def on_error(self, callback: Callable):
        self._on_error = callback
    
    def run(self, goal: str) -> str:
        \"\"\"Agent 主循环\"\"\"
        print(f"🚀 Agent 开始执行: {goal}")
        self.state = AgentState.THINKING
        
        for step_num in range(self.config.max_steps):
            # 检查成本
            if self.cost_tracker["total_cost"] >= self.config.cost_limit:
                return "达到成本限制，停止执行"
            
            step = AgentStep(
                step_id=f"step_{step_num}",
                timestamp=time.time()
            )
            
            try:
                # 1. 思考
                self.state = AgentState.THINKING
                step.thought = self._think(goal, step_num)
                print(f"\n💭 Step {step_num + 1}: {step.thought}")
                
                # 2. 决定行动
                action_result = self._decide_action(step.thought, goal)
                step.action = action_result["action"]
                step.action_input = action_result["input"]
                
                # 3. 执行行动
                self.state = AgentState.ACTING
                step.observation = self._act(step.action, step.action_input)
                print(f"  🔧 {step.action}: {step.observation[:80]}")
                
                # 4. 观察结果
                self.state = AgentState.OBSERVING
                step.duration = time.time() - step.timestamp
                
                # 5. 检查是否完成
                if self._is_complete(step.observation, goal):
                    self.state = AgentState.COMPLETE
                    self.steps.append(step)
                    self._notify_step(step)
                    
                    final_answer = self._synthesize_answer(goal)
                    print(f"\n✅ 完成! 共 {len(self.steps)} 步")
                    return final_answer
                
                # 6. 记录到记忆
                self.memory.append({
                    "step": step_num,
                    "thought": step.thought,
                    "action": step.action,
                    "observation": step.observation,
                })
                
                self.steps.append(step)
                self._notify_step(step)
                
            except Exception as e:
                self.state = AgentState.ERROR
                step.observation = f"错误: {e}"
                step.duration = time.time() - step.timestamp
                self.steps.append(step)
                
                if self._on_error:
                    self._on_error(step, e)
                
                print(f"  ❌ 错误: {e}")
                
                # 重试
                if step_num < self.config.max_retries:
                    continue
                return f"执行失败: {e}"
        
        return f"达到最大步数 ({self.config.max_steps})，未完成"
    
    def _think(self, goal: str, step_num: int) -> str:
        \"\"\"思考下一步（模拟 LLM）\"\"\"
        if step_num == 0:
            return f"我需要完成: {goal}"
        return f"根据之前的结果，继续执行..."
    
    def _decide_action(self, thought: str, goal: str) -> Dict:
        \"\"\"决定行动（模拟 LLM）\"\"\"
        # 简化：直接返回 finish
        return {"action": "finish", "input": {"answer": f"基于 {goal} 的结果"}}
    
    def _act(self, action: str, input_data: Dict) -> str:
        \"\"\"执行行动\"\"\"
        if action == "finish":
            return f"FINISH: {input_data.get('answer', '')}"
        
        tool = self.tools.get(action)
        if not tool:
            return f"错误: 工具 '{action}' 不存在"
        
        try:
            result = tool(**input_data)
            return str(result)
        except Exception as e:
            return f"执行错误: {e}"
    
    def _is_complete(self, observation: str, goal: str) -> bool:
        return observation.startswith("FINISH:")
    
    def _synthesize_answer(self, goal: str) -> str:
        if self.steps:
            last = self.steps[-1]
            return last.observation.replace("FINISH: ", "")
        return "无法生成答案"
    
    def _notify_step(self, step: AgentStep):
        if self._on_step:
            self._on_step(step)
    
    def get_trace(self) -> List[Dict]:
        return [
            {
                "step": s.step_id,
                "thought": s.thought,
                "action": s.action,
                "observation": s.observation[:100],
                "duration": f"{s.duration:.2f}s",
            }
            for s in self.steps
        ]
`

## 3. 事件系统

`python
class EventBus:
    \"\"\"事件总线\"\"\"
    
    def __init__(self):
        self.listeners: Dict[str, List[Callable]] = {}
    
    def on(self, event: str, callback: Callable):
        if event not in self.listeners:
            self.listeners[event] = []
        self.listeners[event].append(callback)
    
    def emit(self, event: str, data: Any = None):
        for callback in self.listeners.get(event, []):
            callback(data)
    
    def off(self, event: str, callback: Callable = None):
        if callback:
            self.listeners[event] = [
                cb for cb in self.listeners.get(event, []) if cb != callback
            ]
        else:
            self.listeners.pop(event, None)


# 全局事件总线
event_bus = EventBus()

# 注册事件处理
event_bus.on("step_complete", lambda step: print(f"📊 步骤完成: {step.step_id}"))
event_bus.on("error", lambda err: print(f"🚨 错误: {err}"))
event_bus.on("agent_complete", lambda result: print(f"🎉 Agent 完成: {result}"))
`

## 4. 配置管理

`python
@dataclass
class RuntimeConfig:
    \"\"\"运行时配置\"\"\"
    # Agent
    model: str = "gpt-4"
    max_steps: int = 20
    temperature: float = 0.7
    
    # 工具
    enabled_tools: List[str] = field(default_factory=lambda: ["calculator", "search", "file_read"])
    tool_timeout: int = 30
    
    # 安全
    max_input_length: int = 10000
    blocked_patterns: List[str] = field(default_factory=list)
    sandbox_mode: bool = True
    
    # 记忆
    max_memory_messages: int = 100
    memory_backend: str = "memory"  # memory, file, sqlite
    
    # 成本
    cost_limit: float = 10.0
    token_limit: int = 100000
    
    # 追踪
    enable_tracing: bool = True
    log_level: str = "info"
    
    @classmethod
    def from_dict(cls, data: dict) -> 'RuntimeConfig':
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})
`

## 5. 今日目标

### 实现清单
1. ✅ Agent Loop 核心循环
2. ✅ 事件系统
3. ✅ 配置管理
4. ✅ 基础工具注册
5. ✅ 步骤追踪

### 测试要求
`python
# 核心循环测试
agent = AgentLoop()
result = agent.run("1+1等于几")
assert result is not None
assert len(agent.steps) > 0
`

## 6. 动手练习

### 练习 1：实现 AgentLoop
### 练习 2：实现事件系统
### 练习 3：集成工具到 Agent
