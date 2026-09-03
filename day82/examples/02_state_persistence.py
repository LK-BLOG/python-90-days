"""Day 82 Example 02: 文件状态持久化"""
import json
import os
import time
from typing import Dict, Any, Optional, List


class FileStateManager:
    """基于文件的Agent状态持久化管理器"""

    def __init__(self, storage_dir: str = "./agent_states"):
        self.storage_dir = storage_dir
        os.makedirs(storage_dir, exist_ok=True)

    def _get_path(self, agent_id: str) -> str:
        """获取agent状态文件路径"""
        # 防止路径注入
        safe_id = "".join(c for c in agent_id if c.isalnum() or c in "-_")
        return os.path.join(self.storage_dir, f"{safe_id}.json")

    def save(self, agent_id: str, state: Dict[str, Any]) -> str:
        """原子写入状态"""
        state["_meta"] = {
            "timestamp": time.time(),
            "version": "1.0",
            "agent_id": agent_id
        }
        filepath = self._get_path(agent_id)

        # 原子写入：先写临时文件，再重命名
        tmp_path = filepath + ".tmp"
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
        os.replace(tmp_path, filepath)
        return filepath

    def load(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """加载状态"""
        filepath = self._get_path(agent_id)
        if not os.path.exists(filepath):
            return None
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)

    def exists(self, agent_id: str) -> bool:
        """检查状态是否存在"""
        return os.path.exists(self._get_path(agent_id))

    def delete(self, agent_id: str) -> bool:
        """删除状态"""
        filepath = self._get_path(agent_id)
        if os.path.exists(filepath):
            os.remove(filepath)
            return True
        return False

    def list_agents(self) -> List[Dict[str, Any]]:
        """列出所有agent及其元数据"""
        agents = []
        for f in os.listdir(self.storage_dir):
            if not f.endswith(".json"):
                continue
            filepath = os.path.join(self.storage_dir, f)
            try:
                with open(filepath, "r", encoding="utf-8") as fp:
                    data = json.load(fp)
                    meta = data.get("_meta", {})
                    agents.append({
                        "agent_id": meta.get("agent_id", f[:-5]),
                        "timestamp": meta.get("timestamp", 0),
                        "version": meta.get("version", "unknown"),
                        "size_bytes": os.path.getsize(filepath)
                    })
            except (json.JSONDecodeError, KeyError):
                continue
        return sorted(agents, key=lambda x: x["timestamp"], reverse=True)

    def update_field(self, agent_id: str, field: str, value: Any):
        """更新单个字段"""
        state = self.load(agent_id)
        if state is None:
            raise KeyError(f"Agent {agent_id} 不存在")
        state[field] = value
        self.save(agent_id, state)


def demo():
    """演示文件状态持久化"""
    print("=== 文件状态持久化演示 ===\n")

    mgr = FileStateManager("./demo_states")

    # 保存agent状态
    agent_state = {
        "current_step": 3,
        "messages": [
            {"role": "user", "content": "你好"},
            {"role": "assistant", "content": "你好！有什么帮助？"},
            {"role": "user", "content": "解释Python装饰器"}
        ],
        "tool_calls": [],
        "context": {"session_start": time.time()}
    }

    filepath = mgr.save("agent_001", agent_state)
    print(f"已保存到: {filepath}")

    # 加载状态
    loaded = mgr.load("agent_001")
    print(f"加载状态: 当前步骤={loaded['current_step']}, 消息数={len(loaded['messages'])}")

    # 列出所有agent
    agents = mgr.list_agents()
    print(f"所有Agent: {agents}")

    # 更新字段
    mgr.update_field("agent_001", "current_step", 5)
    print(f"更新后步骤: {mgr.load('agent_001')['current_step']}")

    # 清理
    mgr.delete("agent_001")
    print(f"删除后存在: {mgr.exists('agent_001')}")

    # 清理演示目录
    import shutil
    shutil.rmtree("./demo_states", ignore_errors=True)


if __name__ == "__main__":
    demo()
