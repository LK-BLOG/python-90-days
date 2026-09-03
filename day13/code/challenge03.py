"""Challenge 3: 描述符验证 - 起手代码"""

class ValidatedField:
    """属性验证描述符"""
    def __init__(self, min_value=None, max_value=None, required=False, type_check=None):
        # TODO: 保存参数
        pass

    def __set_name__(self, owner, name):
        # TODO: 自动获取属性名
        pass

    def __get__(self, obj, objtype=None):
        # TODO: 返回属性值
        pass

    def __set__(self, obj, value):
        # TODO: 验证并设置值
        pass

class Product:
    name = None      # TODO: ValidatedField(required=True, type_check=str)
    price = None     # TODO: ValidatedField(min_value=0.01, type_check=float)
    stock = None     # TODO: ValidatedField(min_value=0, type_check=int)

    def __init__(self, name, price, stock):
        self.name = name
        self.price = price
        self.stock = stock
