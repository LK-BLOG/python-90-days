"""Challenge 3: 自定义容器"""
class Ring:
    """环形缓冲区"""
    def __init__(self, capacity):
        self._capacity = capacity
        self._data = []
    # TODO: __len__, __getitem__, __contains__, __iter__, __bool__
    def append(self, item): pass
