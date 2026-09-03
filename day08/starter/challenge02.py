# Day 8 挑战二：配置文件管理器 (★★★☆☆)
# 要求: 读写配置文件，支持嵌套和默认值。


import json
import os


class ConfigManager:
    """配置文件管理器。
    
    支持:
        - JSON 配置文件读写
        - 嵌套键访问 (db.host)
        - 默认值
        - 配置验证
    """
    
    def __init__(self, filepath, defaults=None):
        """初始化。
        
        Args:
            filepath: 配置文件路径
            defaults: 默认配置字典
        """
        self.filepath = filepath
        self._config = dict(defaults) if defaults else {}
        self._original = {}  # 保存原始值用于回滚
    
    def get(self, key, default=None):
        """获取配置值（支持点号分隔的嵌套键）。
        
        示例:
            config.get("db.host", "localhost")
        """
        # TODO: 解析点号分隔的键，逐层访问
        pass
    
    def set(self, key, value):
        """设置配置值（支持点号分隔的嵌套键）。"""
        pass
    
    def delete(self, key):
        """删除配置项。"""
        pass
    
    def has(self, key):
        """检查键是否存在。"""
        pass
    
    def load(self):
        """从文件加载配置。"""
        # TODO: 处理文件不存在（使用默认值）
        # TODO: 处理 JSON 解析错误
        pass
    
    def save(self, indent=2):
        """保存配置到文件。"""
        # TODO: 写入 JSON 文件
        pass
    
    def reset(self):
        """恢复到原始值。"""
        self._config = dict(self._original)
    
    def to_dict(self):
        """返回配置字典的副本。"""
        return dict(self._config)
    
    def update(self, other_dict):
        """批量更新配置。"""
        # TODO: 递归合并
        pass


# ===== 测试 =====
if __name__ == "__main__":
    cfg = ConfigManager("_test_config.json", defaults={
        "db": {"host": "localhost", "port": 3306},
        "debug": False,
        "log_level": "INFO"
    })
    cfg.set("db.port", 5432)
    cfg.set("debug", True)
    cfg.save()
    
    cfg2 = ConfigManager("_test_config.json")
    cfg2.load()
    print(f"db.host: {cfg2.get('db.host')}")
    print(f"db.port: {cfg2.get('db.port')}")
    print(f"debug: {cfg2.get('debug')}")
    os.remove("_test_config.json")
