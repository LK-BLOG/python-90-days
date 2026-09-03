\"\"\"Day 47 Starter: DI练习起点\"\"\"

from abc import ABC, abstractmethod


class Database(ABC):
    @abstractmethod
    def connect(self) -> None: ...
    @abstractmethod
    def query(self, sql: str) -> list: ...
    @abstractmethod
    def close(self) -> None: ...


class MySQLDatabase(Database):
    def connect(self): print(\"MySQL connected\")
    def query(self, sql: str) -> list: return []
    def close(self): print(\"MySQL closed\")


class PostgresDatabase(Database):
    def connect(self): print(\"Postgres connected\")
    def query(self, sql: str) -> list: return []
    def close(self): print(\"Postgres closed\")


# TODO: 实现DI容器
# TODO: 通过配置驱动选择数据库实现
# TODO: 写测试验证可替换
