# Day 78 示例 5: 工具链组合
from dataclasses import dataclass
from typing import Any

@dataclass
class ToolResult:
    success: bool
    data: Any = None
    error: str = ""

class ToolChain:
    \"\"\"串联多个工具执行\"\"\"
    def __init__(self, tools: dict):
        self.tools = tools
    
    def execute(self, steps: list) -> ToolResult:
        context = {}
        for i, step in enumerate(steps):
            name = step["tool"]
            params = dict(step.get("params", {}))
            for k, v in params.items():
                if isinstance(v, str) and v.startswith("$"):
                    params[k] = context.get(v[1:], v)
            tool = self.tools.get(name)
            if not tool:
                return ToolResult(False, error=f"未知工具: {name}")
            result = tool.run(**params)
            if not result.success:
                return ToolResult(False, error=f"步骤{i+1}失败: {result.error}")
            context[f"step{i+1}"] = result.data
            context["last"] = result.data
        return ToolResult(True, data=context)

# 演示
if __name__ == "__main__":
    class Step1Tool:
        name = "step1"
        def run(self, **kw): return ToolResult(True, data=f"处理: {kw.get('input','')}")
    class Step2Tool:
        name = "step2"
        def run(self, **kw): return ToolResult(True, data=f"分析: {kw.get('data','')}")
    
    chain = ToolChain({"step1": Step1Tool(), "step2": Step2Tool()})
    result = chain.execute([
        {"tool": "step1", "params": {"input": "原始数据"}},
        {"tool": "step2", "params": {"data": ""}},
    ])
    print(result)
