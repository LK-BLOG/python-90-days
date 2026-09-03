# Day 76 示例 1: 基础 ReAct 循环
\"\"\"
最小化的 ReAct Agent 实现
演示 Reasoning + Acting 交替循环
\"\"\"
import re
from typing import Callable, Any


class Tool:
    \"\"\"工具基类\"\"\"
    def __init__(self, name: str, description: str, func: Callable):
        self.name = name
        self.description = description
        self.func = func
    
    def execute(self, **kwargs) -> str:
        try:
            return str(self.func(**kwargs))
        except Exception as e:
            return f"错误: {e}"


class SimpleReActAgent:
    \"\"\"简单 ReAct Agent\"\"\"
    
    def __init__(self, tools: list[Tool]):
        self.tools = {t.name: t for t in tools}
        self.trace = []
        self.max_steps = 10
    
    def _build_tool_descriptions(self) -> str:
        \"\"\"构建工具描述\"\"\"
        return "\n".join([
            f"  {t.name}: {t.description}"
            for t in self.tools.values()
        ])
    
    def _simulate_llm_thought(self, query: str, history: list) -> str:
        \"\"\"模拟 LLM 推理（实际项目中调用真实 LLM）\"\"\"
        if not history:
            return f'Thought: 我需要分析问题 "{query}"'
        last = history[-1]
        if "错误" in last.get("observation", ""):
            return "Thought: 上次执行失败，换个方法"
        return "Thought: 已获得足够信息，可以回答了"
    
    def _simulate_llm_action(self, query: str, history: list) -> str:
        \"\"\"模拟 LLM 生成 Action\"\"\"
        if not history:
            if "距离" in query or "多少" in query:
                return 'Action: calculator(distance=1318)'
            return 'Action: search("{}", query=query)'.format(query)
        if len(history) >= 1:
            return f'Action: finish(answer="根据查询结果...")'
        return 'Action: finish(answer="无法回答")'
    
    def _parse_action(self, action_str: str) -> dict:
        \"\"\"解析 Action 字符串\"\"\"
        match = re.match(r'Action:\s*(\w+)\((.*)\)', action_str.strip())
        if not match:
            return {"type": "unknown", "raw": action_str}
        
        tool_name = match.group(1)
        args_str = match.group(2)
        
        # 简单参数解析
        params = {}
        if args_str:
            for pair in args_str.split(","):
                if "=" in pair:
                    k, v = pair.split("=", 1)
                    params[k.strip()] = v.strip().strip('"\'')
        
        if tool_name == "finish":
            return {"type": "finish", "output": params.get("answer", "")}
        return {"type": "tool", "tool": tool_name, "params": params}
    
    def run(self, query: str) -> str:
        \"\"\"执行 ReAct 循环\"\"\"
        print(f"=== ReAct Agent 开始 ===")
        print(f"查询: {query}\n")
        
        history = []
        
        for step in range(self.max_steps):
            print(f"--- Step {step + 1} ---")
            
            # 思考
            thought = self._simulate_llm_thought(query, history)
            print(thought)
            
            # 行动
            action_str = self._simulate_llm_action(query, history)
            print(action_str)
            
            # 解析行动
            action = self._parse_action(action_str)
            
            # 如果是最终答案
            if action["type"] == "finish":
                answer = action["output"]
                print(f"\n=== 最终答案 ===")
                print(answer)
                self.trace.append({
                    "step": step + 1,
                    "thought": thought,
                    "action": action_str,
                    "observation": "FINISH"
                })
                return answer
            
            # 执行工具
            if action["type"] == "tool":
                tool_name = action["tool"]
                if tool_name in self.tools:
                    observation = self.tools[tool_name].execute(**action["params"])
                else:
                    observation = f"错误: 未知工具 '{tool_name}'"
                
                print(f"Observation: {observation}")
                history.append({
                    "thought": thought,
                    "action": action_str,
                    "observation": observation
                })
                self.trace.append({
                    "step": step + 1,
                    "thought": thought,
                    "action": action_str,
                    "observation": observation
                })
        
        return "达到最大步数限制"


# 演示
if __name__ == "__main__":
    # 定义工具
    tools = [
        Tool(
            name="calculator",
            description="执行数学计算，参数: expression (数学表达式)",
            func=lambda expression="": str(eval(expression))  # 仅演示用
        ),
        Tool(
            name="search",
            description="搜索信息，参数: query (搜索关键词)",
            func=lambda query="": f"搜索结果: 关于 '{query}' 的信息..."
        ),
        Tool(
            name="lookup",
            description="查找定义，参数: term (要查找的术语)",
            func=lambda term="": f"定义: {term} 是一种..."
        ),
    ]
    
    agent = SimpleReActAgent(tools)
    result = agent.run("北京到上海的距离，按350km/h需要多少小时？")
    print(f"\n追踪记录: {agent.trace}")
