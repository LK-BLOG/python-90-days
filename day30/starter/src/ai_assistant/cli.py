"""Day 30 - AI Assistant CLI 交互界面

支持命令：
- /tools: 显示可用工具
- /history: 显示对话历史
- /clear: 清空对话
- /save: 保存对话
- /load: 加载对话
- /quit: 退出
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ai_assistant.core.agent import Agent


class CLI:
    """命令行交互界面"""

    BANNER = """
╔══════════════════════════════════╗
║      🤖 AI Assistant v0.1       ║
║   输入 /help 查看所有命令        ║
╚══════════════════════════════════╝
"""
    COMMANDS = {
        "/tools": "显示所有可用工具",
        "/history": "显示对话历史",
        "/clear": "清空对话历史",
        "/save": "保存对话到文件",
        "/load": "从文件加载对话",
        "/quit": "退出程序",
        "/help": "显示帮助信息",
    }

    def __init__(self, agent: "Agent"):
        """初始化 CLI

        Args:
            agent: AI Agent 实例
        """
        self.agent = agent
        self.history_file = Path("conversation.json")

    def run(self) -> None:
        """启动交互循环"""
        # TODO: 打印 Banner
        # TODO: 循环读取用户输入
        # TODO: 处理命令（/xxx）或调用 agent
        # TODO: 流式输出 agent 响应
        ...

    def handle_command(self, command: str) -> bool:
        """处理用户命令

        Args:
            command: 用户输入的命令（以 / 开头）

        Returns:
            False 表示应退出
        """
        # TODO: 根据命令执行对应操作
        ...

    def show_tools(self) -> None:
        """显示所有可用工具"""
        # TODO: 列出 agent 注册的所有工具
        ...

    def show_history(self) -> None:
        """显示对话历史"""
        # TODO: 格式化输出所有消息
        ...

    def save_conversation(self) -> None:
        """保存对话到 JSON 文件"""
        # TODO: 序列化对话历史
        ...

    def load_conversation(self) -> None:
        """从 JSON 文件加载对话"""
        # TODO: 反序列化并恢复对话
        ...


def run_cli() -> None:
    """CLI 入口"""
    # TODO: 创建 Agent，启动 CLI
    print("请先实现 Agent 模块")
