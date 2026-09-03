# Day 79 课程：Planning & Goal Decomposition

## 1. 目标分解策略

### 分解方法

`python
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class StepStatus(Enum):
    '''步骤状态'''
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class TaskStep:
    '''任务步骤'''
    id: str
    description: str
    tool_name: str | None = None
    tool_input: dict | None = None
    dependencies: list[str] = None
    status: StepStatus = StepStatus.PENDING
    result: any = None
    error: str | None = None
    
    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []


@dataclass
class Plan:
    '''计划'''
    goal: str
    steps: list[TaskStep]
    current_step: int = 0
    is_complete: bool = False
    
    def get_next_step(self) -> TaskStep | None:
        '''获取下一个待执行的步骤'''
        for step in self.steps:
            if step.status == StepStatus.PENDING:
                # 检查依赖是否满足
                deps_met = all(
                    self._get_step_by_id(dep).status == StepStatus.COMPLETED
                    for dep in step.dependencies
                    if self._get_step_by_id(dep)
                )
                if deps_met:
                    return step
        return None
    
    def _get_step_by_id(self, step_id: str) -> TaskStep | None:
        '''根据ID获取步骤'''
        for step in self.steps:
            if step.id == step_id:
                return step
        return None


class GoalDecomposer:
    '''目标分解器'''
    
    def __init__(self, llm_provider=None):
        self.llm_provider = llm_provider
    
    def decompose(self, goal: str, available_tools: list[str]) -> Plan:
        '''将目标分解为计划'''
        # 使用LLM分解目标
        prompt = self._build_decomposition_prompt(goal, available_tools)
        
        # 这里应该调用LLM，简化处理
        steps = self._decompose_with_llm(goal, available_tools)
        
        return Plan(goal=goal, steps=steps)
    
    def _decompose_with_llm(
        self, 
        goal: str, 
        available_tools: list[str]
    ) -> list[TaskStep]:
        '''使用LLM分解目标（模拟）'''
        # 实际实现中，这里应该调用LLM
        # 这里返回模拟的分解结果
        
        if "搜索" in goal or "查找" in goal:
            return [
                TaskStep(
                    id="step1",
                    description="分析搜索需求",
                    tool_name=None
                ),
                TaskStep(
                    id="step2",
                    description="执行搜索",
                    tool_name="web_search",
                    tool_input={"query": goal},
                    dependencies=["step1"]
                ),
                TaskStep(
                    id="step3",
                    description="整理结果",
                    tool_name=None,
                    dependencies=["step2"]
                )
            ]
        else:
            return [
                TaskStep(
                    id="step1",
                    description=f"执行任务: {goal}",
                    tool_name=None
                )
            ]
`

## 2. 任务规划器设计

`python
class TaskPlanner:
    '''任务规划器'''
    
    def __init__(self, llm_provider=None):
        self.llm_provider = llm_provider
        self.decomposer = GoalDecomposer(llm_provider)
    
    def create_plan(
        self, 
        goal: str, 
        context: dict = None,
        available_tools: list[str] = None
    ) -> Plan:
        '''创建计划'''
        # 分析上下文
        if context is None:
            context = {}
        
        # 分解目标
        plan = self.decomposer.decompose(goal, available_tools or [])
        
        # 优化计划
        plan = self._optimize_plan(plan)
        
        return plan
    
    def replan(
        self, 
        goal: str, 
        failed_step: TaskStep,
        current_plan: Plan
    ) -> Plan:
        '''重新规划'''
        # 分析失败原因
        failure_analysis = self._analyze_failure(failed_step)
        
        # 创建新计划
        new_steps = self._create_remediation_steps(
            goal, failed_step, failure_analysis
        )
        
        # 合并到现有计划
        return self._merge_plans(current_plan, new_steps)
    
    def _optimize_plan(self, plan: Plan) -> Plan:
        '''优化计划（并行化等）'''
        # 检查哪些步骤可以并行执行
        # 这里简化处理，返回原计划
        return plan
    
    def _analyze_failure(self, step: TaskStep) -> dict:
        '''分析失败原因'''
        return {
            "step_id": step.id,
            "error": step.error,
            "suggestion": "尝试使用不同的方法"
        }
    
    def _create_remediation_steps(
        self,
        goal: str,
        failed_step: TaskStep,
        analysis: dict
    ) -> list[TaskStep]:
        '''创建修复步骤'''
        return [
            TaskStep(
                id=f"remedy_{failed_step.id}",
                description=f"修复: {analysis['suggestion']}",
                tool_name=failed_step.tool_name,
                tool_input=failed_step.tool_input
            )
        ]
    
    def _merge_plans(
        self, 
        original: Plan, 
        new_steps: list[TaskStep]
    ) -> Plan:
        '''合并计划'''
        # 在失败步骤后插入新步骤
        merged_steps = []
        for step in original.steps:
            merged_steps.append(step)
            if step.id == new_steps[0].id.replace("remedy_", ""):
                merged_steps.extend(new_steps)
        
        return Plan(goal=original.goal, steps=merged_steps)
`

