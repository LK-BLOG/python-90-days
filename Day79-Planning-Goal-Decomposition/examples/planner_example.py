'''
Day 79 示例：任务规划器
'''

from dataclasses import dataclass
from enum import Enum
from typing import Optional, Callable


class StepStatus(Enum):
    '''步骤状态'''
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


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
    
    def get_next_step(self) -> TaskStep | None:
        '''获取下一个可执行步骤'''
        for step in self.steps:
            if step.status == StepStatus.PENDING:
                deps_met = all(
                    self._get_step(dep).status == StepStatus.COMPLETED
                    for dep in step.dependencies
                    if self._get_step(dep)
                )
                if deps_met:
                    return step
        return None
    
    def _get_step(self, step_id: str) -> TaskStep | None:
        for s in self.steps:
            if s.id == step_id:
                return s
        return None
    
    def display(self):
        '''显示计划'''
        print(f"\n目标: {self.goal}")
        print("-" * 40)
        for step in self.steps:
            status_icon = {
                StepStatus.PENDING: "⏳",
                StepStatus.IN_PROGRESS: "🔄",
                StepStatus.COMPLETED: "✅",
                StepStatus.FAILED: "❌"
            }.get(step.status, "❓")
            
            deps = f" (依赖: {', '.join(step.dependencies)})" if step.dependencies else ""
            print(f"{status_icon} {step.id}: {step.description}{deps}")
        
        print("-" * 40)


class GoalDecomposer:
    '''目标分解器'''
    
    def decompose(self, goal: str, tools: list[str]) -> list[TaskStep]:
        '''分解目标'''
        # 简化的分解逻辑
        steps = []
        
        # 步骤1：分析
        steps.append(TaskStep(
            id="step1",
            description=f"分析目标: {goal}"
        ))
        
        # 步骤2：执行
        tool = self._select_tool(goal, tools)
        steps.append(TaskStep(
            id="step2",
            description="执行核心任务",
            tool_name=tool,
            dependencies=["step1"]
        ))
        
        # 步骤3：验证
        steps.append(TaskStep(
            id="step3",
            description="验证结果",
            dependencies=["step2"]
        ))
        
        return steps
    
    def _select_tool(self, goal: str, tools: list[str]) -> str | None:
        '''选择合适的工具'''
        if "搜索" in goal or "查找" in goal:
            return "web_search" if "web_search" in tools else None
        elif "计算" in goal:
            return "calculator" if "calculator" in tools else None
        return None


class TaskPlanner:
    '''任务规划器'''
    
    def __init__(self):
        self.decomposer = GoalDecomposer()
    
    def create_plan(self, goal: str, tools: list[str] = None) -> Plan:
        '''创建计划'''
        if tools is None:
            tools = []
        
        steps = self.decomposer.decompose(goal, tools)
        return Plan(goal=goal, steps=steps)
    
    def replan(self, goal: str, failed_step: TaskStep, original_plan: Plan) -> Plan:
        '''重新规划'''
        # 分析失败
        print(f"分析失败步骤: {failed_step.id}")
        
        # 创建修复步骤
        fix_step = TaskStep(
            id=f"fix_{failed_step.id}",
            description=f"修复: {failed_step.description}",
            tool_name=failed_step.tool_name,
            dependencies=[failed_step.id]
        )
        
        # 合并计划
        new_steps = []
        for step in original_plan.steps:
            new_steps.append(step)
            if step.id == failed_step.id:
                new_steps.append(fix_step)
        
        # 添加最后的验证步骤
        new_steps.append(TaskStep(
            id="final_verify",
            description="最终验证",
            dependencies=[s.id for s in new_steps if s.status != StepStatus.COMPLETED]
        ))
        
        return Plan(goal=goal, steps=new_steps)


def main():
    '''演示任务规划'''
    print("=" * 60)
    print("任务规划器演示")
    print("=" * 60)
    
    planner = TaskPlanner()
    
    # 创建计划
    goal = "搜索Python最新版本信息并总结"
    plan = planner.create_plan(goal, ["web_search", "calculator"])
    
    print("\n初始计划:")
    plan.display()
    
    # 模拟执行
    print("\n执行过程:")
    
    step = plan.get_next_step()
    while step:
        print(f"\n执行: {step.id} - {step.description}")
        step.status = StepStatus.COMPLETED
        step.result = f"{step.description}的模拟结果"
        print(f"  完成: {step.result}")
        
        step = plan.get_next_step()
    
    print("\n最终计划:")
    plan.display()
    
    # 模拟失败和重新规划
    print("\n" + "=" * 60)
    print("模拟失败场景:")
    
    # 创建新计划
    plan2 = planner.create_plan("搜索Python最新版本", ["web_search"])
    plan2.steps[1].status = StepStatus.FAILED
    plan2.steps[1].error = "搜索超时"
    
    print("\n失败的计划:")
    plan2.display()
    
    # 重新规划
    new_plan = planner.replan(
        "搜索Python最新版本",
        plan2.steps[1],
        plan2
    )
    
    print("\n重新规划后的计划:")
    new_plan.display()
    
    print("\n" + "=" * 60)
    print("演示完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
