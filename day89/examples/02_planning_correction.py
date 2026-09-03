# Day 89 示例 2: Planning + Self-Correction
from dataclasses import dataclass, field
from typing import List, Dict
from enum import Enum

class TaskStatus(Enum):
    PENDING='pending'; RUNNING='running'; COMPLETED='completed'; FAILED='failed'

@dataclass
class Task:
    id: str; desc: str; tool: str = ''; status: TaskStatus = TaskStatus.PENDING; result: str = ''

class Plan:
    def __init__(self, goal, tasks): self.goal = goal; self.tasks = tasks
    def get_ready(self):
        done = {t.id for t in self.tasks if t.status==TaskStatus.COMPLETED}
        return [t for t in self.tasks if t.status==TaskStatus.PENDING and all(d in done for d in (getattr(t,'depends',[]) or []))]
    def is_complete(self): return all(t.status==TaskStatus.COMPLETED for t in self.tasks)

class SelfCorrection:
    def check(self, output): return [] if len(output)>10 else ['太短']
    def correct(self, output, issues): return f'{output} [已修正{len(issues)}个问题]'

if __name__ == '__main__':
    plan = Plan('测试', [Task('t1','步骤1','calc'), Task('t2','步骤2','search')])
    sc = SelfCorrection()
    for t in plan.get_ready() or plan.tasks[:1]:
        t.status = TaskStatus.COMPLETED; t.result = '结果'
        issues = sc.check(t.result)
        if issues: t.result = sc.correct(t.result, issues)
        print(f'{t.desc}: {t.result}')
