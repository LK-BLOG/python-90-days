# 组合 vs 继承

# 继承：is-a
class Animal:
    def __init__(self, name):
        self.name = name
    def speak(self):
        raise NotImplementedError

class Dog(Animal):
    def speak(self):
        return '汪!'

class Cat(Animal):
    def speak(self):
        return '喵~'

# 组合：has-a
class Engine:
    def __init__(self, hp):
        self.hp = hp
    def start(self):
        return f'{self.hp}马力引擎启动'

class Car:
    def __init__(self, brand, engine):
        self.brand = brand
        self.engine = engine  # 组合

    def start(self):
        return f'{self.brand}: {self.engine.start()}'

car = Car('宝马', Engine(300))
print(car.start())

# 策略模式（组合的高级用法）
class Sorter:
    def __init__(self, strategy=None):
        self._strategy = strategy or sorted
    def sort(self, data):
        return self._strategy(data)

sorter = Sorter(lambda d: sorted(d, reverse=True))
print(sorter.sort([3, 1, 2]))  # [3, 2, 1]
