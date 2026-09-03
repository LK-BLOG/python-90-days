"""Boss: ORM 模型基类 - 起手代码"""
# TODO: 实现完整的 ORM 模型基类
# 包含: 字段系统、验证、序列化、查询、JSON 持久化

class Field:
    pass

class Model:
    pass

class User(Model):
    name = None  # StringField(required=True)
    age = None   # IntegerField(min_val=0)
