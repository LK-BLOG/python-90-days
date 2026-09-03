# Day 15 - Challenge 4: 链式工厂方法
# 难度: ⭐⭐⭐⭐☆
#
# 要求: 多种方式创建实例
# 参考 challenge.md

"""
链式工厂方法挑战 — 学习多种实例创建模式

工厂方法模式:
- 类方法工厂
- Builder 模式
- 参数化工厂
"""

from dataclasses import dataclass


@dataclass
class DatabaseConfig:
    """数据库配置"""
    host: str = "localhost"
    port: int = 3306
    database: str = ""
    username: str = ""
    password: str = ""
    charset: str = "utf8mb4"
    pool_size: int = 5
    timeout: int = 30
    ssl: bool = False
    options: dict = None

    def __post_init__(self):
        if self.options is None:
            self.options = {}

    # ===== 工厂方法 =====

    @classmethod
    def from_url(cls, url: str) -> "DatabaseConfig":
        """从连接 URL 创建

        格式: mysql://user:pass@host:port/dbname?charset=utf8

        Args:
            url: 数据库连接 URL

        Raises:
            ValueError: URL 格式不正确
        """
        # TODO: 解析 URL -> 提取各部分 -> 构造 Config
        pass

    @classmethod
    def from_dict(cls, data: dict) -> "DatabaseConfig":
        """从字典创建"""
        # TODO: cls(**data)
        pass

    @classmethod
    def sqlite(cls, path: str = ":memory:") -> "DatabaseConfig":
        """快速创建 SQLite 配置"""
        return cls(host="localhost", port=0, database=path, username="", password="")

    @classmethod
    def postgres(cls, host: str, db: str, user: str, password: str) -> "DatabaseConfig":
        """快速创建 PostgreSQL 配置"""
        return cls(host=host, port=5432, database=db,
                   username=user, password=password, charset="utf8")

    # ===== Builder 模式 =====

    def set_host(self, host: str) -> "DatabaseConfig":
        """链式设置 host"""
        self.host = host
        return self

    def set_port(self, port: int) -> "DatabaseConfig":
        self.port = port
        return self

    def set_database(self, db: str) -> "DatabaseConfig":
        self.database = db
        return self

    def set_auth(self, username: str, password: str) -> "DatabaseConfig":
        self.username = username
        self.password = password
        return self

    def set_pool(self, size: int) -> "DatabaseConfig":
        self.pool_size = size
        return self

    def enable_ssl(self) -> "DatabaseConfig":
        self.ssl = True
        return self

    def build(self) -> "DatabaseConfig":
        """完成构建"""
        # TODO: 验证必要字段 -> 返回自身
        pass

    def to_url(self) -> str:
        """转换为 URL 字符串"""
        # TODO: mysql://user:pass@host:port/db
        pass

    def __repr__(self) -> str:
        return (f"DatabaseConfig(host={self.host}, port={self.port}, "
                f"db={self.database})")


# ---- 测试 ----
if __name__ == "__main__":
    print("=== 链式工厂方法测试 ===")

    # 默认
    c1 = DatabaseConfig()
    print(f"默认: {c1}")

    # 工厂方法
    c2 = DatabaseConfig.postgres("db.example.com", "mydb", "admin", "secret")
    print(f"PostgreSQL: {c2}")

    c3 = DatabaseConfig.sqlite("app.db")
    print(f"SQLite: {c3}")

    # Builder 链式
    c4 = (DatabaseConfig()
          .set_host("10.0.0.1")
          .set_port(5432)
          .set_database("prod")
          .set_auth("root", "pass")
          .set_pool(20)
          .enable_ssl()
          .build())
    print(f"Builder: {c4}")

    print("✅ Challenge 04 完成")
