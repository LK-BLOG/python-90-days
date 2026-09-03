"""Day 16 测试"""
def test_repr_str():
    class P:
        def __init__(self, x, y): self.x, self.y = x, y
        def __repr__(self): return f'P({self.x},{self.y})'
        def __str__(self): return f'({self.x},{self.y})'
    p = P(1, 2)
    assert repr(p) == 'P(1,2)'
    assert str(p) == '(1,2)'

def test_comparison():
    class Temp:
        def __init__(self, c): self.c = c
        def __eq__(self, o): return self.c == o.c
        def __lt__(self, o): return self.c < o.c
    assert Temp(10) < Temp(20)
    assert not Temp(10) > Temp(20)
    assert Temp(10) == Temp(10)

def test_container():
    class Bag:
        def __init__(self): self._items = []
        def __len__(self): return len(self._items)
        def __contains__(self, i): return i in self._items
        def __getitem__(self, i): return self._items[i]
        def add(self, i): self._items.append(i)
    b = Bag()
    b.add('x')
    b.add('y')
    assert len(b) == 2
    assert 'x' in b

def test_callable():
    class Adder:
        def __init__(self, n): self.n = n
        def __call__(self, x): return x + self.n
    add5 = Adder(5)
    assert add5(3) == 8

if __name__ == '__main__':
    test_repr_str()
    test_comparison()
    test_container()
    test_callable()
    print('All Day 16 tests passed!')
