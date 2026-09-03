# Day 84 骨架代码
class MessageBus:
    def __init__(self): pass
    def send(self, msg): pass
    def receive(self, agent_id): pass

class BaseAgent:
    def __init__(self, agent_id, role, bus): pass
    def send(self, receiver, content): pass
    def process(self, msg): pass

class Pipeline:
    def __init__(self, agents): pass
    def run(self, input_data): pass
