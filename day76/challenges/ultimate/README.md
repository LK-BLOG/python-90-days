# Day 76 - 挑战 5（Boss）: 混合模式 Agent
## 难度: ⭐⭐⭐⭐⭐

## 任务
实现结合 ReAct 和 Plan-and-Execute 的混合 Agent。

## 要求
1. 先用 Plan-and-Execute 制定计划
2. 每个步骤内部用 ReAct 执行
3. 步骤失败触发重新规划
4. 完整的状态管理

## 架构
`
HybridAgent
├── Planner (宏观计划)
├── ReActExecutor (微观执行)
├── StateManager (状态管理)
└── Replanner (重新规划)
`
"@ | Out-File -Encoding utf8 "D:\Python-Learn-30-days\challenges\day76\challenge05\README.md"

@"
# Day 76 - 终极挑战
## Mini ReAct Engine

从零实现最小化的 ReAct 引擎。

## 功能要求
1. Agent 核心循环 (react_step + react_loop)
2. 工具注册和调用系统
3. 动态 Prompt 构建
4. 输出解析 (Thought/Action)
5. 退出条件 (finish + max_steps)
6. 完整追踪系统
