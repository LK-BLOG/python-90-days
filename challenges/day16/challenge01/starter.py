"""Challenge 1: 美观输出"""
class Color:
    def __init__(self, r, g, b):
        self.r, self.g, self.b = r, g, b

    def __repr__(self):
        # TODO: 返回可重建的表示
        pass

    def __str__(self):
        # TODO: 返回友好显示
        pass

    def __format__(self, fmt):
        # TODO: 支持 hex 格式
        pass
