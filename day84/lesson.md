# Day 84: Multi-Agent 系统

## 1. 为什么需要多 Agent？

单个 Agent 处理复杂任务时：
- 上下文太长，容易混乱
- 角色不专一，什么都做不好
- 推理链太长，容易出错

多 Agent 通过**分工协作**解决这些问题：

`
┌──────────┐  ┌──────────┐  ┌──────────┐
│ 研究 Agent │  │ 编码 Agent │  │ 审核 Agent │
│ (搜索分析) │  │ (写代码)   │  │ (质量检查) │
└─────┬─────┘  └─────┬─────┘  └─────┬─────┘
      │              │              │
      └──────────────┴──────────────┘
                     │
              ┌──────┴──────┐
              │  协调 Agent  │
              │ (任务分发)   │
              └─────────────┘
`

## 2. Agent 间通信

### 2.1 消息传递

`python
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Callable
from collections import defaultdict
import time
import uuid


@dataclass
class Message:
    \"\"\"Agent 间消息\"\"\"
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    sender: str = ""
    receiver: str = ""  # 空字符串表示广播
    content: Any = None
    msg_type: str = "text"  # text, task, result, error
    timestamp: float = field(default_factory=time.time)
    reply_to: str = ""


class MessageBus:
    \"\"\"消息总线 - Agent 间通信\"\"\"
    
    def __init__(self):
        self.inboxes: Dict[str, List[Message]] = defaultdict(list)
        self.subscribers: Dict[str, List[Callable]] = defaultdict(list)
    
    def send(self, message: Message):
        if message.receiver:
            self.inboxes[message.receiver].append(message)
        else:
            # 广播
            for agent_id in self.subscribers:
                self.inboxes[agent_id].append(message)
        
        # 触发订阅回调
        target = message.receiver or "all"
        for callback in self.subscribers.get(target, []):
            callback(message)
    
    def receive(self, agent_id: str) -> Optional[Message]:
        if self.inboxes[agent_id]:
            return self.inboxes[agent_id].pop(0)
        return None
    
    def receive_all(self, agent_id: str) -> List[Message]:
        messages = list(self.inboxes[agent_id])
        self.inboxes[agent_id].clear()
        return messages
    
    def subscribe(self, agent_id: str, callback: Callable):
        self.subscribers[agent_id].append(callback)
    
    def get_conversation(self, agent1: str, agent2: str) -> List[Message]:
        # 返回两个 Agent 之间的对话
        all_msgs = []
        for msgs in self.inboxes.values():
            for m in msgs:
                if (m.sender == agent1 and m.receiver == agent2) or \
                   (m.sender == agent2 and m.receiver == agent1):
                    all_msgs.append(m)
        return sorted(all_msgs, key=lambda m: m.timestamp)
`

## 3. Agent 角色定义

`python
class BaseAgent:
    \"\"\"Agent 基类\"\"\"
    
    def __init__(self, agent_id: str, role: str, description: str, bus: MessageBus):
        self.agent_id = agent_id
        self.role = role
        self.description = description
        self.bus = bus
        self.is_running = False
    
    def send(self, receiver: str, content: Any, msg_type: str = "text"):
        msg = Message(sender=self.agent_id, receiver=receiver, content=content, msg_type=msg_type)
        self.bus.send(msg)
    
    def receive(self) -> Optional[Message]:
        return self.bus.receive(self.agent_id)
    
    def receive_all(self) -> List[Message]:
        return self.bus.receive_all(self.agent_id)
    
    def run(self):
        \"\"\"Agent 主循环\"\"\"
        self.is_running = True
        while self.is_running:
            msg = self.receive()
            if msg:
                response = self.process(msg)
                if response:
                    self.send(msg.sender, response)
            time.sleep(0.1)  # 避免 CPU 空转
    
    def process(self, message: Message) -> Any:
        raise NotImplementedError


class ResearchAgent(BaseAgent):
    \"\"\"研究 Agent\"\"\"
    
    def __init__(self, bus: MessageBus):
        super().__init__("researcher", "研究员", "负责搜索和分析信息", bus)
        self.knowledge = []
    
    def process(self, message: Message) -> str:
        if message.msg_type == "task":
            query = message.content
            # 模拟搜索
            result = f"研究结果: 关于 '{query}' 的分析..."
            self.knowledge.append(result)
            return result
        return None


class CoderAgent(BaseAgent):
    \"\"\"编码 Agent\"\"\"
    
    def __init__(self, bus: MessageBus):
        super().__init__("coder", "程序员", "负责编写代码", bus)
    
    def process(self, message: Message) -> str:
        if message.msg_type == "task":
            spec = message.content
            # 模拟代码生成
            return f"生成的代码: # {spec}\nprint('Hello')"
        return None


class ReviewerAgent(BaseAgent):
    \"\"\"审核 Agent\"\"\"
    
    def __init__(self, bus: MessageBus):
        super().__init__("reviewer", "审核员", "负责代码审核", bus)
    
    def process(self, message: Message) -> str:
        if message.msg_type == "code":
            return f"审核通过 ✅: {message.content[:50]}..."
        return None
`

