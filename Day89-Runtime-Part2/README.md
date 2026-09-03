# Day 89: Agent 项目 - AI Assistant Runtime②

## 🎯 学习目标

- 集成Memory系统
- 实现Planning能力
- 添加Self-Correction
- 实现Context Engineering

## 📋 前置知识

- Day 88: Agent Runtime核心
- Memory系统
- Planning系统

## ⏰ 预计时间：2小时

---

今天继续完善Runtime，添加记忆、规划和自我纠正能力。

## 🔑 核心任务

### 1. Memory系统集成

`python
# 在Agent中添加Memory
class Agent:
    def __init__(self):
        self.short_term_memory = ShortTermMemory()
        self.long_term_memory = LongTermMemory()
    
    async def run(self, query: str) -> str:
        # 检索相关记忆
        relevant_memories = self.long_term_memory.search(query)
        
        # 构建包含记忆的上下文
        context = self._build_context_with_memory(query, relevant_memories)
        
        # 执行Agent循环
        result = await self._agent_loop(context)
        
        # 存储重要信息
        self._store_to_memory(query, result)
        
        return result
`

### 2. Planning能力

`python
class PlanningAgent(Agent):
    def __init__(self):
        super().__init__()
        self.planner = TaskPlanner()
    
    async def run(self, query: str) -> str:
        # 创建计划
        plan = self.planner.create_plan(query)
        
        # 执行计划
        results = []
        for step in plan.steps:
            result = await self._execute_step(step)
            results.append(result)
            
            # 检查是否需要调整
            if self._should_replan(step, result):
                plan = self.planner.replan(query, step, plan)
        
        return self._synthesize_results(results)
`

### 3. Self-Correction

`python
class SelfCorrectingAgent(Agent):
    def __init__(self):
        super().__init__()
        self.corrector = SelfCorrector()
    
    async def _execute_with_correction(self, task: str) -> str:
        max_attempts = 3
        
        for attempt in range(max_attempts):
            try:
                result = await self._execute(task)
                
                # 检查结果
                if self._is_successful(result):
                    return result
                
                # 生成纠正方案
                correction = self.corrector.correct(
                    error=None,
                    context={"task": task, "result": result}
                )
                
                # 应用纠正
                task = self._apply_correction(task, correction)
            
            except Exception as e:
                if attempt == max_attempts - 1:
                    raise
        
        return "任务执行失败"
`

### 4. Context Engineering

`python
class ContextualAgent(Agent):
    def __init__(self):
        super().__init__()
        self.context_manager = ContextManager()
        self.context_budget = ContextBudget(total_budget=4096)
    
    async def _build_context(self, query: str) -> str:
        # 获取记忆
        memory = self._get_relevant_memory(query)
        
        # 获取工具描述
        tools = self._get_tools_description()
        
        # 构建上下文
        context = self.context_manager.build_context(
            system_prompt=self.config.system_prompt,
            memory=memory,
            history=self.memory[-5:],  # 最近5轮对话
            current_input=query
        )
        
        return context
`

## 📋 完整的集成代码

`python
# src/runtime.py
from .agent import Agent, AgentConfig
from .memory import ShortTermMemory, LongTermMemory
from .planning import TaskPlanner
from .context import ContextManager


class AIRuntime:
    '''AI Assistant Runtime'''
    
    def __init__(self, config: AgentConfig = None):
        self.agent = Agent(config or AgentConfig())
        self.memory = LongTermMemory()
        self.planner = TaskPlanner()
        self.context_manager = ContextManager()
    
    async def initialize(self):
        '''初始化Runtime'''
        # 注册默认工具
        self._register_default_tools()
        
        # 加载记忆
        await self._load_memory()
    
    def _register_default_tools(self):
        '''注册默认工具'''
        # 工具将在后面实现
        pass
    
    async def _load_memory(self):
        '''加载记忆'''
        # 从持久化存储加载
        pass
    
    async def run(self, query: str) -> str:
        '''运行'''
        # 1. 检索相关记忆
        memories = self.memory.retrieve(query)
        
        # 2. 创建计划（如果需要）
        if self._need_planning(query):
            plan = self.planner.create_plan(query)
            return await self._execute_plan(plan)
        
        # 3. 直接回答
        return await self.agent.run(query)
    
    def _need_planning(self, query: str) -> bool:
        '''是否需要规划'''
        # 简单的启发式检查
        complex_keywords = ["完成", "实现", "构建", "设计", "分析"]
        return any(kw in query for kw in complex_keywords)
    
    async def _execute_plan(self, plan) -> str:
        '''执行计划'''
        results = []
        for step in plan.steps:
            result = await self._execute_step(step)
            results.append(result)
        
        return "\n".join(results)
    
    async def _execute_step(self, step) -> str:
        '''执行步骤'''
        return await self.agent.run(step.description)
`

---

> 📖 详细课程内容见 [lesson.md](./lesson.md)  
> 💪 挑战任务见 [challenge.md](./challenge.md)
