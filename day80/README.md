# Day 80: Context Engineering — 上下文工程

> 上下文窗口是LLM的"工作台"，上下文工程就是让你的工作台永远够大、够干净、够精准。

## 今日目标
- 理解上下文窗口的本质与限制
- 掌握Token预算管理与动态上下文注入
- 学会System Prompt工程与上下文压缩
- 实现一个完整的上下文管理系统

## 前置知识
- Day 76-79: Agent架构、工具系统、工具开发、Planning

## 目录结构
`
day80/
├── README.md          # 本文件
├── lesson.md          # 完整知识点
├── challenge.md       # 5个挑战概览
├── ultimate_challenge.md
├── examples/          # 可运行示例
├── starter/           # 骨架代码
├── tests/             # 测试
└── code/              # 你的实现
`

## 快速开始
`ash
cd examples
python 01_token_counter.py
python 02_context_manager.py
python 03_sliding_window.py
`

## 今日挑战
| # | 难度 | 主题 |
|---|------|------|
| 1 | ⭐ | Token计数器 |
| 2 | ⭐⭐ | System Prompt模板 |
| 3 | ⭐⭐⭐ | 上下文压缩器 |
| 4 | ⭐⭐⭐⭐ | 滑动窗口管理器 |
| 5 | 🏆 | 完整上下文管理系统 |
