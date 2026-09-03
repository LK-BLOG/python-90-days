"""Boss: 向量/矩阵类"""
class Vector:
    def __init__(self, *args):
        self.coords = list(args)
    # TODO: 完整实现
    # 支持: +, -, *, /, abs, len, getitem, eq, lt, repr, format, callable

class Matrix:
    def __init__(self, data):
        self.data = data
    # TODO: +, *, @, transpose, determinant
