'''
Day 84 示例：多Agent协作系统
'''

from dataclasses import dataclass, field
from typing import Any
from datetime import datetime
import asyncio


@dataclass
class AgentMessage:
    '''Agent消息'''
    sender: str
    receiver: str | None
    content: Any
    msg_type: str = "task"
    timestamp: datetime = field(default_factory=datetime.now)


class BaseAgent:
    '''Agent基类'''
    
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role
        self.inbox: list[AgentMessage] = []
    
    def receive(self, message: AgentMessage):
        '''接收消息'''
        self.inbox.append(message)
    
    def send(self, bus: 'MessageBus', receiver: str, content: Any, msg_type: str = "task"):
        '''发送消息'''
        msg = AgentMessage(
            sender=self.name,
            receiver=receiver,
            content=content,
            msg_type=msg_type
        )
        bus.send_message(msg)
    
    async def process(self, message: AgentMessage) -> str:
        '''处理消息'''
        return f"{self.name} 处理了消息"


class MessageBus:
    '''消息总线'''
    
    def __init__(self):
        self.agents: dict[str, BaseAgent] = {}
        self.history: list[AgentMessage] = []
    
    def register(self, agent: BaseAgent):
        '''注册Agent'''
        self.agents[agent.name] = agent
        print(f"注册Agent: {agent.name} ({agent.role})")
    
    def send_message(self, message: AgentMessage):
        '''发送消息'''
        self.history.append(message)
        
        if message.receiver and message.receiver in self.agents:
            self.agents[message.receiver].receive(message)
            print(f"  {message.sender} -> {message.receiver}: {str(message.content)[:50]}")
    
    async def process_all(self):
        '''处理所有消息'''
        for agent in self.agents.values():
            while agent.inbox:
                msg = agent.inbox.pop(0)
                result = await agent.process(msg)
                print(f"  处理结果: {result}")


class MasterAgent(BaseAgent):
    '''主Agent'''
    
    def __init__(self, name: str = "master"):
        super().__init__(name, "master")
        self.workers: list[str] = []
    
    def add_worker(self, worker_name: str):
        '''添加工作Agent'''
        self.workers.append(worker_name)
    
    async def process(self, message: AgentMessage) -> str:
        '''处理消息'''
        if message.msg_type == "result":
            return f"收到结果: {message.content}"
        return f"主Agent收到: {message.content}"
    
    def distribute_task(self, bus: MessageBus, task: str):
        '''分配任务'''
        for worker in self.workers:
            self.send(bus, worker, {"task": task}, "task")


class WorkerAgent(BaseAgent):
    '''工作Agent'''
    
    async def process(self, message: AgentMessage) -> str:
        '''处理任务'''
        task = message.content.get("task", "")
        return f"完成任务: {task}"


async def main():
    '''演示多Agent系统'''
    print("=" * 60)
    print("多Agent协作系统演示")
    print("=" * 60)
    
    # 创建消息总线
    bus = MessageBus()
    
    # 创建Agent
    master = MasterAgent()
    workers = [
        WorkerAgent("researcher"),
        WorkerAgent("writer"),
        WorkerAgent("reviewer")
    ]
    
    # 注册Agent
    bus.register(master)
    for worker in workers:
        bus.register(worker)
        master.add_worker(worker.name)
    
    # 分配任务
    print("\n1. 分配任务:")
    master.distribute_task(bus, "分析Python最新趋势")
    
    # 处理消息
    print("\n2. 处理消息:")
    await bus.process_all()
    
    # 模拟结果返回
    print("\n3. 结果返回:")
    for worker in workers:
        worker.send(bus, "master", "任务完成", "result")
    
    await bus.process_all()
    
    print("\n" + "=" * 60)
    print("演示完成！")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
