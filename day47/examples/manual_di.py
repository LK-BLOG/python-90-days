\"\"\"手动DI容器实现\"\"\"

from typing import Any, Callable, TypeVar

T = TypeVar("T")


class Container:
    \"\"\"简易依赖注入容器\"\"\"

    def __init__(self):
        self._bindings: dict[str, tuple[Callable, bool]] = {}
        self._singletons: dict[str, Any] = {}

    def bind(self, interface: str, factory: Callable) -> None:
        \"\"\"注册一个工厂函数\"\"\"
        self._bindings[interface] = (factory, False)

    def singleton(self, interface: str, factory: Callable) -> None:
        \"\"\"注册一个单例\"\"\"
        self._bindings[interface] = (factory, True)

    def resolve(self, interface: str) -> Any:
        \"\"\"解析依赖\"\"\"
        if interface not in self._bindings:
            raise KeyError(f\"No binding for '{interface}'\")

        factory, is_singleton = self._bindings[interface]

        if is_singleton:
            if interface not in self._singletons:
                self._singletons[interface] = factory()
            return self._singletons[interface]

        return factory()

    def has(self, interface: str) -> bool:
        return interface in self._bindings

    def reset(self) -> None:
        self._bindings.clear()
        self._singletons.clear()


# 示例：模拟数据库和缓存
class MockDatabase:
    def __init__(self, url: str = \"\"):
        self.url = url
        self.connected = True

    def query(self, sql: str) -> list:
        return [{\"id\": 1, \"name\": \"test\"}]

    def close(self):
        self.connected = False


class MockCache:
    def __init__(self, host: str = \"localhost\", port: int = 6379):
        self.host = host
        self.port = port
        self._store: dict = {}

    def get(self, key: str) -> Any:
        return self._store.get(key)

    def set(self, key: str, value: Any) -> None:
        self._store[key] = value


if __name__ == \"__main__\":
    container = Container()

    # 注册依赖
    container.singleton(\"database\", lambda: MockDatabase(\"postgresql://localhost/test\"))
    container.singleton(\"cache\", lambda: MockCache(\"localhost\", 6379))

    # 解析
    db = container.resolve(\"database\")
    cache = container.resolve(\"cache\")

    # 验证单例
    assert db is container.resolve(\"database\")
    assert cache is container.resolve(\"cache\")

    print(f\"DB: {db.url}, Connected: {db.connected}\")
    print(f\"Cache: {cache.host}:{cache.port}\")

    # 使用
    results = db.query(\"SELECT * FROM users\")
    cache.set(\"users\", results)
    print(f\"Cached users: {cache.get('users')}\")
