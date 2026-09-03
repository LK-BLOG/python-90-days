# Day 45 设计模式骨架 - TODO: 实现

# === TODO: 实现 Singleton ===
def singleton(cls):
    # TODO: 实现单例装饰器
    pass

@singleton
class Config:
    def __init__(self):
        self.debug = False

# === TODO: 实现 Observer ===
class EventEmitter:
    def __init__(self):
        # TODO
        pass
    def on(self, event, callback):
        # TODO
        pass
    def emit(self, event, *args, **kwargs):
        # TODO
        pass

# === TODO: 实现 Strategy ===
class SortStrategy:
    def sort(self, data):
        raise NotImplementedError

class BubbleSort(SortStrategy):
    def sort(self, data):
        # TODO
        pass

class QuickSort(SortStrategy):
    def sort(self, data):
        # TODO
        pass

class Sorter:
    def __init__(self, strategy):
        # TODO
        pass
    def sort(self, data):
        # TODO
        pass

# === TODO: 实现 Factory ===
class StorageFactory:
    @staticmethod
    def create(storage_type):
        # TODO: 根据类型创建不同存储
        pass

# === TODO: 实现 State ===
class OrderState:
    def next(self, order):
        raise NotImplementedError

class PendingState(OrderState):
    def next(self, order):
        # TODO
        pass