## 3. 计划验证与调整

`python
class PlanValidator:
    '''计划验证器'''
    
    def validate(self, plan: Plan) -> tuple[bool, list[str]]:
        '''验证计划'''
        errors = []
        
        # 检查步骤依赖
        for step in plan.steps:
            for dep_id in step.dependencies:
                if not self._step_exists(plan, dep_id):
                    errors.append(f"步骤 {step.id} 的依赖 {dep_id} 不存在")
                elif self._is_self_dep(step, dep_id):
                    errors.append(f"步骤 {step.id} 不能依赖自己")
        
        # 检查循环依赖
        if self._has_cycle(plan):
            errors.append("计划中存在循环依赖")
        
        # 检查步骤完整性
        if not plan.steps:
            errors.append("计划为空")
        
        return len(errors) == 0, errors
    
    def _step_exists(self, plan: Plan, step_id: str) -> bool:
        '''检查步骤是否存在'''
        return any(s.id == step_id for s in plan.steps)
    
    def _is_self_dep(self, step: TaskStep, dep_id: str) -> bool:
        '''检查是否自我依赖'''
        return step.id == dep_id
    
    def _has_cycle(self, plan: Plan) -> bool:
        '''检查是否存在循环依赖'''
        visited = set()
        rec_stack = set()
        
        def dfs(step_id: str) -> bool:
            visited.add(step_id)
            rec_stack.add(step_id)
            
            step = self._get_step(plan, step_id)
            if step:
                for dep in step.dependencies:
                    if dep not in visited:
                        if dfs(dep):
                            return True
                    elif dep in rec_stack:
                        return True
            
            rec_stack.remove(step_id)
            return False
        
        for step in plan.steps:
            if step.id not in visited:
                if dfs(step.id):
                    return True
        
        return False
    
    def _get_step(self, plan: Plan, step_id: str) -> TaskStep | None:
        '''获取步骤'''
        for step in plan.steps:
            if step.id == step_id:
                return step
        return None
`

## 4. 层次化规划（HLP）

`python
class HierarchicalPlanner:
    '''层次化规划器'''
    
    def __init__(self, llm_provider=None):
        self.llm_provider = llm_provider
    
    def create_hierarchical_plan(self, goal: str) -> dict:
        '''创建层次化计划'''
        # 第一层：战略目标
        strategic = self._create_strategic_plan(goal)
        
        # 第二层：战术分解
        tactical = {}
        for objective in strategic["objectives"]:
            tactical[objective] = self._create_tactical_plan(objective)
        
        # 第三层：操作步骤
        operational = {}
        for objective, tasks in tactical.items():
            operational[objective] = {}
            for task in tasks:
                operational[objective][task] = self._create_operational_plan(task)
        
        return {
            "strategic": strategic,
            "tactical": tactical,
            "operational": operational
        }
    
    def _create_strategic_plan(self, goal: str) -> dict:
        '''创建战略计划'''
        return {
            "goal": goal,
            "objectives": [
                f"目标1: 分析{goal}的需求",
                f"目标2: 执行{goal}的核心任务",
                f"目标3: 验证{goal}的结果"
            ],
            "timeline": "short-term"
        }
    
    def _create_tactical_plan(self, objective: str) -> list[str]:
        '''创建战术计划'''
        return [
            f"任务1: 准备{objective}",
            f"任务2: 执行{objective}",
            f"任务3: 评估{objective}"
        ]
    
    def _create_operational_plan(self, task: str) -> list[dict]:
        '''创建操作计划'''
        return [
            {"action": f"步骤1: {task}", "tool": None},
            {"action": f"步骤2: {task}", "tool": None},
            {"action": f"步骤3: {task}", "tool": None}
        ]
`

## 5. 本日总结

- 目标分解是Agent规划的基础
- TaskPlanner实现了任务的创建和调整
- PlanValidator确保计划的正确性
- 层次化规划支持复杂目标的分解

明天我们将学习Self-Correction和反思机制。
