# Day 76: Agent 架构概述

## 🎯 学习目标

- 理解Agent的核心概念：感知→思考→行动循环
- 掌握主流Agent架构模式（ReAct/Plan-and-Execute/Autonomous）
- 区分Agent vs Chatbot vs Copilot的本质差异
- 对比主流Agent框架（LangChain/LlamaIndex/CrewAI/AutoGen）

## 📋 前置知识

- Day 60-75: LLM应用开发基础
- Python异步编程（asyncio）
- 面向对象设计

## ⏰ 预计时间：2小时

---

**Phase 4: Agent Engineering** — 你将从LLM使用者进化为Agent构建者。

Agent不是Prompt Engineering的简单延伸，而是一个**完整的自主系统**。
在这个阶段结束时，你将能独立设计和实现一个生产级AI Agent Runtime。

## 🔑 核心概念

### Agent ≠ Chatbot

| 特性 | Chatbot | Copilot | Agent |
|------|---------|---------|-------|
| 交互模式 | 问答 | 辅助 | 自主 |
| 工具使用 | 无 | 建议 | 执行 |
| 记忆 | 对话内 | 有限 | 多层 |
| 决策能力 | 无 | 有限 | 完全 |
| 迭代能力 | 无 | 手动 | 自动 |

### Perception-Reasoning-Action Loop

`python
while True:
    # 1. 感知（Perception）
    perception = agent.perceive(environment)
    
    # 2. 思考（Reasoning）
    thought = agent.reason(perception, memory, goals)
    
    # 3. 决策（Decision）
    action = agent.decide(thought, available_tools)
    
    # 4. 执行（Action）
    result = agent.act(action)
    
    # 5. 观察结果，更新记忆
    agent.update_memory(result)
    
    if agent.is_goal_achieved():
        break
`

---

> 📖 详细课程内容见 [lesson.md](./lesson.md)  
> 💪 挑战任务见 [challenge.md](./challenge.md)  
> 🏆 终极挑战见 [ultimate_challenge.md](./ultimate_challenge.md)
