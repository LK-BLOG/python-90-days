\"\"\"依赖倒置原则示例\"\"\"

from abc import ABC, abstractmethod
from dataclasses import dataclass, field


# ===== 违反DIP =====
class MySQLDatabaseBad:
    def save(self, table: str, data: dict) -> None:
        print(f\"MySQL: INSERT INTO {table} {data}\")

    def query(self, table: str, conditions: dict) -> list:
        print(f\"MySQL: SELECT * FROM {table}\")
        return []


class UserServiceBad:
    def __init__(self):
        self.db = MySQLDatabaseBad()  # 直接依赖具体实现！

    def save_user(self, name: str, email: str) -> None:
        self.db.save(\"users\", {\"name\": name, \"email\": email})


# ===== 遵循DIP =====
class Database(ABC):
    \"\"\"数据库抽象\"\"\"

    @abstractmethod
    def save(self, table: str, data: dict) -> None: ...

    @abstractmethod
    def query(self, table: str, conditions: dict | None = None) -> list[dict]: ...


class MySQLDatabase(Database):
    def save(self, table: str, data: dict) -> None:
        print(f\"MySQL: INSERT INTO {table} {data}\")

    def query(self, table: str, conditions: dict | None = None) -> list[dict]:
        print(f\"MySQL: SELECT * FROM {table}\")
        return []


class PostgresDatabase(Database):
    def save(self, table: str, data: dict) -> None:
        print(f\"PostgreSQL: INSERT INTO {table} {data}\")

    def query(self, table: str, conditions: dict | None = None) -> list[dict]:
        print(f\"PostgreSQL: SELECT * FROM {table}\")
        return []


class InMemoryDatabase(Database):
    \"\"\"用于测试的内存数据库\"\"\"

    def __init__(self):
        self._store: dict[str, list[dict]] = {}

    def save(self, table: str, data: dict) -> None:
        self._store.setdefault(table, []).append(data)
        print(f\"InMemory: saved to {table}\")

    def query(self, table: str, conditions: dict | None = None) -> list[dict]:
        rows = self._store.get(table, [])
        if conditions:
            rows = [r for r in rows if all(r.get(k) == v for k, v in conditions.items())]
        return rows


class UserService:
    \"\"\"依赖抽象，不依赖具体实现\"\"\"

    def __init__(self, db: Database):
        self.db = db

    def save_user(self, name: str, email: str) -> None:
        self.db.save(\"users\", {\"name\": name, \"email\": email})

    def get_all_users(self) -> list[dict]:
        return self.db.query(\"users\")


if __name__ == \"__main__\":
    # 可以自由切换数据库实现
    for label, db in [
        (\"MySQL\", MySQLDatabase()),
        (\"PostgreSQL\", PostgresDatabase()),
        (\"InMemory\", InMemoryDatabase()),
    ]:
        print(f\"\\n=== Using {label} ===\")
        service = UserService(db)
        service.save_user(\"Alice\", \"alice@example.com\")
        users = service.get_all_users()
        print(f\"Users: {users}\")
