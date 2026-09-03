"""Challenge 3: 缓存描述符"""
class Cached:
    def __init__(self, func):
        # TODO
        pass
    def __set_name__(self, owner, name):
        pass
    def __get__(self, obj, objtype=None):
        # TODO: 检查缓存，没有则计算
        pass

class DataProcessor:
    def __init__(self, data):
        self.data = data

    @Cached
    def expensive_result(self):
        print('计算中...')
        return sum(x**2 for x in self.data)
