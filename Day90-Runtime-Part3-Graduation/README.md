# Day 90: Agent 项目 - AI Assistant Runtime③ + 毕业

## 🎯 最终目标

- 完成所有功能集成
- 实现多Agent支持
- 添加评估与监控
- 实现安全护栏
- **通过毕业验收！**

## 📋 前置知识

- Day 76-89: 所有Agent知识

## ⏰ 预计时间：2-3小时

---

# 🎓 毕业项目：AI Assistant Runtime

## 项目要求

你需要构建一个完整的AI Assistant Runtime，包含以下功能：

### 核心功能

| 功能 | 描述 | 状态 |
|------|------|------|
| 多轮对话 | 支持上下文的多轮对话 | ☐ |
| 工具调用 | 至少5个工具 | ☐ |
| Memory系统 | 短期和长期记忆 | ☐ |
| Planning | 任务分解和规划 | ☐ |
| Self-Correction | 错误检测和纠正 | ☐ |
| Context管理 | 上下文窗口管理 | ☐ |
| 状态持久化 | 检查点和恢复 | ☐ |
| 安全护栏 | 输入输出安全 | ☐ |
| 可观测性 | 日志和追踪 | ☐ |

### 技术要求

- [ ] 使用包结构（src/ layout）
- [ ] 完整类型注解
- [ ] 测试覆盖
- [ ] 项目文档

## 项目结构

`
ai-assistant-runtime/
├── pyproject.toml
├── README.md
├── src/
│   └── ai_runtime/
│       ├── __init__.py
│       ├── agent/
│       │   ├── __init__.py
│       │   ├── core.py
│       │   ├── loop.py
│       │   └── state.py
│       ├── tools/
│       │   ├── __init__.py
│       │   ├── base.py
│       │   ├── registry.py
│       │   └── builtin/
│       │       ├── __init__.py
│       │       ├── search.py
│       │       ├── calculator.py
│       │       ├── file_ops.py
│       │       ├── code_executor.py
│       │       └── web_request.py
│       ├── memory/
│       │   ├── __init__.py
│       │   ├── short_term.py
│       │   ├── long_term.py
│       │   └── working.py
│       ├── planning/
│       │   ├── __init__.py
│       │   ├── planner.py
│       │   └── validator.py
│       ├── context/
│       │   ├── __init__.py
│       │   ├── manager.py
│       │   └── compressor.py
│       ├── safety/
│       │   ├── __init__.py
│       │   ├── guardrails.py
│       │   └── validator.py
│       └── observability/
│           ├── __init__.py
│           ├── logger.py
│           ├── tracer.py
│           └── metrics.py
├── tests/
│   ├── test_agent.py
│   ├── test_tools.py
│   ├── test_memory.py
│   ├── test_planning.py
│   └── test_integration.py
├── examples/
│   ├── basic_usage.py
│   ├── advanced_usage.py
│   └── multi_agent.py
└── docs/
    ├── architecture.md
    ├── api_reference.md
    └── examples.md
`

## 毕业验收标准

### 功能验收（60分）

- [ ] Agent能执行多步任务（10分）
- [ ] 至少5个工具正常工作（10分）
- [ ] Memory系统有效（10分）
- [ ] Planning功能正常（10分）
- [ ] 安全护栏工作（10分）
- [ ] 可观测性完整（10分）

### 代码质量（20分）

- [ ] 代码结构清晰（5分）
- [ ] 完整类型注解（5分）
- [ ] 错误处理完善（5分）
- [ ] 文档完整（5分）

### 测试覆盖（20分）

- [ ] 单元测试覆盖核心功能（10分）
- [ ] 集成测试完整（10分）

**总分：100分，70分以上通过毕业**

---

> 📖 详细课程内容见 [lesson.md](./lesson.md)  
> 💪 最终挑战见 [ultimate_challenge.md](./ultimate_challenge.md)  
> 📋 毕业验收见 [graduation.md](./graduation.md)
