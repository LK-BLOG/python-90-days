# Day 88 课程：构建AI Assistant Runtime

## 1. 项目架构设计

### 模块化设计原则

`python
# src/__init__.py
\"\"\"
AI Assistant Runtime
一个模块化、可扩展的AI Agent框架
\"\"\"

__version__ = "0.1.0"
`

### 核心模块

`python
# src/agent/__init__.py
from .core import Agent
from .loop import AgentLoop
from .state import AgentState

__all__ = ["Agent", "AgentLoop", "AgentState"]
`

## 2. Agent核心实现

`python
# src/agent/core.py
from dataclasses import dataclass, field
from typing import Any, Callable, Awaitable
from datetime import datetime
import asyncio


@dataclass
class AgentConfig:
    '''Agent配置'''
    name: str = "Assistant"
    model: str = "gpt-4"
    max_iterations: int = 10
    temperature: float = 0.7
    system_prompt: str = "你是一个有用的AI助手。"
    tools: list[str] = field(default_factory=list)
    memory_enabled: bool = True
    planning_enabled: bool = True


class Agent:
    '''AI Assistant Agent'''
    
    def __init__(self, config: AgentConfig = None):
        self.config = config or AgentConfig()
        self.tools: dict[str, Callable] = {}
        self.memory: list[dict] = []
        self.state: dict[str, Any] = {}
        self.is_running: bool = False
        
        # 回调函数
        self.on_think: Callable | None = None
        self.on_act: Callable | None = None
        self.on_observe: Callable | None = None
        self.on_error: Callable | None = None
    
    def register_tool(self, name: str, func: Callable):
        '''注册工具'''
        self.tools[name] = func
        print(f"注册工具: {name}")
    
    def add_memory(self, role: str, content: str):
        '''添加记忆'''
        self.memory.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
    
    def get_memory_prompt(self, max_items: int = 10) -> str:
        '''获取记忆提示'''
        recent = self.memory[-max_items:]
        return "\n".join([f"{m['role']}: {m['content']}" for m in recent])
    
    async def run(self, user_input: str) -> str:
        '''运行Agent'''
        self.is_running = True
        
        # 添加用户输入到记忆
        self.add_memory("user", user_input)
        
        # 构建提示
        context = self._build_context(user_input)
        
        # Agent循环
        iterations = 0
        while iterations < self.config.max_iterations:
            iterations += 1
            
            # 思考
            thought = await self._think(context)
            if self.on_think:
                await self.on_think(thought)
            
            # 检查是否需要行动
            if thought.get("action_needed"):
                # 执行行动
                result = await self._act(
                    thought["tool"],
                    thought["tool_input"]
                )
                
                if self.on_act:
                    await self.on_act(thought, result)
                
                # 更新上下文
                context += f"\nAction: {thought['tool']}({thought['tool_input']})\nResult: {result}"
            else:
                # 得到最终回答
                answer = thought.get("answer", "无法生成回答")
                self.add_memory("assistant", answer)
                self.is_running = False
                return answer
        
        self.is_running = False
        return "达到最大迭代次数"
    
    def _build_context(self, user_input: str) -> str:
        '''构建上下文'''
        tools_desc = "\n".join([
            f"- {name}: {func.__doc__ or '无描述'}"
            for name, func in self.tools.items()
        ])
        
        memory = self.get_memory_prompt()
        
        return f\"\"\"
{self.config.system_prompt}

可用工具：
{tools_desc}

对话历史：
{memory}

用户输入：{user_input}
\"\"\"
    
    async def _think(self, context: str) -> dict:
        '''思考（调用LLM）'''
        # 这里应该调用真实的LLM
        # 简化处理，返回模拟响应
        return {
            "thought": "分析用户需求",
            "action_needed": False,
            "answer": f"我理解你的问题。作为{self.config.name}，我会尽力帮助你。"
        }
    
    async def _act(self, tool_name: str, tool_input: Any) -> Any:
        '''执行行动'''
        if tool_name not in self.tools:
            return f"工具 {tool_name} 不存在"
        
        tool_func = self.tools[tool_name]
        
        try:
            if asyncio.iscoroutinefunction(tool_func):
                result = await tool_func(tool_input)
            else:
                result = tool_func(tool_input)
            return result
        except Exception as e:
            if self.on_error:
                await self.on_error(e)
            return f"工具执行错误: {str(e)}"
`

## 3. Agent循环

`python
# src/agent/loop.py
from dataclasses import dataclass
from typing import Any
from datetime import datetime


@dataclass
class AgentStep:
    '''Agent步骤'''
    step_number: int
    thought: str
    action: str | None = None
    action_input: Any = None
    observation: str | None = None
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


class AgentLoop:
    '''Agent循环管理器'''
    
    def __init__(self, agent: 'Agent'):
        self.agent = agent
        self.steps: list[AgentStep] = []
        self.current_step: int = 0
    
    async def run(self, query: str, max_steps: int = 10) -> dict:
        '''运行循环'''
        self.steps = []
        context = self.agent._build_context(query)
        
        for step_num in range(1, max_steps + 1):
            # 思考
            thought = await self.agent._think(context)
            
            step = AgentStep(
                step_number=step_num,
                thought=thought.get("thought", "")
            )
            
            # 检查是否需要行动
            if thought.get("action_needed"):
                step.action = thought.get("tool")
                step.action_input = thought.get("tool_input")
                
                # 执行
                observation = await self.agent._act(
                    step.action,
                    step.action_input
                )
                
                step.observation = str(observation)
                
                # 更新上下文
                context += f"\nAction: {step.action}({step.action_input})\nObservation: {step.observation}"
            
            self.steps.append(step)
            
            # 检查是否完成
            if not thought.get("action_needed"):
                return {
                    "answer": thought.get("answer", ""),
                    "steps": self.steps,
                    "total_steps": step_num
                }
        
        return {
            "answer": "达到最大步数限制",
            "steps": self.steps,
            "total_steps": max_steps
        }
`

## 4. 状态管理

`python
# src/agent/state.py
from dataclasses import dataclass, field
from typing import Any
from datetime import datetime
from enum import Enum


class AgentStatus(Enum):
    '''Agent状态'''
    IDLE = "idle"
    THINKING = "thinking"
    ACTING = "acting"
    WAITING = "waiting"
    ERROR = "error"
    COMPLETED = "completed"


@dataclass
class AgentState:
    '''Agent状态'''
    status: AgentStatus = AgentStatus.IDLE
    current_task: str | None = None
    variables: dict[str, Any] = field(default_factory=dict)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def update(self, **kwargs):
        '''更新状态'''
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.now()
    
    def to_dict(self) -> dict:
        '''转换为字典'''
        return {
            "status": self.status.value,
            "current_task": self.current_task,
            "variables": self.variables,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
`

## 5. 本日总结

- 设计了模块化的Runtime架构
- 实现了Agent核心类
- 实现了Agent循环管理
- 实现了状态管理系统

明天将继续集成Memory和Planning系统。
