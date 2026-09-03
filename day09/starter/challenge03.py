# Day 9 挑战三：JSON 配置文件管理器 (★★★☆☆)
# 要求: 完整的 JSON 配置管理，支持嵌套、默认值、校验、备份。


import json
import os
import shutil
from pathlib import Path
from datetime import datetime


class JSONConfig:
    """JSON 配置文件管理器。
    
    特性:
        - 嵌套键读写 (dotted notation: "db.host")
        - 默认值
        - 自动备份
        - 变更追踪
        - 延迟写入
    """
    
    def __init__(self, filepath, defaults=None):
        self.filepath = Path(filepath)
        self._data = {}
        self._defaults = defaults or {}
        self._dirty = False
        self._history = []
        self._apply_defaults()
    
    def _apply_defaults(self):
        """将默认值应用到当前数据。"""
        # TODO: 递归合并默认值
        pass
    
    def get(self, dotted_key, default=None):
        """获取配置值（点号分隔键）。"""
        # TODO: 按 "." 拆分键，逐层访问
        pass
    
    def set(self, dotted_key, value):
        """设置配置值。"""
        # TODO: 按 "." 拆分键，逐层设置
        # TODO: 记录变更历史
        # TODO: 标记为 dirty
        pass
    
    def load(self):
        """从文件加载。"""
        # TODO: 处理文件不存在、JSON 解析错误
        pass
    
    def save(self):
        """保存到文件。"""
        # TODO: 如果 dirty 则写入
        pass
    
    def backup(self):
        """创建配置备份。"""
        # TODO: 复制为 .bak 文件
        pass
    
    def restore(self):
        """从备份恢复。"""
        pass
    
    def get_history(self):
        """返回变更历史。"""
        return list(self._history)
    
    def to_dict(self):
        """返回配置字典副本。"""
        return json.loads(json.dumps(self._data))
    
    def merge(self, other_dict):
        """深度合并另一个字典到当前配置。"""
        pass


# ===== 测试 =====
if __name__ == "__main__":
    cfg = JSONConfig("_test_cfg.json", defaults={
        "app": {"name": "MyApp", "version": "1.0"},
        "db": {"host": "localhost", "port": 3306},
    })
    cfg.set("db.port", 5432)
    cfg.set("db.name", "mydb")
    cfg.save()
    
    print(f"db.host: {cfg.get('db.host')}")
    print(f"db.port: {cfg.get('db.port')}")
    print(f"db.name: {cfg.get('db.name')}")
    print(f"history: {cfg.get_history()}")
    
    os.remove("_test_cfg.json")
