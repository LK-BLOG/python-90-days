# Day 84 示例 2: Agent 基类 + 角色
class BaseAgent:
    def __init__(self, agent_id, role, bus):
        self.agent_id = agent_id; self.role = role; self.bus = bus
    def send(self, receiver, content, msg_type='text'):
        self.bus.send(Message(self.agent_id, receiver, content, msg_type))
    def receive(self): return self.bus.receive(self.agent_id)
    def process(self, msg): raise NotImplementedError

class ResearchAgent(BaseAgent):
    def __init__(self, bus):
        super().__init__('researcher', '研究员', bus)
    def process(self, msg):
        return f'研究结果: {msg.content}'

class CoderAgent(BaseAgent):
    def __init__(self, bus):
        super().__init__('coder', '程序员', bus)
    def process(self, msg):
        return f'代码: print("{msg.content}")'

if __name__ == '__main__':
    bus = MessageBus()
    r = ResearchAgent(bus); c = CoderAgent(bus)
    bus.send(Message('user', 'researcher', 'Python排序算法'))
    m = r.receive()
    result = r.process(m)
    print(f'研究员: {result}')
    c.send('user', result)
    m2 = c.receive()
    print(f'程序员: {c.process(m2)}')
