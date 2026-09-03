# Day 88 示例 1: Agent Loop 核心引擎
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from enum import Enum
import time

class AgentState(Enum):
    IDLE = 'idle'; THINKING = 'thinking'; ACTING = 'acting'; COMPLETE = 'complete'; ERROR = 'error'

@dataclass
class AgentStep:
    step_id: str; thought: str = ''; action: str = ''; action_input: dict = field(default_factory=dict)
    observation: str = ''; duration: float = 0.0

class AgentLoop:
    def __init__(self, max_steps=10):
        self.max_steps = max_steps; self.state = AgentState.IDLE
        self.steps: List[AgentStep] = []; self.memory: List[Dict] = []
        self.tools: Dict[str, Any] = {}
    
    def register_tool(self, name, tool): self.tools[name] = tool
    
    def run(self, goal: str) -> str:
        print(f'🚀 开始: {goal}')
        for i in range(self.max_steps):
            step = AgentStep(f's{i}')
            # Think
            step.thought = self._think(goal, i)
            print(f'💭 {step.thought}')
            # Act
            action = self._decide(step.thought, goal)
            step.action = action['action']; step.action_input = action.get('input', {})
            # Execute
            t0 = time.time()
            step.observation = self._execute(step.action, step.action_input)
            step.duration = time.time() - t0
            print(f'  🔧 {step.action}: {step.observation[:60]}')
            # Check complete
            if step.observation.startswith('FINISH:'):
                self.steps.append(step)
                return step.observation.replace('FINISH: ', '')
            self.memory.append({'step': i, 'thought': step.thought, 'obs': step.observation})
            self.steps.append(step)
        return '达到最大步数'
    
    def _think(self, goal, step_num): return f'分析: {goal}' if step_num == 0 else '继续...'
    def _decide(self, thought, goal): return {'action': 'finish', 'input': {'answer': f'{goal}的结果'}}
    def _execute(self, action, input_data):
        if action == 'finish': return f'FINISH: {input_data.get("answer","")}'
        tool = self.tools.get(action)
        if not tool: return f'错误: 无工具 {action}'
        try: return str(tool(**input_data))
        except Exception as e: return f'错误: {e}'
    
    def get_trace(self):
        return [{'step': s.step_id, 'action': s.action, 'obs': s.observation[:50], 'time': f'{s.duration:.2f}s'} for s in self.steps]

if __name__ == '__main__':
    agent = AgentLoop(max_steps=5)
    agent.register_tool('calc', lambda expression='': str(eval(expression)))
    result = agent.run('计算 2+3*4')
    print(f'\n结果: {result}')
    print(f'追踪: {agent.get_trace()}')
