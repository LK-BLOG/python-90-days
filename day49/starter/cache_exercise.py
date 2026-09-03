\"\"\"Day 49 Starter: 缓存练习\"\"\"

# TODO: 实现以下缓存类

class MemoryCache:
    \"\"\"支持TTL和LRU的内存缓存\"\"\"

    def __init__(self, maxsize: int = 128, default_ttl: int = 300):
        pass

    def get(self, key: str):
        pass

    def set(self, key: str, value, ttl: int | None = None):
        pass

    def delete(self, key: str):
        pass

    def cache_info(self):
        pass


# TODO: 实现多级缓存
class MultiLevelCache:
    def __init__(self, l1, l2):
        pass

    def get(self, key: str):
        pass

    def set(self, key: str, value, l1_ttl=60, l2_ttl=3600):
        pass

    def delete(self, key: str):
        pass
