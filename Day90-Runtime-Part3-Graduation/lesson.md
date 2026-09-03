# Day 90 课程：完成AI Assistant Runtime

## 1. 多Agent支持

`python
# src/ai_runtime/multi_agent/__init__.py
from .coordinator import AgentCoordinator
from .worker import WorkerAgent

__all__ = ["AgentCoordinator", "WorkerAgent"]
`

`python
# src/ai_runtime/multi_agent/coordinator.py
from dataclasses import dataclass
from typing import Any
import asyncio


@dataclass
class AgentRole:
    '''Agent角色'''
    name: str
    description: str
    tools: list[str]


class AgentCoordinator:
    '''Agent协调器'''
    
    def __init__(self):
        self.agents: dict[str, Any] = {}
        self.roles: dict[str, AgentRole] = {}
    
    def register_agent(self, name: str, agent: Any, role: AgentRole):
        '''注册Agent'''
        self.agents[name] = agent
        self.roles[name] = role
    
    async def execute(self, task: str, assigned_agent: str = None) -> str:
        '''执行任务'''
        if assigned_agent and assigned_agent in self.agents:
            return await self.agents[assigned_agent].run(task)
        
        # 自动选择Agent
        agent_name = self._select_agent(task)
        return await self.agents[agent_name].run(task)
    
    def _select_agent(self, task: str) -> str:
        '''选择Agent'''
        # 简单的关键词匹配
        task_lower = task.lower()
        
        for name, role in self.roles.items():
            if any(kw in task_lower for kw in role.description.lower().split()):
                return name
        
        # 默认返回第一个
        return list(self.agents.keys())[0]
`

## 2. 评估与监控

`python
# src/ai_runtime/observability/monitor.py
from dataclasses import dataclass
from datetime import datetime
from typing import Any
import time


@dataclass
class MetricPoint:
    '''指标点'''
    name: str
    value: float
    timestamp: datetime
    tags: dict[str, Any]


class AgentMonitor:
    '''Agent监控器'''
    
    def __init__(self):
        self.metrics: list[MetricPoint] = []
        self.traces: list[dict] = []
    
    def record_metric(self, name: str, value: float, tags: dict = None):
        '''记录指标'''
        self.metrics.append(MetricPoint(
            name=name,
            value=value,
            timestamp=datetime.now(),
            tags=tags or {}
        ))
    
    def start_trace(self, operation: str) -> str:
        '''开始追踪'''
        trace_id = f"trace_{len(self.traces)}"
        self.traces.append({
            "id": trace_id,
            "operation": operation,
            "start_time": time.time(),
            "spans": []
        })
        return trace_id
    
    def end_trace(self, trace_id: str):
        '''结束追踪'''
        for trace in self.traces:
            if trace["id"] == trace_id:
                trace["end_time"] = time.time()
                trace["duration"] = trace["end_time"] - trace["start_time"]
                break
    
    def get_summary(self) -> dict:
        '''获取摘要'''
        return {
            "total_metrics": len(self.metrics),
            "total_traces": len(self.traces),
            "avg_duration": sum(t.get("duration", 0) for t in self.traces) / len(self.traces) if self.traces else 0
        }
`

## 3. 安全护栏集成

`python
# src/ai_runtime/safety/guardrails_manager.py
from typing import Callable


class GuardrailsManager:
    '''Guardrails管理器'''
    
    def __init__(self):
        self.input_guardrails: list[Callable] = []
        self.output_guardrails: list[Callable] = []
    
    def add_input_guardrail(self, guardrail: Callable):
        '''添加输入Guardrail'''
        self.input_guardrails.append(guardrail)
    
    def add_output_guardrail(self, guardrail: Callable):
        '''添加输出Guardrail'''
        self.output_guardrails.append(guardrail)
    
    def check_input(self, text: str) -> tuple[bool, str, list]:
        '''检查输入'''
        violations = []
        current = text
        
        for guardrail in self.input_guardrails:
            passed, result = guardrail(current)
            if not passed:
                violations.append(guardrail.__name__)
                current = result
        
        return len(violations) == 0, current, violations
    
    def check_output(self, text: str) -> tuple[bool, str, list]:
        '''检查输出'''
        violations = []
        current = text
        
        for guardrail in self.output_guardrails:
            passed, result = guardrail(current)
            if not passed:
                violations.append(guardrail.__name__)
                current = result
        
        return len(violations) == 0, current, violations
`

