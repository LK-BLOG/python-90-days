"""Day 82 Example 03: Checkpoint与断点续传"""
import json
import os
import time
import copy
import glob
from typing import Dict, Any, Optional, List


class CheckpointManager:
    """检查点管理器"""

    def __init__(self, storage_dir: str = "./checkpoints"):
        self.storage_dir = storage_dir
        os.makedirs(storage_dir, exist_ok=True)

    def save_checkpoint(self, agent_id: str, task_id: str,
                        step: int, state: Dict[str, Any],
                        metadata: Dict = None) -> str:
        """保存检查点"""
        checkpoint = {
            "agent_id": agent_id,
            "task_id": task_id,
            "step": step,
            "state": copy.deepcopy(state),
            "metadata": metadata or {},
            "timestamp": time.time(),
            "version": "1.0"
        }

        filename = f"{agent_id}_{task_id}_step{step:04d}.json"
        filepath = os.path.join(self.storage_dir, filename)

        tmp = filepath + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(checkpoint, f, ensure_ascii=False, indent=2)
        os.replace(tmp, filepath)
        return filepath

    def load_checkpoint(self, agent_id: str, task_id: str,
                        step: int = None) -> Optional[Dict]:
        """加载指定步骤或最新的检查点"""
        if step is not None:
            filename = f"{agent_id}_{task_id}_step{step:04d}.json"
            filepath = os.path.join(self.storage_dir, filename)
            if os.path.exists(filepath):
                with open(filepath, "r", encoding="utf-8") as f:
                    return json.load(f)
            return None

        # 加载最新的
        pattern = os.path.join(self.storage_dir, f"{agent_id}_{task_id}_step*.json")
        files = glob.glob(pattern)
        if not files:
            return None

        files.sort(key=lambda f: int(os.path.basename(f).split("_step")[-1].split(".")[0]))
        with open(files[-1], "r", encoding="utf-8") as f:
            return json.load(f)

    def list_checkpoints(self, agent_id: str, task_id: str) -> List[Dict]:
        """列出某任务所有检查点"""
        pattern = os.path.join(self.storage_dir, f"{agent_id}_{task_id}_step*.json")
        results = []
        for fp in sorted(glob.glob(pattern)):
            with open(fp, "r", encoding="utf-8") as f:
                ckpt = json.load(f)
                results.append({
                    "step": ckpt["step"],
                    "timestamp": ckpt["timestamp"],
                    "file": os.path.basename(fp)
                })
        return results

    def cleanup(self, agent_id: str, task_id: str, keep_last: int = 3):
        """清理旧检查点"""
        pattern = os.path.join(self.storage_dir, f"{agent_id}_{task_id}_step*.json")
        files = sorted(glob.glob(pattern),
                      key=lambda f: int(os.path.basename(f).split("_step")[-1].split(".")[0]))
        deleted = 0
        for f in files[:-keep_last]:
            os.remove(f)
            deleted += 1
        return deleted


class ResumableAgent:
    """支持断点续传的Agent"""

    def __init__(self, agent_id: str, checkpoint_mgr: CheckpointManager):
        self.agent_id = agent_id
        self.ckpt_mgr = checkpoint_mgr
        self.state = {"messages": [], "results": [], "step": 0}
        self.task_id = None

    def run_task(self, task_id: str, messages: list, total_steps: int = 5):
        """运行任务，支持从断点恢复"""
        self.task_id = task_id

        # 尝试恢复
        checkpoint = self.ckpt_mgr.load_checkpoint(self.agent_id, task_id)
        if checkpoint:
            self.state = checkpoint["state"]
            start_step = self.state["step"] + 1
            print(f"[RESUME] 从步骤 {start_step} 恢复 (共 {total_steps} 步)")
        else:
            self.state["messages"] = messages
            start_step = 1
            print(f"[START] 从头开始 (共 {total_steps} 步)")

        # 从断点处继续执行
        for step in range(start_step, total_steps + 1):
            self.state["step"] = step

            # 模拟处理
            result = f"Step {step}: 处理了 {len(self.state['messages'])} 条消息"
            self.state["results"].append(result)
            print(f"  [STEP {step}] {result}")

            # 每步保存检查点
            self.ckpt_mgr.save_checkpoint(
                self.agent_id, task_id, step, self.state
            )

        print(f"\n[DONE] 任务完成，共 {total_steps} 步")
        return self.state["results"]


def demo():
    """演示断点续传"""
    print("=== Checkpoint与断点续传演示 ===\n")

    mgr = CheckpointManager("./demo_checkpoints")
    agent = ResumableAgent("worker_001", mgr)

    # 第一次运行（模拟在第3步崩溃）
    print("--- 第一次运行 ---")
    agent.task_id = "task_alpha"
    for step in range(1, 4):
        agent.state["step"] = step
        agent.state["results"].append(f"Step {step} result")
        mgr.save_checkpoint("worker_001", "task_alpha", step, agent.state)
        print(f"  [STEP {step}] 已保存checkpoint")

    print("\n--- 模拟崩溃后恢复 ---")
    # 重新创建agent（模拟重启）
    agent2 = ResumableAgent("worker_001", mgr)
    agent2.run_task("task_alpha", [], total_steps=5)

    # 列出所有检查点
    checkpoints = mgr.list_checkpoints("worker_001", "task_alpha")
    print(f"\n检查点列表:")
    for cp in checkpoints:
        print(f"  Step {cp['step']}: {cp['file']}")

    # 清理
    deleted = mgr.cleanup("worker_001", "task_alpha", keep_last=2)
    print(f"\n清理了 {deleted} 个旧检查点")

    import shutil
    shutil.rmtree("./demo_checkpoints", ignore_errors=True)


if __name__ == "__main__":
    demo()
