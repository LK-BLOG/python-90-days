"""Day 82 测试: 文件状态持久化"""
import pytest
import os
import sys
import shutil
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "examples"))

TEST_DIR = "./test_states"


@pytest.fixture(autouse=True)
def cleanup():
    yield
    if os.path.exists(TEST_DIR):
        shutil.rmtree(TEST_DIR)


def test_save_and_load():
    """测试保存和加载"""
    from importlib import import_module
    mod = import_module("02_state_persistence")

    mgr = mod.FileStateManager(TEST_DIR)
    state = {"step": 1, "data": "hello"}
    mgr.save("agent_test", state)

    loaded = mgr.load("agent_test")
    assert loaded is not None
    assert loaded["step"] == 1
    assert loaded["data"] == "hello"
    assert "_meta" in loaded


def test_load_nonexistent():
    """测试加载不存在的agent"""
    from importlib import import_module
    mod = import_module("02_state_persistence")

    mgr = mod.FileStateManager(TEST_DIR)
    assert mgr.load("nonexistent") is None


def test_list_agents():
    """测试列出agents"""
    from importlib import import_module
    mod = import_module("02_state_persistence")

    mgr = mod.FileStateManager(TEST_DIR)
    mgr.save("a1", {"x": 1})
    mgr.save("a2", {"x": 2})

    agents = mgr.list_agents()
    assert len(agents) == 2


def test_delete():
    """测试删除"""
    from importlib import import_module
    mod = import_module("02_state_persistence")

    mgr = mod.FileStateManager(TEST_DIR)
    mgr.save("to_delete", {"x": 1})
    assert mgr.exists("to_delete")
    mgr.delete("to_delete")
    assert not mgr.exists("to_delete")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
