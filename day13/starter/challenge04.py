# Day 13 - Challenge 4: 单例 + slots
# 难度: ⭐⭐⭐⭐☆
#
# 要求: 结合单例模式和 __slots__
# 参考 challenge.md

"""
单例 + slots 挑战 — 限制属性 + 保证唯一实例

核心知识点:
- __slots__: 限制实例只能有哪些属性，节省内存
- __new__: 控制实例创建，实现单例
- 两者结合的注意事项
"""


class Config:
    """配置单例类 — 使用 __slots__ 限制属性

    __slots__ 限制了实例只能有这些属性:
        db_host, db_port, db_name, debug, log_level

    使用 __new__ 保证全局只有一个实例。

    Example:
        >>> c1 = Config()
        >>> c1.db_host = 'localhost'
        >>> c2 = Config()
        >>> c1 is c2
        True
    """

    __slots__ = ("db_host", "db_port", "db_name", "debug", "log_level")

    _instance = None  # 单例实例

    # 默认配置
    _defaults = {
        "db_host": None,
        "db_port": 5432,
        "db_name": "default_db",
        "debug": False,
        "log_level": "INFO",
    }

    def __new__(cls, **kwargs):
        """创建或返回单例实例

        Args:
            **kwargs: 初始配置

        Returns:
            唯一的 Config 实例
        """
        # TODO: 如果 _instance 为 None，创建新实例
        # 否则直接返回 _instance
        # 用 kwargs 更新配置
        pass

    def update(self, **kwargs) -> None:
        """更新配置

        Args:
            **kwargs: 要更新的配置项

        Raises:
            AttributeError: 未知的配置项
        """
        # TODO: 遍历 kwargs，验证 key 在 __slots__ 中，然后 setattr
        pass

    def reset(self) -> None:
        """重置所有配置为默认值"""
        # TODO: 遍历 _defaults，setattr 每个属性
        pass

    def to_dict(self) -> dict:
        """导出配置为字典"""
        # TODO: 从 __slots__ 遍历，getattr 每个属性
        pass

    def __repr__(self) -> str:
        # TODO: 返回 Config(db_host='localhost', db_port=5432, ...)
        pass

    def __getitem__(self, key: str):
        """支持 dict 风格访问: config['db_host']"""
        # TODO: getattr(self, key)
        pass

    def __setitem__(self, key: str, value):
        """支持 dict 风格赋值: config['db_host'] = 'x'"""
        # TODO: setattr(self, key, value)
        pass


# ---- 测试 ----
if __name__ == "__main__":
    print("=== 单例 + slots 测试 ===")

    c1 = Config()
    c1.db_host = "localhost"
    c1.debug = True
    print(f"c1: {c1}")

    c2 = Config()
    print(f"c1 is c2: {c1 is c2}")  # True
    print(f"c2.db_host: {c2.db_host}")  # localhost

    # dict 风格访问
    print(f"config['debug']: {c2['debug']}")

    # 重置
    c2.reset()
    print(f"重置后 db_host: {c2.db_host}")  # None

    # 验证单例
    c3 = Config()
    assert c1 is c3 is c2

    print("✅ Challenge 04 完成")
