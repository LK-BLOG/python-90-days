# Day 30 挑战任务

## Challenge 1: 搭建项目骨架 + 配置系统
**目标：** 创建完整的项目结构和配置管理

**要求：**
- 创建 src/ai_assistant/ 包结构
- 编写 pyproject.toml
- 实现 Config 类（pydantic-settings 或 dataclass）
- 支持环境变量和 .env 文件
- 实现 __init__.py 和 __main__.py
- 所有模块文件创建但可以为空

**验收：** python -m ai_assistant 能启动（哪怕只打印一行字）

**难度：** ⭐⭐

---

## Challenge 2: 工具注册系统 + 至少2个工具
**目标：** 实现工具注册器和具体工具

**要求：**
- 实现 BaseTool 抽象基类
- 实现 ToolRegistry 注册器
- 实现 FileReadTool 和 CalculatorTool
- 支持装饰器或实例注册
- get_definitions() 返回OpenAI格式
- 测试覆盖工具注册和执行

**难度：** ⭐⭐⭐

---

## Challenge 3: Memory系统
**目标：** 实现对话记忆管理

**要求：**
- 实现 BaseMemory 接口
- 实现 SlidingWindowMemory
- 实现 SummaryMemory（可选，用AI压缩）
- Token估算和限制
- System prompt始终保留
- clear() 正确工作
- 测试覆盖

**难度：** ⭐⭐⭐

---

## Challenge 4: Agent核心循环 + AI引擎
**目标：** 实现Agent决策循环和API调用

**要求：**
- 实现 AIEngine（封装OpenAI API调用）
- 实现 Agent.run() ReAct循环
- 集成Memory和Tools
- 支持tool_calls处理
- 最大迭代限制
- 基本错误处理
- 测试覆盖Agent逻辑

**难度：** ⭐⭐⭐⭐

---

## Challenge 5 (Boss): 完整功能 + 高级特性
**目标：** 完成整个项目，添加高级特性

**要求：**
- 实现CLI交互界面
- 至少4个工具（文件、Shell、代码执行、搜索）
- 流式输出逐字显示
- Token计数和成本估算
- 对话保存/加载（JSON）
- /tools, /history, /clear 命令
- 完整的 pyproject.toml
- 所有测试通过

**难度：** ⭐⭐⭐⭐⭐
