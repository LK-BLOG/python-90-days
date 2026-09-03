# Day 84 示例 1: 消息总线
from dataclasses import dataclass, field
from collections import defaultdict
import uuid, time
from typing import Dict, List, Any, Optional

@dataclass
class Message:
    sender: str; receiver: str; content: Any; msg_type: str = 'text'
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    timestamp: float = field(default_factory=time.time)

class MessageBus:
    def __init__(self):
        self.inboxes: Dict[str, List[Message]] = defaultdict(list)
    def send(self, msg: Message):
        if msg.receiver:
            self.inboxes[msg.receiver].append(msg)
        else:
            for k in self.inboxes: self.inboxes[k].append(msg)
    def receive(self, agent_id: str) -> Optional[Message]:
        return self.inboxes[agent_id].pop(0) if self.inboxes[agent_id] else None
    def receive_all(self, agent_id: str) -> List[Message]:
        msgs = list(self.inboxes[agent_id]); self.inboxes[agent_id].clear(); return msgs

if __name__ == '__main__':
    bus = MessageBus()
    bus.send(Message('alice', 'bob', '你好'))
    bus.send(Message('alice', 'bob', '在吗'))
    print(f'bob 收到: {[m.content for m in bus.receive_all("bob")]}')
