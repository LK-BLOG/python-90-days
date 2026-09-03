# Day 79: Planning & Goal Decomposition

## 🎯 学习目标

- 掌握目标分解策略
- 实现任务规划器（Planner）
- 学习计划验证与调整
- 理解层次化规划（HLP）

## 📋 前置知识

- Day 76-78: Agent架构和工具系统
- 图论基础（DAG）
- 问题分解方法

## ⏰ 预计时间：2小时

---

Agent不只是执行命令，它需要**规划**。

今天你将学习如何让Agent制定计划、分解目标，并执行复杂的多步骤任务。

## 🔑 核心概念

### 计划的三个层次

`
┌─────────────────────────────────────┐
│        Strategic Plan               │
│        战略计划（高层目标）           │
├─────────────────────────────────────┤
│        Tactical Plan                │
│        战术计划（中间步骤）           │
├─────────────────────────────────────┤
│        Operational Plan             │
│        操作计划（具体行动）           │
└─────────────────────────────────────┘
`

### 计划与执行的循环

`python
while not goal_achieved:
    # 1. 制定计划
    plan = planner.create_plan(goal, context)
    
    # 2. 执行计划
    for step in plan.steps:
        result = executor.execute(step)
        
        # 3. 监控执行
        if result.failed:
            # 4. 调整计划
            plan = planner.replan(goal, result, plan)
            break
        
        # 5. 更新状态
        state.update(step, result)
    
    # 6. 评估进展
    if goal_achieved(state):
        break
`

---

> 📖 详细课程内容见 [lesson.md](./lesson.md)  
> 💪 挑战任务见 [challenge.md](./challenge.md)  
> 🏆 终极挑战见 [ultimate_challenge.md](./ultimate_challenge.md)
