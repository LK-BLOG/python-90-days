# Day 76 课程：Agent 架构概述

## 1. 什么是Agent？

Agent（智能体）是一个能够**自主感知环境、做出决策并执行行动**的系统。
它不是简单的函数调用，而是一个完整的**循环系统**。

### Agent的核心组件

`
┌─────────────────────────────────────────────┐
│                  Agent                       │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐     │
│  │Perception│  │Reasoning│  │  Action  │     │
│  │  感知层  │  │  思考层  │  │  执行层  │     │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘    │
│       │              │              │         │
│       └──────────────┼──────────────┘         │
│                      │                        │
│               ┌──────┴──────┐                 │
│               │   Memory    │                 │
│               │   记忆系统   │                 │
│               └─────────────┘                 │
└─────────────────────────────────────────────┘
`

## 2. Agent架构模式

### ReAct (Reasoning + Acting)

ReAct是最流行的Agent模式，让LLM交替进行推理和行动：

`python
# ReAct模式示例
class ReActAgent:
    def __init__(self, llm, tools):
        self.llm = llm
        self.tools = tools
        self.trajectory = []
    
    def run(self, query: str, max_steps: int = 10) -> str:
        """执行ReAct循环"""
        context = self._build_initial_context(query)
        
        for step in range(max_steps):
            # 思考：LLM决定下一步行动
            thought = self._think(context)
            self.trajectory.append({"thought": thought})
            
            # 检查是否需要行动
            if thought.get("action_needed"):
                # 行动：选择并执行工具
                tool_name = thought["tool"]
                tool_input = thought["input"]
                observation = self._act(tool_name, tool_input)
                self.trajectory.append({
                    "action": tool_name,
                    "observation": observation
                })
                
                # 更新上下文
                context += f"\nAction: {tool_name}({tool_input})\nObservation: {observation}"
            else:
                # 最终回答
                return thought["answer"]
        
        return "达到最大步数限制"
    
    def _think(self, context: str) -> dict:
        """让LLM决定下一步"""
        prompt = self._build_reasoning_prompt(context)
        response = self.llm.generate(prompt)
        return self._parse_response(response)
    
    def _act(self, tool_name: str, tool_input: str) -> str:
        """执行工具调用"""
        tool = self.tools.get(tool_name)
        if not tool:
            return f"错误：工具 {tool_name} 不存在"
        return tool.execute(tool_input)
`

### Plan-and-Execute模式

先制定计划，再逐步执行：

`python
class PlanAndExecuteAgent:
    def __init__(self, llm, tools):
        self.llm = llm
        self.tools = tools
        self.plan = []
        self.results = []
    
    def run(self, goal: str) -> str:
        """先规划后执行"""
        # 第一步：制定计划
        self.plan = self._create_plan(goal)
        print(f"计划：{self.plan}")
        
        # 第二步：逐步执行
        for i, step in enumerate(self.plan):
            print(f"执行步骤 {i+1}: {step['description']}")
            
            # 执行当前步骤
            result = self._execute_step(step, self.results)
            self.results.append({
                "step": step,
                "result": result
            })
            
            # 检查是否需要调整计划
            if self._should_replan():
                self.plan = self._replan(goal, self.results)
        
        # 第三步：综合结果
        return self._synthesize_results(goal, self.results)
    
    def _create_plan(self, goal: str) -> list:
        """使用LLM创建计划"""
        prompt = f\"\"\"
        目标：{goal}
        
        请制定一个详细的执行计划，包含具体的步骤。
        每个步骤应该是一个JSON对象，包含：
        - description: 步骤描述
        - tool: 使用的工具名称
        - input: 工具输入
        \"\"\"
        response = self.llm.generate(prompt)
        return self._parse_plan(response)
`

### Autonomous Agent模式

完全自主的Agent，能够自己设定目标并执行：

`python
class AutonomousAgent:
    def __init__(self, llm, tools, memory):
        self.llm = llm
        self.tools = tools
        self.memory = memory
        self.goals = []
        self.is_running = False
    
    def start(self, initial_goal: str = None):
        """启动自主Agent"""
        self.is_running = True
        
        if initial_goal:
            self.goals.append(initial_goal)
        
        while self.is_running:
            # 感知环境
            perception = self._perceive()
            
            # 思考下一步
            thought = self._reason(perception)
            
            # 执行行动
            if thought["action_type"] == "tool_use":
                result = self._use_tool(thought["tool"], thought["input"])
            elif thought["action_type"] == "set_goal":
                self.goals.append(thought["goal"])
                result = f"设定新目标: {thought['goal']}"
            elif thought["action_type"] == "reflect":
                result = self._reflect()
            else:
                result = "无行动"
            
            # 更新记忆
            self.memory.store({
                "perception": perception,
                "thought": thought,
                "result": result
            })
            
            # 检查是否完成所有目标
            if self._all_goals_achieved():
                self.is_running = False
    
    def _reflect(self) -> str:
        """自我反思"""
        recent_memory = self.memory.get_recent(5)
        prompt = f\"\"\"
        最近的经历：
        {recent_memory}
        
        请反思：
        1. 我做得好的地方
        2. 需要改进的地方
        3. 下一步应该关注什么
        \"\"\"
        return self.llm.generate(prompt)
`

