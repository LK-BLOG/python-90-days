# Day 84 课程：Multi-Agent 系统

## 1. 多Agent协作模式

`python
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable
from datetime import datetime
import asyncio
from abc import ABC, abstractmethod


class CollaborationMode(Enum):
    '''协作模式'''
    MASTER_SLAVE = "master_slave"  # 主从模式
    PEER_TO_PEER = "peer_to_peer"  # 对等模式
    COMPETITIVE = "competitive"    # 竞争模式
    PIPELINE = "pipeline"          # 流水线模式


@dataclass
class AgentMessage:
    '''Agent消息'''
    sender: str
    receiver: str | None  # None表示广播
    content: Any
    msg_type: str = "task"  # task, result, info
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: dict = field(default_factory=dict)


class BaseAgent(ABC):
    '''Agent基类'''
    
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role
        self.inbox: list[AgentMessage] = []
        self.outbox: list[AgentMessage] = []
    
    @abstractmethod
    async def process(self, message: AgentMessage) -> AgentMessage | None:
        '''处理消息'''
        pass
    
    def send(self, receiver: str, content: Any, msg_type: str = "task"):
        '''发送消息'''
        msg = AgentMessage(
            sender=self.name,
            receiver=receiver,
            content=content,
            msg_type=msg_type
        )
        self.outbox.append(msg)
        return msg
    
    def receive(self, message: AgentMessage):
        '''接收消息'''
        self.inbox.append(message)
    
    def get_pending_messages(self) -> list[AgentMessage]:
        '''获取待处理消息'''
        messages = self.inbox.copy()
        self.inbox.clear()
        return messages
`

## 2. Agent间通信协议

`python
class MessageBus:
    '''消息总线'''
    
    def __init__(self):
        self.agents: dict[str, BaseAgent] = {}
        self.message_history: list[AgentMessage] = []
    
    def register_agent(self, agent: BaseAgent):
        '''注册Agent'''
        self.agents[agent.name] = agent
    
    def send_message(self, message: AgentMessage):
        '''发送消息'''
        self.message_history.append(message)
        
        if message.receiver is None:
            # 广播
            for name, agent in self.agents.items():
                if name != message.sender:
                    agent.receive(message)
        elif message.receiver in self.agents:
            self.agents[message.receiver].receive(message)
    
    async def process_messages(self):
        '''处理所有消息'''
        for agent in self.agents.values():
            messages = agent.get_pending_messages()
            for msg in messages:
                response = await agent.process(msg)
                if response:
                    self.send_message(response)
`

## 3. 主从模式实现

`python
class MasterAgent(BaseAgent):
    '''主Agent'''
    
    def __init__(self, name: str = "master"):
        super().__init__(name, "master")
        self.slaves: list[str] = []
        self.task_results: dict[str, Any] = {}
    
    def add_slave(self, slave_name: str):
        '''添加从Agent'''
        self.slaves.append(slave_name)
    
    async def process(self, message: AgentMessage) -> AgentMessage | None:
        '''处理消息'''
        if message.msg_type == "result":
            # 收集结果
            self.task_results[message.sender] = message.content
            return None
        
        return None
    
    def distribute_task(self, task: str, data: dict = None):
        '''分配任务'''
        for slave_name in self.slaves:
            msg = AgentMessage(
                sender=self.name,
                receiver=slave_name,
                content={"task": task, "data": data},
                msg_type="task"
            )
            self.send(slave_name, msg.content, "task")
    
    def collect_results(self) -> dict:
        '''收集结果'''
        return self.task_results.copy()


class WorkerAgent(BaseAgent):
    '''工作Agent'''
    
    def __init__(self, name: str, task_handler: Callable = None):
        super().__init__(name, "worker")
        self.task_handler = task_handler or self._default_handler
    
    async def process(self, message: AgentMessage) -> AgentMessage | None:
        '''处理任务'''
        if message.msg_type == "task":
            task = message.content.get("task")
            data = message.content.get("data")
            
            # 执行任务
            result = await self.task_handler(task, data)
            
            # 返回结果
            return self.send(message.sender, result, "result")
        
        return None
    
    async def _default_handler(self, task: str, data: dict = None) -> Any:
        '''默认任务处理'''
        return f"{self.name} 完成了任务: {task}"
`

## 4. 流水线模式实现

`python
class PipelineStage:
    '''流水线阶段'''
    
    def __init__(self, name: str, processor: Callable):
        self.name = name
        self.processor = processor
    
    async def process(self, data: Any) -> Any:
        '''处理数据'''
        return await self.processor(data)


class Pipeline:
    '''流水线'''
    
    def __init__(self, name: str):
        self.name = name
        self.stages: list[PipelineStage] = []
        self.results: list[dict] = []
    
    def add_stage(self, name: str, processor: Callable):
        '''添加阶段'''
        self.stages.append(PipelineStage(name, processor))
    
    async def execute(self, initial_data: Any) -> Any:
        '''执行流水线'''
        current_data = initial_data
        
        for stage in self.stages:
            print(f"执行阶段: {stage.name}")
            
            result = await stage.process(current_data)
            
            self.results.append({
                "stage": stage.name,
                "input": str(current_data)[:100],
                "output": str(result)[:100]
            })
            
            current_data = result
        
        return current_data
`

## 5. CrewAI风格的多Agent系统

`python
@dataclass
class Role:
    '''角色定义'''
    name: str
    goal: str
    backstory: str
    tools: list[str] = field(default_factory=list)


@dataclass
class Task:
    '''任务定义'''
    description: str
    agent_role: str
    expected_output: str = ""
    dependencies: list[str] = field(default_factory=list)


class Crew:
    '''团队'''
    
    def __init__(self, name: str):
        self.name = name
        self.roles: dict[str, Role] = {}
        self.tasks: list[Task] = []
        self.results: dict[str, str] = {}
    
    def add_role(self, role: Role):
        '''添加角色'''
        self.roles[role.name] = role
    
    def add_task(self, task: Task):
        '''添加任务'''
        self.tasks.append(task)
    
    async def execute(self) -> dict:
        '''执行所有任务'''
        for task in self.tasks:
            # 检查依赖
            deps_met = all(
                dep in self.results
                for dep in task.dependencies
            )
            
            if not deps_met:
                print(f"任务 {task.description} 的依赖未满足，跳过")
                continue
            
            # 执行任务
            role = self.roles.get(task.agent_role)
            if role:
                print(f"执行任务: {task.description} (角色: {role.name})")
                result = await self._execute_task(task, role)
                self.results[task.description] = result
        
        return self.results
    
    async def _execute_task(self, task: Task, role: Role) -> str:
        '''执行单个任务（模拟）'''
        # 实际实现中，这里应该调用LLM
        return f"任务 '{task.description}' 已由 {role.name} 完成"
`

## 6. 本日总结

- 多Agent系统有多种协作模式
- MessageBus实现Agent间通信
- MasterAgent/WorkerAgent实现主从模式
- Pipeline实现流水线模式
- Crew实现团队协作

明天我们将学习Agent工作流。
