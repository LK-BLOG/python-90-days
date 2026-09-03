#!/usr/bin/env python3
"""Agent Loop Example"""

import asyncio
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum


class AgentState(Enum):
    IDLE = "idle"
    THINKING = "thinking"
    ACTING = "acting"
    OBSERVING = "observing"
    FINISHED = "finished"
    ERROR = "error"


@dataclass
class Message:
    role: str
    content: str
    metadata: Optional[Dict] = None


class MockLLM:
    def __init__(self):
        self.call_count = 0
    
    async def chat(self, messages: List[Message]):
        self.call_count += 1
        class Response:
            content = f"Response {self.call_count}"
            tool_calls = None
        return Response()


class MockToolExecutor:
    async def execute(self, tool_calls: List[Dict]) -> List[Any]:
        return [{"tool": "mock", "result": "success"}]


class MockMemory:
    def __init__(self):
        self.messages: List[Message] = []
    def add_message(self, message: Message):
        self.messages.append(message)
    def get_messages(self):
        return self.messages


class MockStateManager:
    def __init__(self):
        self.state: Dict[str, Any] = {}
    def set(self, key, value):
        self.state[key] = value
    def get(self, key):
        return self.state.get(key)


class AgentLoop:
    def __init__(self, llm, tools, memory, state):
        self.llm = llm
        self.tools = tools
        self.memory = memory
        self.state = state
        self.max_iterations = 10
        self.current_state = AgentState.IDLE
    
    async def run(self, user_input: str) -> str:
        print(f"[Agent] Input: {user_input}")
        self.memory.add_message(Message(role="user", content=user_input))
        
        for i in range(self.max_iterations):
            print(f"[Agent] Iteration {i+1}")
            self.current_state = AgentState.THINKING
            response = await self.llm.chat(self.memory.get_messages())
            
            if response.tool_calls:
                self.current_state = AgentState.ACTING
                tool_results = await self.tools.execute(response.tool_calls)
                for result in tool_results:
                    self.memory.add_message(Message(role="tool", content=str(result)))
                self.current_state = AgentState.OBSERVING
            else:
                self.memory.add_message(Message(role="assistant", content=response.content))
                self.current_state = AgentState.FINISHED
                print(f"[Agent] Done: {response.content}")
                return response.content
        
        raise RuntimeError("Max iterations reached")


async def main():
    print("=== Agent Loop Example ===")
    llm = MockLLM()
    tools = MockToolExecutor()
    memory = MockMemory()
    state = MockStateManager()
    
    agent = AgentLoop(llm, tools, memory, state)
    result = await agent.run("hello world")
    print(f"\nResult: {result}")
    print(f"State: {agent.current_state.value}")
    print(f"Messages: {len(memory.messages)}")


if __name__ == "__main__":
    asyncio.run(main())
