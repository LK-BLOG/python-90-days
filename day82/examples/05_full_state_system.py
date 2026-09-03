"""Day 82 Example 05: 完整Agent状态管理系统"""
import json
import os
import time
import copy
import glob
from enum import Enum, auto
from typing import Dict, Any, Callable, Optional, List


class AgentState(Enum):
    IDLE = auto()
    THINKING = auto()
    TOOL_CALLING = auto()
    WAITING = auto()
    ERROR = auto()
    DONE = auto()


class AtomicStateManager:
    """原子写入的状态管理"""

    def __init__(self, storage_dir: str = "./agent_persist"):
        self.storage_dir = storage_dir
        os.makedirs(storage_dir, exist_ok=True)

    def save(self, agent_id: str, data: Dict) -> str:
        filepath = os.path.join(self.storage_dir, f"{agent_id}.json")
        data["_saved_at"] = time.time()
        tmp = filepath + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        os.replace(tmp, filepath)
        return filepath

    def load(self, agent_id: str) -> Optional[Dict]:
        filepath = os.path.join(self.storage_dir, f"{agent_id}.json")
        if not os.path.exists(filepath):
            return None
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)


class CheckpointEngine:
    """检查点引擎"""

    def __init__(self, state_mgr: AtomicStateManager):
        self.state_mgr = state_mgr

    def save_ckpt(self, agent_id: str, task_id: str, step: int, state: Dict):
        ckpt_id = f"{agent_id}_ckpt_{task_id}_{step:04d}"
        data = {"task_id": task_id, "step": step, "state": copy.deepcopy(state)}
        return self.state_mgr.save(ckpt_id, data)

    def load_latest(self, agent_id: str, task_id: str) -> Optional[Dict]:
        pattern = os.path.join(
            self.state_mgr.storage_dir,
            f"{agent_id}_ckpt_{task_id}_*.json"
        )
        files = glob.glob(pattern)
        if not files:
            return None
        files.sort(key=lambda f: int(f.split("_")[-1].split(".")[0]))
        with open(files[-1], "r", encoding="utf-8") as f:
            return json.load(f)


class FullAgent:
    """完整的带状态管理的Agent"""

    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.state_mgr = AtomicStateManager()
        self.ckpt_engine = CheckpointEngine(self.state_mgr)
        self.state = AgentState.IDLE
        self.messages: List[Dict] = []
        self.results: List[str] = []
        self.step = 0

    def run(self, task_id: str, user_input: str, max_steps: int = 5):
        """运行任务，支持断点续传"""
        # 恢复检查点
        ckpt = self.ckpt_engine.load_latest(self.agent_id, task_id)
        if ckpt:
            self.step = ckpt["step"]
            self.results = ckpt["state"].get("results", [])
            print(f"[RESUME] 从步骤 {self.step} 恢复")

        self.messages.append({"role": "user", "content": user_input})

        for step_num in range(self.step + 1, max_steps + 1):
            self.step = step_num
            self.state = AgentState.THINKING
            print(f"  [Step {step_num}] 处理中...")

            # 模拟处理
            result = f"Step {step_num}: 分析了 {len(self.messages)} 条消息"
            self.results.append(result)
            self.messages.append({"role": "assistant", "content": result})

            # 保存检查点
            state_data = {
                "results": self.results,
                "messages": self.messages,
                "step": self.step
            }
            self.ckpt_engine.save_ckpt(self.agent_id, task_id, step_num, state_data)

        self.state = AgentState.DONE
        print(f"[DONE] 任务完成")
        return self.results

    def save_final(self):
        """保存最终状态"""
        state = {
            "agent_id": self.agent_id,
            "state": self.state.name,
            "messages": self.messages,
            "results": self.results,
            "total_steps": self.step
        }
        self.state_mgr.save(self.agent_id, state)


def demo():
    print("=== 完整Agent状态管理系统 ===\n")

    agent = FullAgent("agent_001")

    # 第一次运行（到第3步模拟崩溃）
    print("--- 运行到第3步 ---")
    agent.messages.append({"role": "user", "content": "帮我分析数据"})
    for step in range(1, 4):
        agent.step = step
        agent.results.append(f"Step {step} done")
        state_data = {"results": agent.results, "step": step}
        agent.ckpt_engine.save_ckpt("agent_001", "task_001", step, state_data)
        print(f"  [Step {step}] checkpoint已保存")

    print("\n--- 恢复执行 ---")
    agent2 = FullAgent("agent_001")
    agent2.run("task_001", "继续分析", max_steps=5)

    agent2.save_final()
    print(f"\n最终结果: {agent2.results}")

    # 清理
    import shutil
    shutil.rmtree("./agent_persist", ignore_errors=True)


if __name__ == "__main__":
    demo()
