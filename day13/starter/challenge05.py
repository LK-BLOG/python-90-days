# Day 13 - Challenge 5: 组合 vs 继承
# 难度: ⭐⭐⭐⭐☆
#
# 要求: 用组合+继承设计灵活的数据库系统
# 参考 challenge.md

"""
组合 vs 继承挑战 — 学会在合适场景选择组合或继承

设计原则:
- Mixin 用多重继承注入功能
- 组合用于 "has-a" 关系
- 继承用于 "is-a" 关系
"""


# ===== Mixin 类 =====

class LoggerMixin:
    """日志 Mixin — 提供 log 方法

    继承此类的类自动拥有日志功能。
    """

    def log(self, msg: str) -> None:
        """打印日志

        Args:
            msg: 日志消息
        """
        # TODO: 打印 [类名] msg 格式的日志
        # 提示: type(self).__name__ 获取类名
        pass


class SerializableMixin:
    """序列化 Mixin — 提供 to_dict 方法"""

    def to_dict(self) -> dict:
        """将对象转换为字典

        Returns:
            包含对象所有属性的字典

        Hint:
            遍历 self.__dict__，处理不可序列化的值
        """
        # TODO: 递归将 __dict__ 转为可序列化的字典
        pass

    def from_dict(cls, data: dict):
        """从字典恢复（类方法）"""
        pass


# ===== 组合组件 =====

class ConnectionPool:
    """数据库连接池（组合用）"""

    def __init__(self, max_connections: int = 5):
        # TODO: 初始化连接池
        pass

    def get_connection(self) -> str:
        """获取一个连接（模拟）"""
        return "connection"

    def release_connection(self, conn: str) -> None:
        """释放连接"""
        pass


# ===== 基类 =====

class Database(LoggerMixin, SerializableMixin):
    """数据库基类 — 使用组合包含 Logger 和 Serializable

    组合: Database "has-a" ConnectionPool
    继承: Database "is-a" LoggerMixin, SerializableMixin
    """

    def __init__(self, host: str, port: int, max_connections: int = 5):
        # TODO: 初始化 host, port
        # TODO: 组合创建 ConnectionPool
        pass

    def connect(self) -> bool:
        """连接数据库"""
        # TODO: 打印连接信息，调用 pool.get_connection()
        self.log(f"Connecting to {self.host}:{self.port}")
        return True

    def disconnect(self) -> None:
        """断开连接"""
        # TODO: 调用 pool.release_connection()
        self.log(f"Disconnected from {self.host}:{self.port}")

    def query(self, sql: str) -> list[dict]:
        """执行查询（模拟）

        Args:
            sql: SQL 语句

        Returns:
            模拟的查询结果
        """
        self.log(f"Executing: {sql}")
        # TODO: 返回模拟数据
        return [{"result": "mock_data"}]

    def __repr__(self) -> str:
        return f"{type(self).__name__}(host={self.host!r}, port={self.port})"


# ===== 具体实现 =====

class MySQL(Database):
    """MySQL 数据库"""

    def __init__(self, host: str, port: int = 3306, **kwargs):
        # TODO: 调用父类 __init__，设置默认端口
        pass

    def connect(self) -> bool:
        self.log("MySQL driver loaded")
        return super().connect()


class PostgreSQL(Database):
    """PostgreSQL 数据库"""

    def __init__(self, host: str, port: int = 5432, **kwargs):
        # TODO: 调用父类 __init__
        pass

    def connect(self) -> bool:
        self.log("psycopg2 driver loaded")
        return super().connect()


# ---- 测试 ----
if __name__ == "__main__":
    print("=== 组合 vs 继承测试 ===")

    db = MySQL(host="localhost", port=3306)
    db.connect()
    db.log("Connected!")  # [MySQL] Connected!
    result = db.query("SELECT * FROM users")
    print(f"查询结果: {result}")
    print(f"序列化: {db.to_dict()}")
    db.disconnect()

    print(f"\nPostgreSQL:")
    pg = PostgreSQL(host="pg.example.com")
    pg.connect()
    pg.disconnect()

    print("✅ Challenge 05 完成")
