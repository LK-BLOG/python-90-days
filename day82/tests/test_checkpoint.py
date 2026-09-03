"""Day 82 测试: Checkpoint"""
import pytest
import os
import sys
import shutil
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "examples"))

TEST_CKPT_DIR = "./test_checkpoints"


@pytest.fixture(autouse=True)
def cleanup():
    yield
    if os.path.exists(TEST_CKPT_DIR):
        shutil.rmtree(TEST_CKPT_DIR)


def test_save_and_load_checkpoint():
    """测试保存和加载检查点"""
    from importlib import import_module
    mod = import_module("03_checkpoint")

    mgr = mod.CheckpointManager(TEST_CKPT_DIR)
    state = {"step": 3, "results": ["a", "b", "c"]}
    mgr.save_checkpoint("agent1", "task1", 3, state)

    loaded = mgr.load_checkpoint("agent1", "task1", step=3)
    assert loaded is not None
    assert loaded["step"] == 3
    assert loaded["state"]["results"] == ["a", "b", "c"]


def test_load_latest():
    """测试加载最新检查点"""
    from importlib import import_module
    mod = import_module("03_checkpoint")

    mgr = mod.CheckpointManager(TEST_CKPT_DIR)
    mgr.save_checkpoint("a", "t", 1, {"step": 1})
    mgr.save_checkpoint("a", "t", 3, {"step": 3})
    mgr.save_checkpoint("a", "t", 5, {"step": 5})

    latest = mgr.load_checkpoint("a", "t")
    assert latest["step"] == 5


def test_list_checkpoints():
    """测试列出检查点"""
    from importlib import import_module
    mod = import_module("03_checkpoint")

    mgr = mod.CheckpointManager(TEST_CKPT_DIR)
    mgr.save_checkpoint("a", "t", 1, {"step": 1})
    mgr.save_checkpoint("a", "t", 2, {"step": 2})

    cps = mgr.list_checkpoints("a", "t")
    assert len(cps) == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
