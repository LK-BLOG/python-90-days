"""Day 29 测试：Memory系统"""

import pytest


class TestSlidingWindowMemory:
    def test_add_and_get(self):
        from day29.starter.memory_starter import SlidingWindowMemory
        mem = SlidingWindowMemory(max_messages=5)
        mem.add("user", "Hello")
        mem.add("assistant", "Hi!")
        messages = mem.get_messages()
        assert len(messages) == 3  # system + 2
        assert messages[0]["role"] == "system"
    
    def test_sliding_window(self):
        from day29.starter.memory_starter import SlidingWindowMemory
        mem = SlidingWindowMemory(max_messages=4)
        for i in range(10):
            mem.add("user" if i % 2 == 0 else "assistant", f"msg{i}")
        messages = mem.get_messages()
        # system + 最近4条 = 5
        assert len(messages) == 5
    
    def test_clear(self):
        from day29.starter.memory_starter import SlidingWindowMemory
        mem = SlidingWindowMemory()
        mem.add("user", "test")
        mem.clear()
        assert len(mem.get_messages()) == 1  # 只剩system


class TestTokenAwareMemory:
    def test_token_limit(self):
        from day29.starter.memory_starter import TokenAwareMemory
        mem = TokenAwareMemory(max_tokens=100)
        mem.add("user", "short")
        mem.add("user", "x" * 500)
        messages = mem.get_messages()
        # 短消息应该被保留，长消息可能被截断
        assert len(messages) >= 1  # 至少有system
    
    def test_system_prompt_always_present(self):
        from day29.starter.memory_starter import TokenAwareMemory
        mem = TokenAwareMemory(system_prompt="Custom system", max_tokens=10)
        mem.add("user", "x" * 1000)
        messages = mem.get_messages()
        assert messages[0]["content"] == "Custom system"


class TestToolRegistry:
    def test_register_tool(self):
        from day29.starter.agent_starter import ToolRegistry
        registry = ToolRegistry()
        
        @registry.register("test_tool", "A test tool", {
            "type": "object",
            "properties": {"x": {"type": "string"}},
            "required": ["x"],
        })
        def test_tool(x: str) -> str:
            return f"result:{x}"
        
        defs = registry.get_definitions()
        assert len(defs) == 1
        assert defs[0]["function"]["name"] == "test_tool"
    
    @pytest.mark.asyncio
    async def test_execute_tool(self):
        from day29.starter.agent_starter import ToolRegistry
        registry = ToolRegistry()
        
        @registry.register("add", "Add two numbers", {
            "type": "object",
            "properties": {
                "a": {"type": "integer"},
                "b": {"type": "integer"},
            },
        })
        async def add(a: int, b: int) -> int:
            return a + b
        
        result = await registry.execute("add", a=3, b=4)
        assert result == 7
    
    @pytest.mark.asyncio
    async def test_unknown_tool(self):
        from day29.starter.agent_starter import ToolRegistry
        registry = ToolRegistry()
        result = await registry.execute("nonexistent")
        assert "错误" in str(result) or "未知" in str(result)
