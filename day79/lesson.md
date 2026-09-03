# Day 79: Planning & Goal Decomposition

## 1. 目标分解

### 1.1 为什么需要规划？

没有规划的 Agent 就像没头苍蝇。规划让 Agent：
- **降低复杂度**：把大问题拆成小问题
- **提高成功率**：每步都有明确目标
- **便于监控**：知道在做什么、做到哪了
- **支持回退**：失败了可以回到某个检查点

### 1.2 目标分解方法

`python
from dataclasses import dataclass, field
from typing import List, Optional, Dict
from enum import Enum


class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    BLOCKED = "blocked"


@dataclass
class Task:
    \"\"\"任务定义\"\"\"
    id: str
    description: str
    tool: str = ""
    params: dict = field(default_factory=dict)
    depends_on: List[str] = field(default_factory=list)
    status: TaskStatus = TaskStatus.PENDING
    result: Optional[str] = None
    subtasks: List['Task'] = field(default_factory=list)
    depth: int = 0  # 层次深度


@dataclass
class Plan:
    \"\"\"计划定义\"\"\"
    goal: str
    tasks: List[Task]
    status: str = "created"
    
    def get_ready_tasks(self) -> List[Task]:
        \"\"\"获取可以执行的任务（依赖都完成）\"\"\"
        completed_ids = {
            t.id for t in self.tasks 
            if t.status == TaskStatus.COMPLETED
        }
        return [
            t for t in self.tasks
            if t.status == TaskStatus.PENDING
            and all(dep in completed_ids for dep in t.depends_on)
        ]
    
    def is_complete(self) -> bool:
        return all(t.status == TaskStatus.COMPLETED for t in self.tasks)
`

## 2. Planner 规划器

`python
class HierarchicalPlanner:
    \"\"\"层次化规划器\"\"\"
    
    def __init__(self, available_tools: dict):
        self.tools = available_tools
    
    def decompose(self, goal: str) -> Plan:
        \"\"\"将目标分解为任务计划\"\"\"
        # Level 1: 高层任务分解
        high_level_tasks = self._decompose_goal(goal)
        
        # Level 2: 每个高层任务进一步分解
        all_tasks = []
        for ht in high_level_tasks:
            subtasks = self._decompose_task(ht)
            all_tasks.extend(subtasks)
        
        return Plan(goal=goal, tasks=all_tasks)
    
    def _decompose_goal(self, goal: str) -> List[dict]:
        \"\"\"目标分解（实际项目中由 LLM 完成）\"\"\"
        # 模拟 LLM 分解
        if "报告" in goal:
            return [
                {"id": "t1", "desc": "收集数据", "tool": "search"},
                {"id": "t2", "desc": "分析数据", "tool": "analyze", "depends": ["t1"]},
                {"id": "t3", "desc": "生成报告", "tool": "write", "depends": ["t2"]},
            ]
        return [
            {"id": "t1", "desc": f"分析: {goal}", "tool": "analyze"},
            {"id": "t2", "desc": f"执行: {goal}", "tool": "execute", "depends": ["t1"]},
        ]
    
    def _decompose_task(self, task_def: dict) -> List[Task]:
        \"\"\"将高层任务分解为可执行的子任务\"\"\"
        # 简化：直接创建 Task
        return [Task(
            id=task_def["id"],
            description=task_def["desc"],
            tool=task_def.get("tool", ""),
            depends_on=task_def.get("depends", [])
        )]
    
    def validate_plan(self, plan: Plan) -> tuple[bool, str]:
        \"\"\"验证计划的正确性\"\"\"
        # 检查循环依赖
        task_ids = {t.id for t in plan.tasks}
        for task in plan.tasks:
            for dep in task.depends_on:
                if dep not in task_ids:
                    return False, f"任务 {task.id} 依赖的 {dep} 不存在"
        
        # 检查所有需要的工具都存在
        for task in plan.tasks:
            if task.tool and task.tool not in self.tools:
                return False, f"工具 {task.tool} 不存在"
        
        return True, "计划有效"
`

## 3. 动态重新规划

