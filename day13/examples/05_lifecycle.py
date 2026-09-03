# 实例生命周期

class Lifecycle:
    def __new__(cls, name):
        print(f'1. __new__: 创建 {name}')
        return super().__new__(cls)

    def __init__(self, name):
        print(f'2. __init__: 初始化 {name}')
        self.name = name

    def __del__(self):
        print(f'3. __del__: 销毁 {self.name}')

obj = Lifecycle('测试')
print('4. 使用中...')
del obj
print('5. 结束')

# 单例模式
class Singleton:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            print('创建单例')
        return cls._instance

a, b = Singleton(), Singleton()
print(a is b)  # True
