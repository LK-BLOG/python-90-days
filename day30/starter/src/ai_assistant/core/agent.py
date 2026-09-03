"""Day 30 - Agent 核心循环（ReAct 模式）"""
from __future__ import annotations

import json
import logging
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ai_assistant.config import Config
    from ai_assistant.core.engine import AIEngine
    from ai_assistant.memory.base import BaseMemory
    from ai_assistant.tools.registry import ToolRegistry

logger = logging.getLogger(__name__)


class Agent:
    """ReAct Agent

    实现 Thought → Act → Observe 循环：
    1. 思考：AI 分析当前情况
    2. 行动：调用工具或生成回答
    3. 观察：获取工具执行结果
    4. 重复直到完成或达到最大迭代次数
    """

    def __init__(self, engine: "AIEngine", tools: "ToolRegistry",
                 memory: "BaseMemory", config: "Config"):
        """初始化

        Args:
            engine: AI 引擎
            tools: 工具注册器
            memory: 记忆系统
            config: 配置
        """
        self.engine = engine
        self.tools = tools
        self.memory = memory
        self.config = config
        self._iteration = 0

    async def run(self, user_input: str) -> str:
        """运行 Agent 主循环

        Args:
            user_input: 用户输入

        Returns:
            Agent 的最终回复
        """
        # TODO: 1. 将用户输入添加到 memory
        self.memory.add("user", user_input)
        # TODO: 2. ReAct 循环
        for i in range(self.config.max_iterations):
            self._iteration = i + 1
            logger.info(f"=== 迭代 {self._iteration}/{self.config.max_iterations} ===")
            # TODO: 3. 调用 AI 引擎
            # TODO: 4. 如果有 tool_calls，执行工具并将结果加入 memory
            # TODO: 5. 如果没有 tool_calls，返回最终回答
            ...
        # TODO: 6. 达到最大迭代时返回错误信息
        return "⚠️ 达到最大迭代次数，未能完成任务。"

    async def _handle_tool_calls(self, tool_calls: list[dict]) -> list[str]:
        """处理工具调用

        Args:
            tool_calls: 工具调用列表

        Returns:
            工具执行结果列表
        """
        # TODO: 逐个执行工具调用
        # TODO: 处理错误
        results = []
        for tc in tool_calls:
            name = tc["function"]["name"]
            args = json.loads(tc["function"]["arguments"])
            logger.info(f"调用工具: {name}({args})")
            # TODO: 执行并收集结果
            ...
        return results

    def _build_messages(self) -> list[dict]:
        """构建发送给 AI 的消息列表"""
        return self.memory.get_messages()
