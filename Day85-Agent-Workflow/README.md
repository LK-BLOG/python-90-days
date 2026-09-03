# Day 85: Agent 工作流

## 🎯 学习目标

- 理解工作流定义（DAG/状态机）
- 实现条件分支和并行执行
- 学习人工介入（Human-in-the-Loop）
- 掌握工作流编排引擎

## 📋 前置知识

- Day 84: Multi-Agent系统
- 图论基础
- 异步编程

## ⏰ 预计时间：2小时

---

工作流是Agent的"剧本"。它定义了Agent如何一步步完成复杂任务。

今天你将学习如何设计和执行Agent工作流。

## 🔑 核心概念

### DAG工作流

`
    A → B → C
    ↓       ↓
    D → E → F
`

### 工作流元素

| 元素 | 描述 |
|------|------|
| 节点(Node) | 工作流中的一个步骤 |
| 边(Edge) | 节点之间的连接 |
| 条件(Condition) | 分支判断 |
| 并行(Parallel) | 同时执行多个节点 |

---

> 📖 详细课程内容见 [lesson.md](./lesson.md)  
> 💪 挑战任务见 [challenge.md](./challenge.md)  
> 🏆 终极挑战见 [ultimate_challenge.md](./ultimate_challenge.md)
