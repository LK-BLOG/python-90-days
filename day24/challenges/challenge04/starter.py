"""
Challenge 04: 配置文件解析器 - ConfigFlow
"""
import os
import sys
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from copy import deepcopy


class ConfigDict(dict):
    """支持点号访问的字典"""
    
    def __getattr__(self, key: str) -> Any:
        """点号访问"""
        try:
            value = self[key]
            if isinstance(value, dict):
                return ConfigDict(value)
            return value
        except KeyError:
            raise AttributeError(f"配置项 '{key}' 不存在")
    
    def __setattr__(self, key: str, value: Any):
        """点号设置"""
        self[key] = value
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取配置值，支持默认值"""
        # TODO: 支持点号路径，如 "database.host"
        pass


class ConfigValidator:
    """配置验证器"""
    
    def __init__(self):
        self.rules = []
    
    def add_rule(self, path: str, rule_type: str, **kwargs):
        """添加验证规则
        
        path: 配置路径，如 "database.host"
        rule_type: 规则类型 (required, type, range, choices, custom)
        """
        # TODO: 实现
        pass
    
    def validate(self, config: ConfigDict) -> List[str]:
        """验证配置，返回错误列表"""
        # TODO: 实现
        pass


class Config:
    """配置管理器"""
    
    def __init__(
        self,
        config_file: str = None,
        env_prefix: str = "",
        defaults: Dict = None
    ):
        self.config_file = config_file
        self.env_prefix = env_prefix
        self.data = ConfigDict(defaults or {})
        self.validator = ConfigValidator()
        self._watchers = []
        
        if config_file:
            self.load_from_file(config_file)
        
        self.load_from_env()
    
    def load_from_file(self, filepath: str):
        """从文件加载配置"""
        path = Path(filepath)
        
        if not path.exists():
            raise FileNotFoundError(f"配置文件不存在: {filepath}")
        
        suffix = path.suffix.lower()
        
        if suffix == ".toml":
            self._load_toml(path)
        elif suffix == ".env":
            self._load_dotenv(path)
        elif suffix in (".yaml", ".yml"):
            self._load_yaml(path)
        elif suffix == ".json":
            self._load_json(path)
        else:
            raise ValueError(f"不支持的配置文件格式: {suffix}")
    
    def _load_toml(self, path: Path):
        """加载 TOML 配置"""
        try:
            import tomllib
        except ImportError:
            import tomli as tomllib
        
        with open(path, "rb") as f:
            data = tomllib.load(f)
        
        # TODO: 合并配置
        pass
    
    def _load_dotenv(self, path: Path):
        """加载 .env 文件"""
        # TODO: 解析 .env 格式
        # 格式: KEY=VALUE
        # 忽略注释和空行
        pass
    
    def _load_yaml(self, path: Path):
        """加载 YAML 配置"""
        # TODO: 使用 PyYAML
        pass
    
    def _load_json(self, path: Path):
        """加载 JSON 配置"""
        # TODO: 使用 json 模块
        pass
    
    def load_from_env(self):
        """从环境变量加载配置"""
        # TODO: 扫描所有环境变量
        # 匹配前缀，移除前缀后作为配置键
        # 支持双下划线作为层级分隔符
        # 例如: MYAPP_DATABASE__HOST -> database.host
        pass
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取配置值"""
        # TODO: 支持点号路径
        pass
    
    def set(self, key: str, value: Any):
        """设置配置值"""
        # TODO: 支持点号路径
        pass
    
    def validate(self, required: List[str] = None) -> List[str]:
        """验证配置"""
        # TODO: 使用 validator 验证
        pass
    
    def all(self) -> Dict:
        """返回所有配置"""
        return deepcopy(self.data)
    
    def watch(self, callback):
        """注册配置变更监听器"""
        self._watchers.append(callback)
    
    def notify(self, key: str, old_value: Any, new_value: Any):
        """通知配置变更"""
        for callback in self._watchers:
            callback(key, old_value, new_value)
    
    def reload(self):
        """重新加载配置"""
        # TODO: 实现热重载
        pass
    
    def __repr__(self):
        return f"Config({self.data})"


def load_dotenv(filepath: str = ".env", prefix: str = "") -> Dict[str, str]:
    """加载 .env 文件为字典"""
    # TODO: 实现
    pass


def main():
    """演示配置管理器"""
    # 创建默认配置
    defaults = {
        "app": {
            "name": "MyApp",
            "debug": False,
            "version": "1.0.0"
        },
        "database": {
            "host": "localhost",
            "port": 5432,
            "name": "mydb"
        }
    }
    
    config = Config(defaults=defaults)
    
    print("默认配置:")
    print(f"  app.name: {config.get('app.name')}")
    print(f"  database.host: {config.get('database.host')}")
    
    # 设置新配置
    config.set("app.debug", True)
    print(f"\n设置 debug=True 后:")
    print(f"  app.debug: {config.get('app.debug')}")


if __name__ == "__main__":
    main()
