# Day 24 - Challenge 4: 配置文件解析器
# 难度: ⭐⭐⭐
# 支持 pyproject.toml / .env / 环境变量，带优先级和验证

import os
import re
from pathlib import Path
from dataclasses import dataclass, field
from typing import Any, get_type_hints


class ConfigError(Exception):
    """配置错误基类"""
    pass


class MissingRequiredConfig(ConfigError):
    """缺少必填配置项"""
    pass


class InvalidConfigType(ConfigError):
    """配置类型不匹配"""
    pass


@dataclass
class ConfigField:
    """配置字段描述"""
    name: str
    type_: type
    default: Any = None
    required: bool = False
    description: str = ""


class ConfigManager:
    """配置管理器

    优先级: 环境变量 > .env > pyproject.toml > 默认值
    支持配置验证（类型检查、必填字段）。
    """

    def __init__(self, project_root: str = "."):
        """初始化配置管理器

        Args:
            project_root: 项目根目录路径
        """
        self.project_root = Path(project_root)
        # TODO: 初始化各层配置存储
        self._defaults: dict[str, Any] = {}
        self._env_file: dict[str, Any] = {}
        self._pyproject: dict[str, Any] = {}
        self._fields: dict[str, ConfigField] = {}

    def register_field(self, name: str, type_: type, default: Any = None,
                       required: bool = False, description: str = "") -> None:
        """注册一个配置字段

        Args:
            name: 字段名
            type_: 期望类型
            default: 默认值
            required: 是否必填
            description: 字段描述
        """
        # TODO: 创建 ConfigField 并注册到 _fields
        ...

    def load_pyproject(self) -> dict[str, Any]:
        """从 pyproject.toml 读取 [tool.myproject] 配置

        Returns:
            解析后的配置字典
        """
        # TODO: 读取 pyproject.toml，提取 [tool.X] 节
        ...

    def load_env_file(self, env_path: str = ".env") -> dict[str, Any]:
        """从 .env 文件读取环境变量

        Args:
            env_path: .env 文件路径

        Returns:
            解析后的键值对
        """
        # TODO: 逐行解析 KEY=VALUE 格式
        # 处理注释行、空行、带引号的值
        ...

    def get(self, key: str) -> Any:
        """获取配置值（按优先级查找）

        Args:
            key: 配置键名

        Returns:
            配置值

        Raises:
            MissingRequiredConfig: 必填字段缺失
        """
        # TODO: 按优先级查找：环境变量 > .env > pyproject > 默认值
        ...

    def validate(self) -> list[str]:
        """验证所有已注册的配置字段

        Returns:
            错误信息列表，空列表表示全部通过
        """
        # TODO: 检查必填字段、类型匹配
        ...

    def to_dict(self) -> dict[str, Any]:
        """导出所有配置为字典"""
        # TODO: 返回合并后的完整配置
        ...


# ==================== 测试 ====================
if __name__ == "__main__":
    cm = ConfigManager()
    cm.register_field("database_url", str, required=True, description="数据库连接URL")
    cm.register_field("debug", bool, default=False, description="调试模式")
    cm.register_field("port", int, default=8000, description="服务端口")

    errors = cm.validate()
    if errors:
        print("配置验证失败:")
        for e in errors:
            print(f"  - {e}")
    else:
        print("配置验证通过")