## 4. 完整Runtime集成

`python
# src/ai_runtime/runtime.py
from .agent import Agent, AgentConfig
from .memory import MemorySystem
from .planning import TaskPlanner
from .context import ContextManager
from .safety import GuardrailsManager
from .observability import AgentMonitor


class AIRuntime:
    '''完整的AI Assistant Runtime'''
    
    def __init__(self, config: AgentConfig = None):
        self.config = config or AgentConfig()
        
        # 核心组件
        self.agent = Agent(self.config)
        self.memory = MemorySystem()
        self.planner = TaskPlanner()
        self.context_manager = ContextManager()
        self.safety = GuardrailsManager()
        self.monitor = AgentMonitor()
        
        # 状态
        self.is_initialized = False
    
    async def initialize(self):
        '''初始化'''
        self._register_default_tools()
        self._setup_safety()
        self.is_initialized = True
    
    def _register_default_tools(self):
        '''注册默认工具'''
        # 注册5个核心工具
        from .tools.builtin import (
            SearchTool, CalculatorTool, 
            FileOpsTool, CodeExecutorTool, WebRequestTool
        )
        
        tools = [
            SearchTool(),
            CalculatorTool(),
            FileOpsTool(),
            CodeExecutorTool(),
            WebRequestTool()
        ]
        
        for tool in tools:
            self.agent.register_tool(tool.name, tool.execute)
    
    def _setup_safety(self):
        '''设置安全护栏'''
        # 输入安全检查
        def check_injection(text: str) -> tuple[bool, str]:
            dangerous = ["ignore previous", "you are now"]
            for pattern in dangerous:
                if pattern in text.lower():
                    return False, "检测到潜在的注入攻击"
            return True, text
        
        self.safety.add_input_guardrail(check_injection)
        
        # 输出敏感信息过滤
        def check_sensitive(text: str) -> tuple[bool, str]:
            import re
            emails = re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', text)
            if emails:
                return False, text.replace(emails[0], "[REDACTED]")
            return True, text
        
        self.safety.add_output_guardrail(check_sensitive)
    
    async def run(self, user_input: str) -> str:
        '''运行'''
        if not self.is_initialized:
            await self.initialize()
        
        # 开始追踪
        trace_id = self.monitor.start_trace("user_interaction")
        
        try:
            # 输入检查
            is_safe, input_text, violations = self.safety.check_input(user_input)
            if not is_safe:
                return f"输入被安全检查阻止: {violations}"
            
            # 添加到记忆
            self.memory.add(input_text, "user")
            
            # 检索相关记忆
            memories = self.memory.search(input_text)
            
            # 构建上下文
            context = self.context_manager.build_context(
                system_prompt=self.config.system_prompt,
                memory=[m.content for m in memories],
                history=[],
                current_input=input_text
            )
            
            # Agent处理
            response = await self.agent.run(input_text)
            
            # 输出检查
            is_safe, response, violations = self.safety.check_output(response)
            
            # 添加到记忆
            self.memory.add(response, "assistant")
            
            # 记录指标
            self.monitor.record_metric("interaction", 1)
            
            return response
        
        finally:
            self.monitor.end_trace(trace_id)
    
    def get_status(self) -> dict:
        '''获取状态'''
        return {
            "initialized": self.is_initialized,
            "memory_size": len(self.memory.items),
            "tools_count": len(self.agent.tools),
            "monitor_summary": self.monitor.get_summary()
        }
`

## 5. 本日总结

- 完成了多Agent支持
- 添加了评估与监控
- 集成了安全护栏
- 构建了完整的Runtime

## 🎓 毕业要求

完成以下任务即可毕业：

1. **功能完整性**：所有核心功能正常工作
2. **代码质量**：结构清晰、类型注解完整
3. **测试覆盖**：核心功能有测试
4. **文档**：有使用说明和API文档

**恭喜你完成Python 90天Agent工程阶段！**
