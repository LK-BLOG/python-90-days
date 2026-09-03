"""Challenge 4: 单例 + slots - 起手代码"""

class Config:
    __slots__ = ('db_host', 'db_port', 'db_name', 'debug')
    _instance = None

    def __new__(cls):
        # TODO: 单例模式
        pass

    def __init__(self):
        # TODO: 初始化默认值
        pass

    def update(self, **kwargs):
        # TODO: 更新配置
        pass

    def reset(self):
        # TODO: 重置为默认值
        pass
