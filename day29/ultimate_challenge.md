# Day 29 Boss挑战：AI助手Agent

## 🎯 任务

构建一个带工具调用的AI助手Agent，支持搜索、计算、文件操作等工具，有对话记忆。

## 📋 功能要求

### 1. AI引擎
- 调用OpenAI Chat Completion API
- 支持流式输出（stream=True）
- 支持system prompt自定义
- 错误重试（指数退避）

### 2. 工具系统（至少4个工具）
- **Calculator**: 安全的数学计算（不直接eval）
- **FileReader**: 读取指定文件内容
- **FileWriter**: 写入内容到文件
- **WebSearch**: 模拟网络搜索（或用真实API）
- **CodeExecutor**: 在沙箱中执行Python代码

### 3. Memory系统
- 对话历史管理
- Token计数和限制
- 摘要压缩（历史过长时自动触发）
- 支持保存/加载对话

### 4. Agent循环
- ReAct模式
- 最大迭代10次
- 每步日志输出
- 错误处理和优雅降级

### 5. CLI交互
- 交互式循环（输入quit退出）
- 命令支持：/clear 清空记忆、/history 查看历史、/tools 列出工具
- 彩色输出（可选）

## 🏗️ 架构

`
ai_assistant/
├── agent.py          # Agent核心
├── engine.py         # AI引擎
├── memory.py         # 记忆系统
├── tools/
│   ├── __init__.py
│   ├── registry.py   # 工具注册
│   ├── calculator.py
│   ├── file_tools.py
│   ├── code_executor.py
│   └── search.py
├── cli.py            # 命令行界面
└── main.py           # 入口
`

## ✅ 验收标准

1. [ ] python main.py 启动交互式对话
2. [ ] AI能正确调用至少4个工具完成任务
3. [ ] 对话记忆在多轮中保持上下文
4. [ ] Token超限时自动压缩
5. [ ] /tools 列出所有可用工具
6. [ ] /history 显示对话历史
7. [ ] 错误情况下不会崩溃
8. [ ] 有基本的日志输出

## 💡 高级特性（加分项）

- 流式输出逐字显示
- Token成本估算
- 对话保存为JSON文件
- 加载历史对话继续
- 彩色终端输出
- 工具执行超时控制
