# Day 76 示例 2: Plan-and-Execute 模式
\"\"\"
先制定计划，再逐步执行
\"\"\"
from dataclasses import dataclass, field
from typing import Any
from enum import Enum


class StepStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    DONE = "done"
    FAILED = "failed"


@dataclass
class PlanStep:
    \"\"\"计划步骤\"\"\"
    id: int
    description: str
    tool_name: str = ""
    params: dict = field(default_factory=dict)
    status: StepStatus = StepStatus.PENDING
    result: Any = None
    error: str = ""


class PlanAndExecuteAgent:
    \"\"\"Plan-and-Execute Agent\"\"\"
    
    def __init__(self, tools: dict):
        self.tools = tools
        self.plan: list[PlanStep] = []
        self.results: list[dict] = []
    
    def create_plan(self, goal: str) -> list[PlanStep]:
        \"\"\"创建执行计划（模拟 LLM 生成）\"\"\"
        print(f"\n📋 制定计划: {goal}")
        
        # 模拟 LLM 生成的计划
        if "报告" in goal:
            steps = [
                PlanStep(1, "搜索相关数据", "search", {"query": "市场数据 2024"}),
                PlanStep(2, "统计数据", "analyze", {"data": "step1_result"}),
                PlanStep(3, "生成报告", "generate_report", {"analysis": "step2_result"}),
            ]
        else:
            steps = [
                PlanStep(1, "分析问题", "analyze", {"query": goal}),
                PlanStep(2, "查找信息", "search", {"query": "step1_result"}),
                PlanStep(3, "生成答案", "answer", {"info": "step2_result"}),
            ]
        
        self.plan = steps
        for s in steps:
            print(f"  Step {s.id}: {s.description}")
        
        return steps
    
    def execute_step(self, step: PlanStep) -> Any:
        \"\"\"执行单个步骤\"\"\"
        step.status = StepStatus.RUNNING
        print(f"\n▶ 执行 Step {step.id}: {step.description}")
        
        try:
            tool = self.tools.get(step.tool_name)
            if not tool:
                raise ValueError(f"工具 '{step.tool_name}' 不存在")
            
            # 模拟执行（用已有结果替换参数引用）
            params = dict(step.params)
            for k, v in params.items():
                if isinstance(v, str) and v.startswith("step") and "_result" in v:
                    ref_step_id = int(v.replace("step", "").replace("_result", ""))
                    ref_result = self._get_step_result(ref_step_id)
                    params[k] = ref_result
            
            result = tool(params)
            step.result = result
            step.status = StepStatus.DONE
            
            self.results.append({
                "step_id": step.id,
                "description": step.description,
                "result": result
            })
            
            print(f"  ✅ 完成: {result}")
            return result
            
        except Exception as e:
            step.status = StepStatus.FAILED
            step.error = str(e)
            print(f"  ❌ 失败: {e}")
            return None
    
    def replan(self, goal: str, failed_step: PlanStep) -> list[PlanStep]:
        \"\"\"重新规划（跳过失败步骤，寻找替代方案）\"\"\"
        print(f"\n🔄 重新规划（Step {failed_step.id} 失败）")
        
        # 简单策略：用替代工具重试
        alternative_tools = {
            "search": "fallback_search",
            "analyze": "manual_analyze",
        }
        
        new_tool = alternative_tools.get(failed_step.tool_name, "search")
        failed_step.tool_name = new_tool
        failed_step.status = StepStatus.PENDING
        failed_step.error = ""
        
        print(f"  替换工具: {failed_step.tool_name} → {new_tool}")
        return self.plan
    
    def _get_step_result(self, step_id: int) -> str:
        for r in self.results:
            if r["step_id"] == step_id:
                return r["result"]
        return ""
    
    def run(self, goal: str) -> str:
        \"\"\"完整执行流程\"\"\"
        # 1. 制定计划
        self.create_plan(goal)
        
        # 2. 逐步执行
        for step in self.plan:
            result = self.execute_step(step)
            
            # 失败时重新规划
            if step.status == StepStatus.FAILED:
                self.replan(goal, step)
                result = self.execute_step(step)
        
        # 3. 汇总结果
        return self._synthesize(goal)
    
    def _synthesize(self, goal: str) -> str:
        \"\"\"汇总所有步骤结果\"\"\"
        print(f"\n📊 汇总结果:")
        output = f"目标: {goal}\n"
        for r in self.results:
            output += f"  Step {r['step_id']}: {r['result']}\n"
        return output


# 演示
if __name__ == "__main__":
    # 定义工具（模拟）
    tools = {
        "search": lambda params: f"搜索'{params['query']}'的结果: 找到10条记录",
        "analyze": lambda params: f"分析数据: {params} → 发现增长趋势 15%",
        "generate_report": lambda params: f"报告已生成: 包含 {params} 的分析",
        "fallback_search": lambda params: f"备用搜索: {params['query']} → 找到5条记录",
        "manual_analyze": lambda params: f"手动分析: {params} → 结论: 正常",
        "answer": lambda params: f"最终答案基于: {params['info']}",
    }
    
    agent = PlanAndExecuteAgent(tools)
    result = agent.run("生成2024年市场分析报告")
    print(result)
