# Day 30 终极挑战 Starter

# ══════════════════════════════════════
# 项目入口 - main.py
# ══════════════════════════════════════
#
# 你的项目应该可以通过以下方式启动：
# python -m ai_assistant
#
# __main__.py 中应该：
# 1. 加载配置（Config.from_env()）
# 2. 验证配置
# 3. 创建 AIEngine
# 4. 创建 ToolRegistry + 注册工具
# 5. 创建 Memory
# 6. 创建 Agent
# 7. 创建 CLI
# 8. 运行 CLI

# ══════════════════════════════════════
# 启动代码骨架
# ══════════════════════════════════════

import asyncio
import logging

# TODO: 从你的模块导入
# from ai_assistant.config.settings import Config
# from ai_assistant.core.engine import AIEngine
# from ai_assistant.tools.registry import ToolRegistry
# from ai_assistant.tools.file_tool import FileReadTool, FileWriteTool
# from ai_assistant.tools.shell_tool import ShellExecTool
# from ai_assistant.tools.code_tool import CodeExecTool
# from ai_assistant.memory.history import SlidingWindowMemory
# from ai_assistant.core.agent import Agent
# from ai_assistant.cli import CLI


def main():
    # 1. 配置
    config = Config.from_env()
    errors = config.validate()
    if errors:
        print(f"配置错误: {', '.join(errors)}")
        return
    
    # 2. 日志
    logging.basicConfig(level=getattr(logging, config.log_level))
    
    # 3. 引擎
    engine = AIEngine(
        api_key=config.api_key,
        model=config.model,
        temperature=config.temperature,
        max_tokens=config.max_tokens,
    )
    
    # 4. 工具
    tools = ToolRegistry()
    tools.register(FileReadTool())
    tools.register(FileWriteTool())
    tools.register(ShellExecTool())
    tools.register(CodeExecTool())
    
    # 5. Memory
    memory = SlidingWindowMemory(
        system_prompt=config.system_prompt,
        max_messages=20,
    )
    
    # 6. Agent
    agent = Agent(
        engine=engine,
        tools=tools,
        memory=memory,
        max_iterations=config.max_iterations,
    )
    
    # 7. CLI
    cli = CLI(agent)
    asyncio.run(cli.run())


if __name__ == "__main__":
    main()

# ══════════════════════════════════════
# 完成标准检查
# ══════════════════════════════════════
#
# □ python -m ai_assistant 能启动
# □ 能进行多轮对话
# □ 至少4个工具能调用
# □ Memory管理历史
# □ 配置从环境变量读取
# □ 所有模块有类型注解
# □ pytest tests/ 通过
# □ 不是单文件
# □ pyproject.toml 正确
# □ 代码可读
