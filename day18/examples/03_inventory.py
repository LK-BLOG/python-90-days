"""背包系统"""
class Inventory:
    def __init__(self, capacity=20):
        self._items = []
        self._capacity = capacity

    def __len__(self): return len(self._items)
    def __bool__(self): return len(self._items) > 0
    def __contains__(self, item): return item in self._items
    def __getitem__(self, index): return self._items[index]
    def __iter__(self): return iter(self._items)

    def add(self, item):
        if len(self._items) >= self._capacity:
            raise ValueError('背包已满')
        self._items.append(item)

    def remove(self, item):
        self._items.remove(item)

    def get_by_type(self, item_type):
        from day18.examples.items import ItemType
        return [i for i in self._items if i.item_type == item_type]
