# Day 76: Agent 架构概述

## 1. 什么是 Agent？

### 1.1 核心定义
Agent（智能体）是一个能够**自主感知环境、做出决策、执行行动**的系统。与传统程序不同，Agent 具有：

- **自主性**：无需人类逐步指令
- **反应性**：能感知环境变化并响应
- **主动性**：能主动采取行动达成目标
- **社交性**：能与其他 Agent 或人类交互

### 1.2 Agent 的核心循环：感知→思考→行动

`python
# Agent 核心循环伪代码
class Agent:
    def __init__(self, tools, llm):
        self.tools = tools
        self.llm = llm
        self.memory = []

    def run(self, goal: str) -> str:
        """Agent 主循环"""
        while not self.is_done(goal):
            # 1. 感知 - 收集当前环境信息
            perception = self.perceive()
            
            # 2. 思考 - LLM 推理决策
            thought = self.think(goal, perception)
            
            # 3. 行动 - 执行工具调用
            action_result = self.act(thought)
            
            # 4. 记录到记忆
            self.memory.append({
                "perception": perception,
                "thought": thought,
                "action": action_result
            })
        
        return self.get_final_answer(goal)
`

> 这个循环就是 Agent 的灵魂。所有框架、所有架构，拆到底都是这个循环的不同实现。

## 2. 两种主流 Agent 模式

### 2.1 ReAct（Reasoning + Acting）

ReAct 模式让 LLM 交替进行**推理**和**行动**：

`python
# ReAct 模式实现
class ReActAgent:
    def __init__(self, llm, tools):
        self.llm = llm
        self.tools = tools
        self.trace = []
    
    def run(self, query: str, max_steps: int = 10) -> str:
        """ReAct 主循环"""
        prompt = self._build_prompt(query)
        
        for step in range(max_steps):
            # LLM 生成 Thought + Action
            response = self.llm.generate(prompt)
            
            # 解析响应
            thought = self._extract_thought(response)
            action = self._extract_action(response)
            self.trace.append({"thought": thought, "action": action})
            
            # 如果是最终答案，结束
            if action.type == "finish":
                return action.output
            
            # 执行工具
            tool = self.tools[action.tool_name]
            observation = tool.execute(action.params)
            
            # 将观察结果加入 prompt，继续循环
            prompt += f"\nThought: {thought}"
            prompt += f"\nAction: {action}"
            prompt += f"\nObservation: {observation}"
        
        return "达到最大步数，未完成任务"
    
    def _build_prompt(self, query: str) -> str:
        tool_descriptions = "\n".join([
            f"- {t.name}: {t.description}" 
            for t in self.tools.values()
        ])
        return f"""你是一个智能助手，可以使用以下工具：
{tool_descriptions}

问题：{query}

请按以下格式思考和行动：
Thought: [你的思考过程]
Action: [工具名称](参数)
"""
`

### 2.2 Plan-and-Execute 模式

先制定完整计划，然后逐步执行：

`python
class PlanAndExecuteAgent:
    def __init__(self, planner_llm, executor_llm, tools):
        self.planner = planner_llm
        self.executor = executor_llm
        self.tools = tools
        self.plan = []
        self.results = []
    
    def run(self, goal: str) -> str:
        # 阶段1：制定计划
        self.plan = self._create_plan(goal)
        print(f"计划：{self.plan}")
        
        # 阶段2：逐步执行
        for i, step in enumerate(self.plan):
            print(f"执行步骤 {i+1}: {step}")
            
            # 可能需要根据已有结果重新规划
            result = self._execute_step(step, self.results)
            self.results.append(result)
            
            # 检查是否需要重新规划
            if self._need_replan(step, result):
                remaining = self.plan[i+1:]
                self.plan = self._replan(goal, remaining, self.results)
        
        return self._synthesize_results(goal, self.results)
    
    def _create_plan(self, goal: str) -> list:
        tool_desc = self._get_tool_descriptions()
        response = self.planner.generate(f"""
        目标：{goal}
        可用工具：{tool_desc}
        请制定一个分步骤的执行计划。每步应明确使用哪个工具。
        """)
        return self._parse_plan(response)
`

### 2.3 两种模式对比

| 特性 | ReAct | Plan-and-Execute |
|------|-------|------------------|
| 推理方式 | 边想边做 | 先想后做 |
| 灵活性 | 高，可随时调整 | 中，需显式重新规划 |
| 效率 | 较低（每步都推理） | 较高（批量推理） |
| 可预测性 | 低 | 高 |
| 适用场景 | 探索性任务 | 目标明确的任务 |
| 典型实现 | LangChain ReAct | LangGraph Plan-and-Execute |

## 3. Agent vs Chatbot vs Copilot

`python
# 三者的本质区别

# Chatbot：问答模式，一问一答
class Chatbot:
    def respond(self, user_message: str) -> str:
        return self.llm.generate(user_message)
    # 没有工具、没有循环、没有目标

# Copilot：辅助模式，建议+人类批准
class Copilot:
    def suggest(self, context: str) -> list:
        suggestions = self.llm.generate(f"基于上下文提供建议：{context}")
        return suggestions
    # 有工具但人类在环，辅助角色

# Agent：自主模式，独立完成任务
class Agent:
    def execute(self, goal: str) -> str:
        # 自主循环：感知→思考→行动
        # 独立使用工具
        # 直到完成目标
        pass
    # 完全自主，人类只设定目标
`

## 4. 主流 Agent 框架对比

| 框架 | 特点 | 适用场景 |
|------|------|---------|
| **LangChain/LangGraph** | 生态丰富，Graph支持 | 通用Agent开发 |
| **AutoGen** | 多Agent对话 | 多Agent协作 |
| **CrewAI** | 角色驱动 | 团队协作模拟 |
| **OpenAI Agents SDK** | 原生支持 | OpenAI生态 |
| **Anthropic Claude** | MCP协议 | 工具集成 |
| **PydanticAI** | 类型安全 | 生产级应用 |

## 5. Agent 的核心组件

`
┌─────────────────────────────────┐
│           Agent System           │
├─────────┬──────────┬────────────┤
│  Brain  │  Tools   │  Memory    │
│ (LLM)   │          │            │
│         │ - Search │ - Short    │
│ - 推理  │ - Code   │ - Long     │
│ - 规划  │ - File   │ - Working  │
│ - 反思  │ - DB     │            │
├─────────┴──────────┴────────────┤
│        Orchestration             │
│  (循环/状态机/工作流)             │
└─────────────────────────────────┘
`

## 6. 常见错误与陷阱

1. **无限循环**：Agent 在工具间反复调用，没有退出条件 → 设置 max_steps
2. **幻觉工具**：LLM 编造不存在的工具 → 严格校验工具名
3. **上下文溢出**：长对话超出窗口 → 定期压缩历史
4. **成本失控**：每次调用都消耗大量 token → 设置成本上限
5. **过度自主**：Agent 做了不该做的事 → 添加 Guardrails

## 7. 动手练习

### 练习 1：实现简单的 ReAct Agent
实现一个能使用 calculator 和 search 两个工具的 ReAct Agent。

### 练习 2：实现 Plan-and-Execute
先制定3步计划，然后逐步执行。

### 练习 3：框架对比
分别用伪代码写出三种框架实现同一个任务（查询天气+推荐餐厅）的方式。
