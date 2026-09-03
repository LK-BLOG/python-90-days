# Day 79 示例 3: 计划执行器
from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class Task:
    id: str; desc: str; tool: str = ''; depends_on: List[str] = field(default_factory=list); status: str = 'pending'; result: str = ''

class PlanExecutor:
    def __init__(self, tools: dict):
        self.tools = tools
        self.results: Dict[str, any] = {}
    
    def execute(self, tasks: List[Task]) -> str:
        for _ in range(len(tasks) * 2):
            done = {t.id for t in tasks if t.status == 'completed'}
            ready = [t for t in tasks if t.status == 'pending' and all(d in done for d in t.depends_on)]
            if not ready:
                break
            for task in ready:
                task.status = 'running'
                tool = self.tools.get(task.tool)
                if not tool:
                    task.status = 'failed'; task.result = f'无工具: {task.tool}'; continue
                result = tool(task.id, self.results)
                task.status = 'completed'; task.result = result; self.results[task.id] = result
                print(f'  ✅ {task.desc}: {result}')
        return self.results

# 演示
if __name__ == '__main__':
    tools = {
        'search': lambda tid, ctx: f'{tid}搜索结果',
        'analyze': lambda tid, ctx: f'{tid}分析: 基于 {list(ctx.keys())}',
        'write': lambda tid, ctx: f'{tid}报告已生成',
    }
    tasks = [
        Task('t1', '收集数据', 'search'),
        Task('t2', '分析数据', 'analyze', ['t1']),
        Task('t3', '写报告', 'write', ['t2']),
    ]
    executor = PlanExecutor(tools)
    executor.execute(tasks)
