"""Challenge 4: 可调用对象"""
class Pipeline:
    """函数管道"""
    def __init__(self):
        self._funcs = []
    def add(self, func):
        # TODO: 添加函数到管道
        pass
    def __call__(self, value):
        # TODO: 依次执行所有函数
        pass