## 4. 多 Agent 协作模式

### 4.1 顺序模式（Pipeline）

`python
class SequentialOrchestrator:
    \"\"\"顺序执行 - Agent 按流水线工作\"\"\"
    
    def __init__(self, agents: List[BaseAgent]):
        self.agents = agents
        self.bus = agents[0].bus if agents else MessageBus()
    
    def run(self, initial_input: str) -> str:
        current_input = initial_input
        
        for agent in self.agents:
            print(f"\n🔄 {agent.role} ({agent.agent_id}) 开始处理...")
            
            # 发送任务
            msg = Message(
                sender="orchestrator",
                receiver=agent.agent_id,
                content=current_input,
                msg_type="task"
            )
            self.bus.send(msg)
            
            # 等待结果
            time.sleep(0.5)
            response = agent.receive()
            if response:
                current_input = response.content
                print(f"  ✅ 完成: {str(current_input)[:100]}")
        
        return current_input
`

### 4.2 协作模式（Discussion）

`python
class DiscussionOrchestrator:
    \"\"\"讨论模式 - Agent 之间互相讨论\"\"\"
    
    def __init__(self, agents: List[BaseAgent], max_rounds: int = 3):
        self.agents = {a.agent_id: a for a in agents}
        self.bus = agents[0].bus if agents else MessageBus()
        self.max_rounds = max_rounds
        self.discussion_log = []
    
    def run(self, topic: str) -> str:
        print(f"💬 讨论主题: {topic}\n")
        
        # 广播主题
        self.bus.send(Message(
            sender="orchestrator",
            content=topic,
            msg_type="task"
        ))
        
        for round_num in range(self.max_rounds):
            print(f"--- 第 {round_num + 1} 轮 ---")
            
            for agent_id, agent in self.agents.items():
                messages = agent.receive_all()
                for msg in messages:
                    response = agent.process(msg)
                    if response:
                        self.discussion_log.append({
                            "round": round_num,
                            "agent": agent_id,
                            "response": response
                        })
                        # 广播给其他 Agent
                        self.bus.send(Message(
                            sender=agent_id,
                            content=response,
                            msg_type="discussion"
                        ))
                        print(f"  [{agent_id}]: {str(response)[:80]}")
        
        return self._synthesize()
    
    def _synthesize(self) -> str:
        return "\n".join([
            f"  [{log['agent']}]: {log['response'][:50]}"
            for log in self.discussion_log
        ])
`

## 5. AutoGen / CrewAI 概念

`python
# AutoGen 风格：Agent 之间通过对话协作
# 核心概念：GroupChat + GroupChatManager

class GroupChat:
    \"\"\"群聊管理器（AutoGen 风格）\"\"\"
    
    def __init__(self, agents: List[BaseAgent], max_turns: int = 10):
        self.agents = {a.agent_id: a for a in agents}
        self.max_turns = max_turns
        self.messages: List[Dict] = []
    
    def run(self, initial_message: str) -> str:
        self.messages.append({"role": "user", "content": initial_message})
        
        speaker_idx = 0
        agent_ids = list(self.agents.keys())
        
        for turn in range(self.max_turns):
            speaker_id = agent_ids[speaker_idx % len(agent_ids)]
            agent = self.agents[speaker_id]
            
            # 获取上下文
            context = "\n".join([f"{m['role']}: {m['content']}" for m in self.messages[-5:]])
            
            # Agent 响应
            response = f"[{agent.role}] 基于讨论: {context[-100:]}"
            self.messages.append({"role": speaker_id, "content": response})
            
            print(f"  [{speaker_id}]: {response[:80]}")
            
            speaker_idx += 1
        
        return self.messages[-1]["content"]
`

## 6. 常见错误

1. **通信风暴**：Agent 互相发消息太多 → 设置消息限制
2. **死锁**：Agent A 等 B，B 等 A → 添加超时机制
3. **角色重叠**：两个 Agent 做同样的事 → 明确分工
4. **没有仲裁**：Agent 间意见冲突 → 设置仲裁 Agent
5. **成本爆炸**：每个 Agent 都调 LLM → 控制调用频率

## 7. 动手练习

### 练习 1：实现消息总线
### 练习 2：实现 Research + Coder 两个 Agent
### 练习 3：实现顺序执行模式
