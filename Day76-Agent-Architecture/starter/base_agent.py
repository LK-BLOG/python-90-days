"""
Day 76 起步代码：Agent基类
你需要实现基础的Agent架构
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class AgentStep:
    '''执行步骤记录'''
    step_number: int
    thought: str
    action: str | None = None
    action_input: str | None = None
    observation: str | None = None
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class AgentResult:
    '''执行结果'''
    query: str
    answer: str
    steps: list[AgentStep]
    total_steps: int
    success: bool
    error: str | None = None


class BaseTool(ABC):
    '''工具基类'''
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    @abstractmethod
    def execute(self, input_data: str) -> str:
        '''执行工具'''
        pass


class BaseAgent(ABC):
    '''Agent基类'''
    
    def __init__(self):
        self.tools: dict[str, BaseTool] = {}
        self.steps: list[AgentStep] = []
    
    def register_tool(self, tool: BaseTool):
        '''注册工具'''
        self.tools[tool.name] = tool
    
    @abstractmethod
    def run(self, query: str, max_steps: int = 10) -> AgentResult:
        '''执行Agent任务'''
        pass
    
    @abstractmethod
    def _think(self, context: str) -> dict:
        '''思考：决定下一步行动'''
        pass
    
    def _act(self, tool_name: str, tool_input: str) -> str:
        '''行动：执行工具'''
        if tool_name not in self.tools:
            return f"错误：工具 {tool_name} 不存在"
        return self.tools[tool_name].execute(tool_input)


class ReActAgent(BaseAgent):
    '''ReAct Agent 实现
    
    TODO: 实现ReAct模式的Agent
    提示：
    1. 在_think方法中，使用LLM决定下一步行动
    2. 在run方法中，实现思考-行动循环
    3. 记录每个步骤的思考和行动
    '''
    
    def __init__(self, llm_provider=None):
        super().__init__()
        self.llm_provider = llm_provider or self._default_llm
    
    def _default_llm(self, prompt: str) -> str:
        '''默认LLM（模拟）'''
        import json
        return json.dumps({
            "thought": "我需要分析这个问题",
            "action": None,
            "action_input": None,
            "answer": "这是模拟的回答"
        })
    
    def _think(self, context: str) -> dict:
        '''TODO: 实现思考逻辑'''
        # TODO: 调用LLM，解析响应
        pass
    
    def run(self, query: str, max_steps: int = 10) -> AgentResult:
        '''TODO: 实现ReAct循环'''
        # TODO: 实现主循环
        pass


class PlanAndExecuteAgent(BaseAgent):
    '''Plan-and-Execute Agent 实现
    
    TODO: 实现先规划后执行的Agent
    '''
    
    def __init__(self, llm_provider=None):
        super().__init__()
        self.llm_provider = llm_provider or self._default_llm
    
    def _default_llm(self, prompt: str) -> str:
        '''默认LLM（模拟）'''
        import json
        return json.dumps({
            "plan": ["步骤1", "步骤2"],
            "answer": "执行完成"
        })
    
    def _think(self, context: str) -> dict:
        '''TODO: 实现规划逻辑'''
        pass
    
    def run(self, query: str, max_steps: int = 10) -> AgentResult:
        '''TODO: 实现规划执行循环'''
        pass
