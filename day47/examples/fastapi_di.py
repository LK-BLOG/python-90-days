\"\"\"FastAPI中的DI集成\"\"\"

from typing import AsyncGenerator
from dataclasses import dataclass, field


# 模拟依赖
@dataclass
class Database:
    url: str = \"\"
    _connected: bool = False

    async def connect(self):
        self._connected = True
        print(f\"Connected to {self.url}\")

    async def close(self):
        self._connected = False
        print(\"Disconnected\")

    async def fetch_all(self, table: str) -> list[dict]:
        return [{\"id\": 1, \"name\": \"Alice\"}]


@dataclass
class Cache:
    host: str = \"localhost\"
    _store: dict = field(default_factory=dict)

    def get(self, key: str):
        return self._store.get(key)

    def set(self, key: str, value):
        self._store[key] = value


# 模拟FastAPI的Depends
class Depends:
    def __init__(self, dependency):
        self.dependency = dependency

# 简化版DI演示
async def get_db() -> AsyncGenerator[Database, None]:
    db = Database(url=\"postgresql://localhost/blog\")
    await db.connect()
    try:
        yield db
    finally:
        await db.close()


async def get_cache() -> Cache:
    return Cache(host=\"localhost\")


async def get_user_service(db=None, cache=None):
    return UserService(db=db, cache=cache)


@dataclass
class UserService:
    db: Database | None = None
    cache: Cache | None = None

    async def get_user(self, user_id: int) -> dict | None:
        # 先查缓存
        if self.cache:
            cached = self.cache.get(f\"user:{user_id}\")
            if cached:
                return cached

        # 再查数据库
        if self.db:
            users = await self.db.fetch_all(\"users\")
            user = next((u for u in users if u[\"id\"] == user_id), None)
            if user and self.cache:
                self.cache.set(f\"user:{user_id}\", user)
            return user
        return None


async def demo():
    \"\"\"模拟FastAPI的DI流程\"\"\"
    async for db in get_db():
        cache = get_cache()
        service = await get_user_service(db=db, cache=cache)

        user = await service.get_user(1)
        print(f\"User: {user}\")

        # 第二次从缓存获取
        user2 = await service.get_user(1)
        print(f\"Cached: {user2}\")


if __name__ == \"__main__\":
    import asyncio
    asyncio.run(demo())
