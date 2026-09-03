"""Challenge 5: ORM字段系统"""
class Field:
    def __init__(self, field_type, required=False, default=None):
        # TODO
        pass
    def __set_name__(self, owner, name):
        pass
    def __get__(self, obj, objtype=None):
        pass
    def __set__(self, obj, value):
        # TODO: 类型检查、必填验证
        pass

class UserModel:
    name = None  # TODO: Field(str, required=True)
    age = None   # TODO: Field(int, min_val=0)
    email = None # TODO: Field(str, required=True)
