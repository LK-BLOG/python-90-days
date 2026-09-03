"""Challenge 4: 链式工厂方法"""
class User:
    def __init__(self, name, age, email):
        # TODO
        pass

    @classmethod
    def from_dict(cls, data):
        # TODO
        pass

    @classmethod
    def from_string(cls, s):
        # TODO: 解析 "name,age,email"
        pass

    @classmethod
    def batch_create(cls, users_list):
        # TODO: 批量创建
        pass
