# Day 30 终极挑战：毕业项目验收

## 🎓 这是你的毕业考试

完成这个挑战，意味着你已经掌握了Python开发的完整技能栈。

## 项目名称
**AI CLI Assistant** (i_assistant)

## 功能需求清单

### P0 — 必须完成
- [ ] python -m ai_assistant 启动
- [ ] 多轮AI对话（调用OpenAI API）
- [ ] 至少4个工具：file_read, file_write, shell_exec, code_exec
- [ ] Memory管理对话历史
- [ ] 配置从环境变量读取
- [ ] 所有模块有类型注解

### P1 — 应该完成
- [ ] 流式输出（逐字打印）
- [ ] 工具注册器（装饰器模式）
- [ ] /tools /clear /history 命令
- [ ] Token计数和限制
- [ ] 完整的pyproject.toml

### P2 — 加分项
- [ ] 摘要压缩Memory
- [ ] Token成本估算
- [ ] 对话保存/加载JSON
- [ ] 搜索工具（用httpx）
- [ ] 日志系统（logging）
- [ ] 测试覆盖率 > 80%

## 架构验收
- [ ] 使用 src/ layout
- [ ] 模块职责清晰（不出现God Object）
- [ ] 使用了至少3种设计模式
- [ ] 使用了类型注解
- [ ] 使用了装饰器
- [ ] 使用了上下文管理器
- [ ] 使用了asyncio

## 代码质量
- [ ] 没有超过200行的单文件
- [ ] 公开API有docstring
- [ ] 没有 import *
- [ ] 没有裸 xcept:
- [ ] 变量命名清晰

## 最终交付

完成后，你的项目应该是这样的：

`ash
# 启动
$ python -m ai_assistant
AI Assistant 已启动。输入 /quit 退出。

你: 帮我读取当前目录的文件列表
[工具] list_directory: .
├── src/
├── tests/
├── pyproject.toml
└── README.md

当前目录有4个项目：
- src/ 是源代码目录
- tests/ 是测试目录
- pyproject.toml 是项目配置
- README.md 是项目文档

你: /tools
可用工具：
1. file_read - 读取文件内容
2. file_write - 写入文件内容
3. shell_exec - 执行Shell命令
4. code_exec - 执行Python代码
5. directory_list - 列出目录内容

你: /quit
再见！
`

## 💡 最后的建议

1. **先跑通骨架，再填肉**。Challenge 1-4不是走过场，每一步都是在为最后的Boss战打基础。
2. **测试不是可选的**。没有测试的项目不是项目，是定时炸弹。
3. **类型注解不是装饰**。它是你的文档，是你的编译器，是你未来回来改代码时的救命稻草。
4. **模块拆分不是为了好看**。每个文件超过300行就该考虑拆分了。
5. **这是你的作品**。把它当成开源项目来写，未来面试官会看到。

祝你毕业顺利 🎓
