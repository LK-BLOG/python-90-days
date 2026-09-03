# Day 84 示例 3: 顺序执行模式
class Pipeline:
    def __init__(self, agents): self.agents = agents
    def run(self, input_data):
        current = input_data
        for agent in self.agents:
            print(f'  🔄 {agent.role} 处理中...')
            msg = Message('pipeline', agent.agent_id, current, 'task')
            agent.bus.send(msg)
            m = agent.receive()
            if m:
                current = agent.process(m)
                print(f'  ✅ {agent.role}: {str(current)[:60]}')
        return current

if __name__ == '__main__':
    bus = MessageBus()
    agents = [ResearchAgent(bus), CoderAgent(bus)]
    p = Pipeline(agents)
    result = p.run('实现快速排序')
    print(f'最终结果: {result}')
