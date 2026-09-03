"""Day 30 示例：Agent核心 + CLI参考实现"""

from __future__ import annotations
import asyncio
import json
import logging
import os
from dataclasses import dataclass
from typing import AsyncGenerator, Any

from openai import AsyncOpenAI

logger = logging.getLogger("ai_assistant")


# ══════════════════════════════════════
# AI Engine
# ══════════════════════════════════════

@dataclass
class ChatResponse:
    content: str | None
    tool_calls: list | None = None
    usage: dict | None = None
    raw_message: Any = None


class AIEngine:
    def __init__(self, api_key: str, model: str = "gpt-4o-mini", **kwargs):
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = model
        self.temperature = kwargs.get("temperature", 0.7)
        self.max_tokens = kwargs.get("max_tokens", 2000)
    
    async def chat(
        self, messages: list[dict], tools: list[dict] | None = None,
    ) -> ChatResponse:
        kwargs: dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }
        if tools:
            kwargs["tools"] = tools
        
        response = await self.client.chat.completions.create(**kwargs)
        msg = response.choices[0].message
        
        return ChatResponse(
            content=msg.content,
            tool_calls=[
                {"id": tc.id, "name": tc.function.name, "arguments": tc.function.arguments}
                for tc in (msg.tool_calls or [])
            ] or None,
            usage={
                "prompt": response.usage.prompt_tokens,
                "completion": response.usage.completion_tokens,
                "total": response.usage.total_tokens,
            } if response.usage else None,
            raw_message=msg,
        )
    
    async def chat_stream(self, messages: list[dict]) -> AsyncGenerator[str, None]:
        stream = await self.client.chat.completions.create(
            model=self.model, messages=messages, stream=True,
        )
        async for chunk in stream:
            delta = chunk.choices[0].delta
            if delta.content:
                yield delta.content


# ══════════════════════════════════════
# Agent
# ══════════════════════════════════════

class Agent:
    def __init__(self, engine: AIEngine, tools, memory, max_iterations: int = 10):
        self.engine = engine
        self.tools = tools  # ToolRegistry
        self.memory = memory  # BaseMemory
        self.max_iterations = max_iterations
        self._total_tokens = 0
    
    async def run(self, user_input: str) -> AsyncGenerator[str, None]:
        """Agent主循环"""
        self.memory.add("user", user_input)
        
        for i in range(self.max_iterations):
            logger.info(f"Iteration {i + 1}/{self.max_iterations}")
            
            messages = self.memory.get_messages()
            tool_defs = self.tools.get_definitions()
            
            response = await self.engine.chat(messages, tools=tool_defs or None)
            
            # 累计token
            if response.usage:
                self._total_tokens += response.usage["total"]
            
            if response.tool_calls:
                yield f"[思考] 需要使用工具...\n"
                
                # 保存assistant消息（含tool_calls）到memory
                self.memory.add("assistant", json.dumps(
                    [{"name": tc["name"], "args": tc["arguments"]} for tc in response.tool_calls],
                    ensure_ascii=False,
                ))
                
                # 并行执行工具
                results = await self._execute_parallel(response.tool_calls)
                
                for result in results:
                    yield f"[工具 {result['name']}] {result['content'][:200]}\n"
                    self.memory.add("tool", result["content"])
            else:
                # 最终回答
                answer = response.content or "(无响应)"
                self.memory.add("assistant", answer)
                yield answer
                return
        
        yield "\n[达到最大迭代次数]"
    
    async def _execute_parallel(self, tool_calls: list[dict]) -> list[dict]:
        async def exec_one(tc):
            name = tc["name"]
            args = json.loads(tc["arguments"])
            logger.info(f"Executing tool: {name}({args})")
            result = await self.tools.execute(name, **args)
            return {"name": name, "content": str(result)}
        
        tasks = [exec_one(tc) for tc in tool_calls]
        return await asyncio.gather(*tasks)
    
    @property
    def total_tokens(self) -> int:
        return self._total_tokens
    
    @property
    def estimated_cost(self) -> float:
        # gpt-4o-mini pricing
        return self._total_tokens * 0.00015 / 1000  # very rough


# ══════════════════════════════════════
# CLI
# ══════════════════════════════════════

class CLI:
    def __init__(self, agent: Agent):
        self.agent = agent
        self.running = True
    
    async def run(self):
        print("=" * 50)
        print("  AI Assistant v1.0")
        print("  命令: /quit /clear /history /tools /tokens")
        print("=" * 50)
        
        while self.running:
            try:
                user_input = input("\n你: ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\n再见！")
                break
            
            if not user_input:
                continue
            
            if user_input.startswith("/"):
                await self._handle_command(user_input)
                continue
            
            print("\n助手: ", end="", flush=True)
            async for chunk in self.agent.run(user_input):
                print(chunk, end="", flush=True)
            print()
    
    async def _handle_command(self, cmd: str):
        cmd = cmd.strip().lower()
        
        if cmd == "/quit":
            self.running = False
            print("再见！")
        elif cmd == "/clear":
            self.agent.memory.clear()
            print("对话已清空。")
        elif cmd == "/history":
            msgs = self.agent.memory.get_messages()
            for m in msgs:
                role = {"user": "你", "assistant": "助手", "tool": "工具"}.get(m["role"], m["role"])
                content = m["content"][:100]
                print(f"  [{role}] {content}")
        elif cmd == "/tools":
            tools = self.agent.tools.list_tools()
            print("可用工具:")
            for i, t in enumerate(tools, 1):
                print(f"  {i}. {t}")
        elif cmd == "/tokens":
            print(f"总Token: {self.agent.total_tokens}")
            print(f"估算成本: ")
        else:
            print(f"未知命令: {cmd}")


if __name__ == "__main__":
    print("这是参考实现。请在你的项目中实现这些模块。")