`python
class AdaptivePlanner:
    \"\"\"自适应规划器 - 可以在执行中重新规划\"\"\"
    
    def __init__(self, planner: HierarchicalPlanner):
        self.planner = planner
        self.plan_history: List[Plan] = []
    
    def replan_on_failure(self, plan: Plan, failed_task: Task, error: str) -> Plan:
        \"\"\"任务失败时重新规划\"\"\"
        print(f"🔄 重新规划: {failed_task.description} 失败")
        print(f"   错误: {error}")
        
        # 策略1: 用替代工具重试
        alternative = self._find_alternative_tool(failed_task.tool)
        if alternative:
            failed_task.tool = alternative
            failed_task.status = TaskStatus.PENDING
            return plan
        
        # 策略2: 跳过该任务
        failed_task.status = TaskStatus.FAILED
        failed_task.result = f"跳过: {error}"
        
        # 策略3: 重新分解目标
        remaining = [
            t for t in plan.tasks
            if t.status == TaskStatus.PENDING
        ]
        
        # 只重新规划剩余部分
        return plan
    
    def _find_alternative_tool(self, tool_name: str) -> str:
        \"\"\"查找替代工具\"\"\"
        alternatives = {
            "web_search": "local_search",
            "api_call": "manual_lookup",
        }
        return alternatives.get(tool_name, "")
`

## 4. 计划执行器

`python
class PlanExecutor:
    \"\"\"计划执行器\"\"\"
    
    def __init__(self, tools: dict, planner: HierarchicalPlanner):
        self.tools = tools
        self.planner = planner
        self.results: Dict[str, Any] = {}
    
    def execute(self, plan: Plan) -> str:
        \"\"\"执行计划\"\"\"
        max_iterations = len(plan.tasks) * 2  # 防止死循环
        
        for _ in range(max_iterations):
            ready = plan.get_ready_tasks()
            
            if not ready:
                if plan.is_complete():
                    return self._synthesize(plan)
                # 可能有循环依赖或卡住的任务
                blocked = [t for t in plan.tasks if t.status == TaskStatus.PENDING]
                if blocked:
                    return f"计划卡住: {len(blocked)} 个任务无法执行"
                break
            
            for task in ready:
                self._execute_task(task, plan)
        
        return self._synthesize(plan)
    
    def _execute_task(self, task: Task, plan: Plan):
        \"\"\"执行单个任务\"\"\"
        task.status = TaskStatus.RUNNING
        print(f"▶ 执行: {task.description}")
        
        tool = self.tools.get(task.tool)
        if not tool:
            task.status = TaskStatus.FAILED
            task.result = f"工具不存在: {task.tool}"
            return
        
        # 替换依赖引用
        params = dict(task.params)
        for key, value in params.items():
            if isinstance(value, str) and value.startswith("$"):
                ref = value[1:]
                params[key] = self.results.get(ref, value)
        
        result = tool.run(**params)
        
        if result.success:
            task.status = TaskStatus.COMPLETED
            task.result = str(result.data)
            self.results[task.id] = result.data
            print(f"  ✅ 完成: {task.result[:100]}")
        else:
            task.status = TaskStatus.FAILED
            task.result = result.error
            print(f"  ❌ 失败: {result.error}")
            
            # 触发重新规划
            self.planner.replan_on_failure(plan, task, result.error)
    
    def _synthesize(self, plan: Plan) -> str:
        \"\"\"汇总结果\"\"\"
        output = f"计划完成: {plan.goal}\n"
        for task in plan.tasks:
            status = "✅" if task.status == TaskStatus.COMPLETED else "❌"
            output += f"  {status} {task.description}: {task.result}\n"
        return output
`

## 5. 常见错误

1. **过度分解**：把简单任务拆得太细 → 设定分解粒度下限
2. **依赖错乱**：循环依赖或遗漏依赖 → 拓扑排序验证
3. **不重新规划**：失败后硬扛 → 添加动态重规划
4. **没有优先级**：所有任务平级执行 → 添加优先级字段

## 6. 动手练习

### 练习 1：实现 Task 和 Plan 数据类
### 练习 2：实现 HierarchicalPlanner
### 练习 3：实现 PlanExecutor 的循环逻辑
