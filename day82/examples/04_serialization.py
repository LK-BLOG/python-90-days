"""Day 82 Example 04: 状态序列化与版本迁移"""
import json
import time
from datetime import datetime
from typing import Dict, Any, Callable, Optional


class StateSerializer:
    """带版本迁移的状态序列化器"""

    CURRENT_VERSION = "2.0"

    def __init__(self):
        self.migrations: Dict[tuple, Callable] = {}
        self.type_handlers: Dict[str, Callable] = {}

        # 注册默认类型处理器
        self.register_type(datetime, lambda o: {"__type__": "datetime", "value": o.isoformat()})
        self.register_type(set, lambda o: {"__type__": "set", "value": list(o)})

    def register_migration(self, from_ver: str, to_ver: str, func: Callable):
        """注册版本迁移函数"""
        self.migrations[(from_ver, to_ver)] = func

    def register_type(self, cls, serializer: Callable):
        """注册自定义类型序列化"""
        self.type_handlers[cls.__name__] = serializer

    def _default_encoder(self, obj):
        """JSON自定义编码器"""
        for cls_name, handler in self.type_handlers.items():
            if type(obj).__name__ == cls_name or isinstance(obj, eval(cls_name)):
                return handler(obj)
        raise TypeError(f"无法序列化: {type(obj)}")

    def serialize(self, state: Dict[str, Any]) -> str:
        """序列化状态"""
        output = {
            "__version__": self.CURRENT_VERSION,
            "data": state,
            "serialized_at": datetime.now().isoformat()
        }
        return json.dumps(output, ensure_ascii=False, indent=2,
                         default=self._default_encoder)

    def deserialize(self, data: str) -> Dict[str, Any]:
        """反序列化状态，自动处理版本迁移"""
        parsed = json.loads(data, object_hook=self._type_hook)
        version = parsed.get("__version__", "0.1")

        # 逐级迁移
        max_iterations = 100
        iterations = 0
        while version != self.CURRENT_VERSION and iterations < max_iterations:
            migrated = False
            for (from_v, to_v), migrator in self.migrations.items():
                if from_v == version:
                    parsed["data"] = migrator(parsed["data"])
                    version = to_v
                    parsed[" "__version__"] = to_v
                    migrated = True
                    break
            if not migrated:
                raise ValueError(f"无可用的迁移路径: {version} -> {self.CURRENT_VERSION}")
            iterations += 1

        return parsed["data"]

    def _type_hook(self, obj):
        """反序列化自定义类型"""
        if "__type__" in obj:
            type_name = obj[" "__type__"]
            if type_name == "datetime":
                return datetime.fromisoformat(obj["value"])
            elif type_name == "set":
                return set(obj["value"])
        return obj


# 版本迁移函数
def migrate_v0_1_to_v1_0(data: Dict) -> Dict:
    """v0.1 -> v1.0: messages格式统一化"""
    if "messages" in data:
        new_msgs = []
        for m in data["messages"]:
            if isinstance(m, str):
                new_msgs.append({"role": "user", "content": m})
            else:
                new_msgs.append(m)
        data["messages"] = new_msgs
    data["metadata"] = {}
    return data


def migrate_v1_0_to_v2_0(data: Dict) -> Dict:
    """v1.0 -> v2.0: 增加trace和timing"""
    data["trace_id"] = ""
    data["timing"] = {"start": None, "end": None}
    if "metadata" not in data:
        data["metadata"] = {}
    return data


def demo():
    """演示序列化和版本迁移"""
    print("=== 状态序列化与版本迁移 ===\n")

    serializer = StateSerializer()
    serializer.register_migration("0.1", "1.0", migrate_v0_1_to_v1_0)
    serializer.register_migration("1.0", "2.0", migrate_v1_0_to_v2_0)

    # 序列化当前版本状态
    state = {
        "messages": [
            {"role": "user", "content": "你好"},
            {"role": "assistant", "content": "你好！"}
        ],
        "current_step": 3,
        "created_at": datetime.now(),
        "tags": {"important", "follow-up"}
    }

    serialized = serializer.serialize(state)
    print(f"序列化结果 (前200字符):\n{serialized[:200]}...\n")

    # 反序列化
    restored = serializer.deserialize(serialized)
    print(f"反序列化后类型检查:")
    print(f"  created_at: {type(restored['created_at'])}")
    print(f"  tags: {type(restored['tags'])} = {restored['tags']}")

    # 模拟旧版本数据迁移
    old_data = json.dumps({
        "__version__": "0.1",
        "data": {
            "messages": ["你好", "我很好"],
            "step": 1
        }
    })

    migrated = serializer.deserialize(old_data)
    print(f"\n旧版本迁移结果:")
    print(f"  messages: {migrated['messages']}")
    print(f"  新增字段 trace_id: {migrated.get('trace_id', 'N/A')}")


if __name__ == "__main__":
    demo()
