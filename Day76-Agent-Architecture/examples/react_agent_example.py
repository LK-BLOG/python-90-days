"""
Day 76 示例：ReAct Agent 实现
展示如何实现一个基础的ReAct Agent
"""

from abc import ABC, abstractmethod
from typing import Any, Callable
from dataclasses import dataclass, field
from datetime import datetime
import json


@dataclass
class AgentStep:
    """Agent执行步骤"""
    step_number: int
    thought: str
    action: str | None = None
    action_input: str | None = None
    observation: str | None = None
    timestamp: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> dict:
        return {
            "step_number": self.step_number,
            "thought": self.thought,
            "action": self.action,
            "action_input": self.action_input,
            "observation": self.observation,
            "timestamp": self.timestamp.isoformat()
        }


@dataclass
class AgentResult:
    """Agent执行结果"""
    query: str
    answer: str
    steps: list[AgentStep]
    total_steps: int
    success: bool
    error: str | None = None


class BaseTool(ABC):
    """工具基类"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    @abstractmethod
    def execute(self, input_data: str) -> str:
        """执行工具"""
        pass
    
    def to_dict(self) -> dict:
        """转换为字典（给LLM看的）"""
        return {
            "name": self.name,
            "description": self.description
        }


class SearchTool(BaseTool):
    """搜索工具（模拟）"""
    
    def __init__(self):
        super().__init__(
            name="search",
            description="搜索互联网获取信息。输入：搜索关键词"
        )
    
    def execute(self, input_data: str) -> str:
        # 模拟搜索结果
        return f"搜索 '{input_data}' 的结果：这是关于{input_data}的信息。"


class CalculatorTool(BaseTool):
    """计算器工具"""
    
    def __init__(self):
        super().__init__(
            name="calculator",
            description="执行数学计算。输入：数学表达式"
        )
    
    def execute(self, input_data: str) -> str:
        try:
            # 安全地计算数学表达式
            result = eval(input_data, {"__builtins__": {}}, {})
            return f"计算结果：{input_data} = {result}"
        except Exception as e:
            return f"计算错误：{str(e)}"


class ReActAgent:
    """ReAct Agent 实现"""
    
    def __init__(self, llm_provider: Callable = None):
        self.tools: dict[str, BaseTool] = {}
        self.steps: list[AgentStep] = []
        self.llm_provider = llm_provider or self._default_llm
    
    def register_tool(self, tool: BaseTool):
        """注册工具"""
        self.tools[tool.name] = tool
    
    def _default_llm(self, prompt: str) -> str:
        """默认LLM（模拟）"""
        # 实际使用时替换为真实的LLM调用
        return json.dumps({
            "thought": "我需要分析这个问题",
            "action": None,
            "action_input": None,
            "answer": "这是模拟的回答"
        })
    
    def _parse_llm_response(self, response: str) -> dict:
        """解析LLM响应"""
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {"thought": response, "action": None, "answer": response}
    
    def _build_prompt(self, query: str, context: str = "") -> str:
        """构建提示词"""
        tools_desc = "\n".join([
            f"- {t.name}: {t.description}" 
            for t in self.tools.values()
        ])
        
        return f\"\"\"
你是一个ReAct Agent。你需要通过思考和行动来回答问题。

可用工具：
{tools_desc}

历史轨迹：
{context}

当前问题：{query}

请以JSON格式返回你的思考和行动：
{{
    "thought": "你的思考过程",
    "action": "工具名称（如果需要行动）",
    "action_input": "工具输入（如果需要行动）",
    "answer": "最终答案（如果已经可以回答）"
}}
\"\"\"
    
    def run(self, query: str, max_steps: int = 10) -> AgentResult:
        """执行ReAct循环"""
        self.steps = []
        context = ""
        
        for step_num in range(1, max_steps + 1):
            # 构建提示词
            prompt = self._build_prompt(query, context)
            
            # 调用LLM
            response = self.llm_provider(prompt)
            parsed = self._parse_llm_response(response)
            
            # 创建步骤记录
            step = AgentStep(
                step_number=step_num,
                thought=parsed.get("thought", ""),
                action=parsed.get("action"),
                action_input=parsed.get("action_input"),
                observation=None
            )
            
            # 检查是否需要行动
            if step.action and step.action in self.tools:
                # 执行工具
                tool = self.tools[step.action]
                observation = tool.execute(step.action_input or "")
                step.observation = observation
                
                # 更新上下文
                context += f"\nThought: {step.thought}\nAction: {step.action}({step.action_input})\nObservation: {observation}"
            
            self.steps.append(step)
            
            # 检查是否得到最终答案
            if parsed.get("answer"):
                return AgentResult(
                    query=query,
                    answer=parsed["answer"],
                    steps=self.steps,
                    total_steps=step_num,
                    success=True
                )
        
        # 达到最大步数
        return AgentResult(
            query=query,
            answer="达到最大步数限制，无法完成任务",
            steps=self.steps,
            total_steps=max_steps,
            success=False,
            error="Max steps exceeded"
        )


def main():
    """演示ReAct Agent"""
    print("=" * 60)
    print("ReAct Agent 演示")
    print("=" * 60)
    
    # 创建Agent
    agent = ReActAgent()
    
    # 注册工具
    agent.register_tool(SearchTool())
    agent.register_tool(CalculatorTool())
    
    # 测试查询
    queries = [
        "什么是Python？",
        "计算 23 * 45 + 67",
        "搜索Python最新版本"
    ]
    
    for query in queries:
        print(f"\n{'='*60}")
        print(f"查询: {query}")
        print('='*60)
        
        result = agent.run(query)
        
        print(f"回答: {result.answer}")
        print(f"步数: {result.total_steps}")
        print(f"成功: {result.success}")
        
        # 打印详细步骤
        print("\n执行步骤:")
        for step in result.steps:
            print(f"  步骤 {step.step_number}: {step.thought}")
            if step.action:
                print(f"    行动: {step.action}({step.action_input})")
                print(f"    观察: {step.observation}")


if __name__ == "__main__":
    main()
