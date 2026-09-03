"""Challenge 5: 组合 vs 继承 - 起手代码"""

class Logger:
    """Mixin: 日志功能"""
    def log(self, msg):
        # TODO: 打印带类名前缀的日志
        pass

class Serializable:
    """Mixin: 序列化功能"""
    def to_dict(self):
        # TODO: 返回实例属性字典
        pass

class Database(Logger, Serializable):
    """数据库基类"""
    def __init__(self, host, port):
        # TODO
        pass

    def connect(self):
        # TODO
        pass

    def disconnect(self):
        # TODO
        pass

    def query(self, 文本模板):
        # TODO
        pass

class My文本模板(Database):
    def __init__(self, host='localhost', port=3306):
        super().__init__(host, port)

class Postgre文本模板(Database):
    def __init__(self, host='localhost', port=5432):
        super().__init__(host, port)
