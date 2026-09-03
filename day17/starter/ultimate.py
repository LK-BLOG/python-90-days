# Day 17 - Ultimate: dataclass 终极挑战
# 难度: ⭐⭐⭐⭐⭐
#
# 要求: 用 dataclass 设计一个完整的配置系统
# 参考 ultimate_challenge.md

"""
dataclass 终极挑战 — 用嵌套 dataclass 构建一个配置管理系统

功能:
- 层级配置（全局 + 环境 + 本地）
- 配置合并
- 配置验证
- JSON/TOML 序列化
"""

import json
from dataclasses import dataclass, field, asdict
from typing import Optional


@dataclass
class ServerConfig:
    """服务器配置"""
    host: str = "localhost"
    port: int = 8000
    workers: int = 4
    timeout: int = 30

    def __post_init__(self):
        if not 1 <= self.port <= 65535:
            raise ValueError(f"端口号无效: {self.port}")
        if self.workers < 1:
            raise ValueError("workers 不能小于 1")


@dataclass
class DatabaseConfig:
    """数据库配置"""
    engine: str = "sqlite"
    host: str = ""
    port: int = 0
    name: str = ""
    pool_size: int = 5
    echo: bool = False

    @property
    def url(self) -> str:
        if self.engine == "sqlite":
            return f"sqlite:///{self.name or ':memory:'}"
        return f"{self.engine}://{self.host}:{self.port}/{self.name}"


@dataclass
class LogConfig:
    """日志配置"""
    level: str = "INFO"
    file: str = ""
    format: str = "%(asctime)s [%(levelname)s] %(message)s"
    max_bytes: int = 10_000_000
    backup_count: int = 5


@dataclass
class AppConfig:
    """应用配置 — 嵌套所有子配置"""
    name: str = "my_app"
    version: str = "1.0.0"
    debug: bool = False
    server: ServerConfig = field(default_factory=ServerConfig)
    database: DatabaseConfig = field(default_factory=DatabaseConfig)
    logging: LogConfig = field(default_factory=LogConfig)

    def merge(self, other: "AppConfig") -> "AppConfig":
        """合并两个配置（other 覆盖 self 的值）

        Returns:
            合并后的新 AppConfig
        """
        # TODO: 递归合并
        pass

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(asdict(self), indent=indent, ensure_ascii=False)

    @classmethod
    def from_json(cls, json_str: str) -> "AppConfig":
        data = json.loads(json_str)
        # TODO: 递归构造嵌套 dataclass
        pass

    def validate(self) -> list[str]:
        """验证配置，返回错误信息列表"""
        errors = []
        # TODO: 验证各子配置
        return errors


# ---- 测试 ----
if __name__ == "__main__":
    print("=== dataclass 终极挑战 ===")

    cfg = AppConfig(
        name="prod",
        server=ServerConfig(port=9000, workers=8),
        database=DatabaseConfig(engine="postgres", host="db.local", port=5432, name="app"),
    )

    print(cfg.to_json()[:300])
    print(f"DB URL: {cfg.database.url}")
    print(f"验证: {cfg.validate()}")

    print("✅ Ultimate 完成")
