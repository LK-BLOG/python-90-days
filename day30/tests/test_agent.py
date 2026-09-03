# Day 30 测试：Agent
import pytest

class TestAgent:
    @pytest.mark.asyncio
    async def test_agent_responds(self):
        pytest.skip("请实现后取消注释")
    
    @pytest.mark.asyncio
    async def test_agent_uses_tool(self):
        pytest.skip("请实现后取消注释")
    
    @pytest.mark.asyncio
    async def test_agent_max_iterations(self):
        pytest.skip("请实现后取消注释")

class TestConfig:
    def test_from_env(self):
        pytest.skip("请实现后取消注释")
    
    def test_validate_missing_key(self):
        pytest.skip("请实现后取消注释")
