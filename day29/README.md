# Day 29: AI + Agent — 从调用API到构建智能体

## 🎯 今日目标

1. 理解LLM API基础（OpenAI格式、Chat Completion）
2. 掌握Prompt Engineering核心技巧
3. 学会Function Calling / Tool Use
4. 理解Memory系统设计
5. 掌握Agent架构（ReAct模式）

## 📚 学习路径

| 模块 | 内容 | 时间 |
|------|------|------|
| Lesson | LLM API + Prompt + Function Calling + Agent | 核心学习 |
| Challenge 1 | 调用OpenAI API，实现基础对话 | 30min |
| Challenge 2 | Prompt Engineering实战 | 30min |
| Challenge 3 | Function Calling工具调用 | 45min |
| Challenge 4 | Memory系统实现 | 45min |
| Challenge 5 | 多工具Agent | 45min |
| Boss挑战 | 完整AI助手Agent | 120min |

## 🏗️ 项目结构

`
day29/
├── README.md           # 本文件
├── lesson.md           # 详细课程内容
├── challenge.md        # 挑战说明
├── ultimate_challenge.md # Boss挑战说明
├── examples/           # 示例代码
├── starter/            # 起始代码
└── tests/              # 测试用例
`

## 🔧 环境准备

`ash
pip install openai httpx aiohttp
export OPENAI_API_KEY="your-key-here"
`

## ⚡ 今日哲学

> "AI不是魔法，是一连串的API调用+精心设计的prompt+工程化的工具链。
> 理解了这三层，你就能构建任何AI应用。"

## 📖 前置回顾

到今天为止，你已经掌握了：
- Python核心语法和高级特性（Day 1-15）
- 工程化开发能力（Day 16-20）
- HTTP、API、asyncio（Day 21-28）

今天是把这些全部串联起来，用AI作为大脑，构建真正有用的智能系统。
