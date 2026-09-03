"""Challenge 2: 方法类型大练习 - 起手代码"""
# TODO: 完成 Temperature 类

class Temperature:
    def __init__(self, celsius):
        # TODO
        pass

    def to_fahrenheit(self):
        # TODO: C -> F 公式: F = C * 9/5 + 32
        pass

    @classmethod
    def from_fahrenheit(cls, f):
        # TODO: 从华氏创建实例
        pass

    @classmethod
    def from_string(cls, s):
        # TODO: 解析 "36.5C" 或 "97.7F"
        pass

    @staticmethod
    def is_freezing(celsius):
        # TODO: 判断是否 < 0
        pass