## 3. Agent vs Chatbot vs Copilot

| 维度 | Chatbot | Copilot | Agent |
|------|---------|---------|-------|
| **主动性** | 被动响应 | 半主动建议 | 完全主动 |
| **工具使用** | 无 | 建议使用 | 自主执行 |
| **记忆** | 无/会话内 | 短期 | 多层记忆 |
| **目标导向** | 无 | 弱 | 强 |
| **迭代能力** | 单轮 | 有限 | 无限循环 |
| **错误处理** | 无 | 人工干预 | 自我纠正 |

## 4. 主流Agent框架对比

### LangChain Agent

`python
from langchain.agents import initialize_agent, Tool
from langchain.llms import OpenAI

# 定义工具
tools = [
    Tool(
        name="Search",
        func=search_function,
        description="搜索互联网获取信息"
    ),
    Tool(
        name="Calculator",
        func=calculator_function,
        description="执行数学计算"
    )
]

# 初始化Agent
llm = OpenAI(temperature=0)
agent = initialize_agent(
    tools, llm, agent="zero-shot-react", verbose=True
)

# 运行
result = agent.run("今天北京天气怎么样？")
`

### LlamaIndex Agent

`python
from llama_index.agent import OpenAIAgent
from llama_index.tools import FunctionTool

# 定义工具
search_tool = FunctionTool.from_defaults(
    fn=search_function,
    name="Search",
    description="搜索互联网获取信息"
)

# 创建Agent
agent = OpenAIAgent.from_tools(
    tools=[search_tool],
    llm=llm,
    verbose=True
)

# 运行
response = agent.chat("今天北京天气怎么样？")
`

### CrewAI

`python
from crewai import Agent, Task, Crew

# 定义Agent
researcher = Agent(
    role="研究员",
    goal="收集和分析信息",
    backstory="你是一个专业的研究员...",
    tools=[search_tool],
    llm=llm
)

writer = Agent(
    role="作者",
    goal="撰写高质量的文章",
    backstory="你是一个专业的作家...",
    llm=llm
)

# 定义任务
research_task = Task(
    description="研究今天的热点新闻",
    agent=researcher
)

write_task = Task(
    description="根据研究结果写一篇文章",
    agent=writer
)

# 创建团队
crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, write_task]
)

# 执行
result = crew.kickoff()
`

### AutoGen

`python
from autogen import AssistantAgent, UserProxyAgent

# 创建Agent
assistant = AssistantAgent(
    name="assistant",
    llm_config={"model": "gpt-4"}
)

user_proxy = UserProxyAgent(
    name="user_proxy",
    human_input_mode="TERMINATE",
    code_execution_config={"work_dir": "coding"}
)

# 开始对话
user_proxy.initiate_chat(
    assistant,
    message="今天北京天气怎么样？"
)
`

## 5. 选择Agent框架的考量

| 因素 | LangChain | LlamaIndex | CrewAI | AutoGen |
|------|-----------|------------|--------|---------|
| **易用性** | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **灵活性** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **多Agent** | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **工具生态** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| **文档质量** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |

## 6. Agent设计原则

### 6.1 最小权限原则

Agent应该只拥有完成任务所需的最小权限：

`python
class SecureAgent:
    def __init__(self, allowed_tools: list[str]):
        self.allowed_tools = set(allowed_tools)
    
    def use_tool(self, tool_name: str, **kwargs):
        if tool_name not in self.allowed_tools:
            raise PermissionError(f"Agent没有权限使用工具: {tool_name}")
        # 执行工具
`

### 6.2 透明性原则

Agent的决策过程应该是可解释的：

`python
class TransparentAgent:
    def think(self, context):
        thought = self.llm.generate(context)
        # 记录思考过程
        self.log(f"思考: {thought}")
        return thought
    
    def act(self, action):
        self.log(f"行动: {action}")
        result = self.execute(action)
        self.log(f"结果: {result}")
        return result
`

### 6.3 安全性原则

Agent应该有安全护栏防止危险行为：

`python
class SafeAgent:
    DANGEROUS_ACTIONS = [
        "delete_all_files",
        "drop_database",
        "transfer_money"
    ]
    
    def execute_action(self, action):
        if action in self.DANGEROUS_ACTIONS:
            return self.request_human_approval(action)
        return self.perform_action(action)
`

## 7. 本日总结

- Agent是一个完整的感知-思考-行动循环系统
- ReAct是最流行的Agent架构模式
- Agent ≠ Chatbot ≠ Copilot，它们有本质区别
- 选择框架时要考虑易用性、灵活性、多Agent支持等因素
- 设计Agent时要遵循最小权限、透明性、安全性原则

明天我们将深入Agent的工具系统，学习如何设计和实现工具注册与调度系统。
