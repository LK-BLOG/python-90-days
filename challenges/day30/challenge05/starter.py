# Challenge 5 Starter: 完整项目骨架
# 这是最终挑战的起始代码。
# 你需要把之前所有Challenge的实现整合到这里。

# ══════════════════════════════════════
# 项目结构（参考）
# ══════════════════════════════════════
#
# ai_assistant/
# ├── pyproject.toml
# ├── src/ai_assistant/
# │   ├── __init__.py
# │   ├── __main__.py
# │   ├── cli.py
# │   ├── core/
# │   │   ├── agent.py
# │   │   ├── engine.py
# │   │   └── prompt.py
# │   ├── tools/
# │   │   ├── registry.py
# │   │   ├── base.py
# │   │   ├── file_tool.py
# │   │   ├── shell_tool.py
# │   │   ├── code_tool.py
# │   │   └── search_tool.py
# │   ├── memory/
# │   │   ├── base.py
# │   │   ├── history.py
# │   │   └── summary.py
# │   ├── config/
# │   │   └── settings.py
# │   └── utils/
# │       └── logger.py
# └── tests/
#
# ══════════════════════════════════════
# TODO清单（按优先级）
# ══════════════════════════════════════
#
# P0 必须：
# □ Config类（from_env, from_file, validate）
# □ ToolRegistry + BaseTool + ToolResult
# □ 至少4个工具（file_read, file_write, shell_exec, code_exec）
# □ BaseMemory + SlidingWindowMemory
# □ AIEngine（chat, chat_stream）
# □ Agent.run() ReAct循环
# □ CLI交互（/quit, /clear, /history, /tools）
# □ __main__.py 入口
#
# P1 应该：
# □ 流式输出
# □ Token计数和成本估算
# □ 对话保存/加载JSON
# □ 日志系统
# □ 测试覆盖
#
# P2 加分：
# □ 摘要压缩Memory
# □ 搜索工具
# □ 装饰器注册
# □ 上下文管理器

print("这是Challenge 5的起始骨架。请完成上面的TODO清单。")
