# Day 79 示例 1: 目标分解
from dataclasses import dataclass, field
from typing import List
from enum import Enum

class TaskStatus(Enum):
    PENDING = 'pending'
    RUNNING = 'running'
    COMPLETED = 'completed'
    FAILED = 'failed'

@dataclass
class Task:
    id: str
    description: str
    tool: str = ''
    depends_on: List[str] = field(default_factory=list)
    status: TaskStatus = TaskStatus.PENDING
    result: str = ''

@dataclass
class Plan:
    goal: str
    tasks: List[Task]
    
    def get_ready(self) -> List[Task]:
        done = {t.id for t in self.tasks if t.status == TaskStatus.COMPLETED}
        return [t for t in self.tasks if t.status == TaskStatus.PENDING and all(d in done for d in t.depends_on)]
    
    def is_complete(self) -> bool:
        return all(t.status == TaskStatus.COMPLETED for t in self.tasks)

class Planner:
    def decompose(self, goal: str) -> Plan:
        # 模拟 LLM 分解
        tasks = [
            Task('t1', '收集数据', 'search'),
            Task('t2', '分析数据', 'analyze', depends_on=['t1']),
            Task('t3', '生成报告', 'write', depends_on=['t2']),
        ]
        return Plan(goal=goal, tasks=tasks)

if __name__ == '__main__':
    planner = Planner()
    plan = planner.decompose('生成市场分析报告')
    for t in plan.tasks:
        print(f'  {t.id}: {t.description} (依赖: {t.depends_on})')
    print(f'  可执行: {[t.id for t in plan.get_ready()]}')
