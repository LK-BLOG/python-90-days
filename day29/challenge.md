# Day 29 挑战任务

## Challenge 1: 基础API调用
**目标：** 用OpenAI SDK和httpx分别实现一次对话调用

**要求：**
- 用openai库实现AsyncOpenAI调用
- 用httpx手动构造请求实现相同功能
- 处理API错误（401、429、500等）
- 打印token用量

**难度：** ⭐⭐

---

## Challenge 2: Prompt Engineering实战
**目标：** 设计一个代码审查机器人的Prompt

**要求：**
- 系统提示定义角色和输出格式
- 用Few-shot示例教模型你的输出风格
- 用Chain-of-Thought引导模型逐步分析
- 结构化输出（JSON格式返回问题列表）
- 处理输入过长的情况（自动截断）

**难度：** ⭐⭐⭐

---

## Challenge 3: Function Calling
**目标：** 实现工具调用系统

**要求：**
- 定义至少3个工具（计算器、天气查询、文本处理）
- 实现完整的tool_call循环
- 处理工具执行错误
- 支持串行调用多个工具
- 工具结果正确传回模型

**难度：** ⭐⭐⭐

---

## Challenge 4: Memory系统
**目标：** 实现对话记忆管理

**要求：**
- 实现滑动窗口Memory（保留最近N条消息）
- 实现摘要压缩Memory（历史太长时自动压缩）
- 实现token计数和限制
- System prompt始终保留
- 对外提供统一接口

**难度：** ⭐⭐⭐⭐

---

## Challenge 5: 多工具Agent
**目标：** 构建一个完整的ReAct Agent

**要求：**
- 组合Memory + Tools + AI Engine
- 实现ReAct循环（Thought→Act→Observe）
- 支持并行工具调用（asyncio.gather）
- 最大迭代次数限制
- 每一步都有日志输出
- 能完成实际任务（如：分析目录下的Python文件并生成报告）

**难度：** ⭐⭐⭐⭐⭐
