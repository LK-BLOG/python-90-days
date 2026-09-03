# Day 79 示例 2: 层次化规划器
from dataclasses import dataclass, field
from typing import List

@dataclass
class Task:
    id: str
    desc: str
    tool: str = ''
    depends_on: List[str] = field(default_factory=list)
    subtasks: List['Task'] = field(default_factory=list)

class HierarchicalPlanner:
    def decompose_goal(self, goal: str) -> List[Task]:
        # Level 1: 高层分解
        if '报告' in goal:
            high = [
                Task('h1', '收集数据', subtasks=[
                    Task('h1_1', '搜索新闻', 'search'),
                    Task('h1_2', '查询数据库', 'db_query'),
                ]),
                Task('h2', '分析数据', 'analyze', depends_on=['h1']),
                Task('h3', '写报告', 'write', depends_on=['h2']),
            ]
        else:
            high = [Task('h1', f'执行: {goal}', 'execute')]
        return self._flatten(high)
    
    def _flatten(self, tasks: List[Task]) -> List[Task]:
        flat = []
        for t in tasks:
            if t.subtasks:
                flat.extend(self._flatten(t.subtasks))
            else:
                flat.append(t)
        return flat
    
    def validate(self, tasks: List[Task]) -> tuple:
        ids = {t.id for t in tasks}
        for t in tasks:
            for d in t.depends_on:
                if d not in ids:
                    return False, f'{t.id} 依赖 {d} 不存在'
        return True, 'OK'

if __name__ == '__main__':
    p = HierarchicalPlanner()
    tasks = p.decompose_goal('生成年度报告')
    for t in tasks:
        print(f'  {t.id}: {t.desc} -> {t.tool}')
    print(f'  验证: {p.validate(tasks)}')
