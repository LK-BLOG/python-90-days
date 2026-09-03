"""缓存描述符"""
class Cached:
    def __init__(self, func):
        self.func = func
        self.attr_name = None

    def __set_name__(self, owner, name):
        self.attr_name = f'_cached_{name}'

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        if not hasattr(obj, self.attr_name):
            setattr(obj, self.attr_name, self.func(obj))
        return getattr(obj, self.attr_name)

class DataProcessor:
    def __init__(self, data):
        self.data = data

    @Cached
    def expensive_result(self):
        print('计算中...')
        return sum(x ** 2 for x in self.data)

p = DataProcessor(range(1000))
print(p.expensive_result)  # 计算中... 332833500
print(p.expensive_result)  # 332833500 (缓存)
