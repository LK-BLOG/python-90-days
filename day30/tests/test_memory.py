# Day 30 测试：Memory系统
import pytest

class TestBaseMemory:
    def test_sliding_window_add(self):
        # TODO: 导入你的 SlidingWindowMemory 并测试
        # mem = SlidingWindowMemory(max_messages=5)
        # mem.add("user", "hello")
        # assert len(mem.get_messages()) == 2  # system + 1
        pytest.skip("请实现后取消注释")
    
    def test_sliding_window_limit(self):
        pytest.skip("请实现后取消注释")
    
    def test_token_aware_limit(self):
        pytest.skip("请实现后取消注释")
    
    def test_clear(self):
        pytest.skip("请实现后取消注释")

class TestSummaryMemory:
    def test_add_messages(self):
        pytest.skip("请实现后取消注释")
    
    def test_save_load(self):
        pytest.skip("请实现后取消注释")
