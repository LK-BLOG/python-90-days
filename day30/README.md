# Day 30: 毕业项目 — AI CLI Assistant / Agent

## 🎓 毕业日

恭喜你走到了最后一天。今天不是上课，是**实战**。

你要把过去29天学到的所有东西——Python语法、OOP、装饰器、上下文管理器、asyncio、类型注解、测试、工程化、HTTP、API——全部整合到一个**真正可用的AI助手项目**中。

## 🎯 项目目标

构建一个 i_assistant Python包，包含：
- CLI交互界面
- AI对话（多轮，流式输出）
- 工具系统（文件读写、Shell执行、Python代码执行、网络搜索）
- Memory系统（对话历史、上下文控制、摘要压缩）
- 配置管理
- 插件式工具注册
- 完整测试

## 📚 学习路径

| 模块 | 内容 | 时间 |
|------|------|------|
| Lesson | 架构设计指南 + 设计模式 + 模块详解 | 架构学习 |
| Challenge 1 | 搭建项目骨架 + 配置系统 | 45min |
| Challenge 2 | 工具注册系统 + 2个工具 | 60min |
| Challenge 3 | Memory系统 | 45min |
| Challenge 4 | Agent核心循环 + AI引擎 | 60min |
| Challenge 5 (Boss) | 完整功能 + 高级特性 | 180min |

## 🏗️ 目录结构

`
ai_assistant/
├── pyproject.toml
├── README.md
├── src/
│   └── ai_assistant/
│       ├── __init__.py
│       ├── __main__.py
│       ├── cli.py
│       ├── core/
│       ├── tools/
│       ├── memory/
│       ├── config/
│       └── utils/
└── tests/
`

## ⚡ 毕业标准

完成Challenge 5后，你的项目应该：
1. python -m ai_assistant 可以启动
2. 能进行多轮AI对话
3. 至少4个工具能调用
4. Memory管理对话历史
5. 配置从文件/环境变量读取
6. 所有模块有类型注解
7. 测试通过
8. **不是单文件**——是真正的包结构

## 🔧 环境准备

`ash
pip install openai httpx aiohttp
export OPENAI_API_KEY="your-key-here"
`

## 💡 记住

> 这不是一个简单的练习。这是一个你可以在简历上写的真实项目。
> 写好了，它是你Python能力的最佳证明。
