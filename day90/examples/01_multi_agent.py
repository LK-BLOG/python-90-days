# Day 90 示例 1: 多 Agent 系统
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from collections import defaultdict
import uuid, time

@dataclass
class AgentMsg:
    sender: str; receiver: str; content: Any; msg_type: str = 'text'
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    ts: float = field(default_factory=time.time)

class MultiAgentBus:
    def __init__(self): self.inboxes = defaultdict(list); self.log = []
    def send(self, msg: AgentMsg): self.inboxes[msg.receiver].append(msg); self.log.append(msg)
    def receive(self, agent_id): return self.inboxes[agent_id].pop(0) if self.inboxes[agent_id] else None
    def receive_all(self, agent_id):
        msgs = list(self.inboxes[agent_id]); self.inboxes[agent_id].clear(); return msgs

class SimpleAgent:
    def __init__(self, agent_id, role, bus):
        self.agent_id = agent_id; self.role = role; self.bus = bus
    def send(self, receiver, content, msg_type='text'):
        self.bus.send(AgentMsg(self.agent_id, receiver, content, msg_type))
    def receive(self): return self.bus.receive(self.agent_id)
    def process(self, msg): return f'[{self.role}] 处理: {msg.content}'

class MultiAgentRuntime:
    def __init__(self):
        self.agents = {}; self.bus = MultiAgentBus()
    def register(self, agent_id, agent): self.agents[agent_id] = agent
    def run_task(self, task):
        results = []
        for aid, agent in self.agents.items():
            self.bus.send(AgentMsg('system', aid, task, 'task'))
            msg = agent.receive()
            if msg: results.append(agent.process(msg))
        return results

if __name__ == '__main__':
    bus = MultiAgentBus()
    runtime = MultiAgentRuntime()
    runtime.register('researcher', SimpleAgent('researcher', '研究员', bus))
    runtime.register('coder', SimpleAgent('coder', '程序员', bus))
    results = runtime.run_task('分析数据并写代码')
    for r in results: print(f'  {r}')
