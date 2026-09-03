# Day 83 示例 1: 检查点管理器
import json, time
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class StepCP:
    step_id: str; tool: str; input_data: dict; output: Any = None; status: str = 'pending'; error: str = ''

@dataclass
class AgentCP:
    agent_id: str; state: str; goal: str; step_idx: int = 0; steps: List[StepCP] = field(default_factory=list)
    def to_dict(self): return {'agent_id': self.agent_id, 'state': self.state, 'goal': self.goal, 'step_idx': self.step_idx, 'steps': [{'step_id':s.step_id,'tool':s.tool,'input':s.input_data,'output':s.output,'status':s.status,'error':s.error} for s in self.steps]}

class CheckpointManager:
    def __init__(self, path='./checkpoints'):
        self.path = Path(path); self.path.mkdir(exist_ok=True)
    def save(self, cp: AgentCP):
        (self.path/f'{cp.agent_id}.json').write_text(json.dumps(cp.to_dict(), ensure_ascii=False, indent=2))
    def load(self, agent_id: str):
        fp = self.path/f'{agent_id}.json'
        if not fp.exists(): return None
        d = json.loads(fp.read_text())
        return AgentCP(d['agent_id'], d['state'], d['goal'], d['step_idx'], [StepCP(**s) for s in d['steps']])

if __name__ == '__main__':
    mgr = CheckpointManager('/tmp/test_cp')
    cp = AgentCP('agent1', 'executing', '测试任务', 0, [StepCP('s1','calc',{'expr':'1+1'}), StepCP('s2','search',{'query':'hello'})])
    mgr.save(cp)
    loaded = mgr.load('agent1')
    print(f'加载检查点: {loaded.agent_id}, 步骤: {len(loaded.steps)}')
    import shutil; shutil.rmtree('/tmp/test_cp')
