"""Challenge 2: 数据验证描述符"""
class Validated:
    def __init__(self, field_type=None, min_val=None, max_val=None, required=False):
        # TODO
        pass
    def __set_name__(self, owner, name):
        pass
    def __get__(self, obj, objtype=None):
        pass
    def __set__(self, obj, value):
        # TODO: 验证类型、范围、必填
        pass

class Product:
    name = None  # TODO: Validated(str, required=True)
    price = None  # TODO: Validated(float, min_val=0.01)
    stock = None  # TODO: Validated(int, min_val=0)
