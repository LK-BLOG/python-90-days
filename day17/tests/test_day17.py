from dataclasses import dataclass, field, asdict

def test_basic():
    @dataclass
    class P:
        x: int
        y: int
    assert P(1, 2) == P(1, 2)
    assert 'x=1' in str(P(1, 2))

def test_frozen():
    @dataclass(frozen=True)
    class C:
        r: int
    c = C(255)
    try:
        c.r = 0
        assert False
    except Exception:
        pass

def test_post_init():
    @dataclass
    class Circle:
        radius: float
        area: float = 0.0
        def __post_init__(self):
            self.area = 3.14 * self.radius ** 2
    assert abs(Circle(1).area - 3.14) < 0.01

def test_default_factory():
    @dataclass
    class Bag:
        items: list = field(default_factory=list)
    b1, b2 = Bag(), Bag()
    b1.items.append('x')
    assert len(b2.items) == 0

def test_asdict():
    @dataclass
    class User:
        name: str
        age: int
    d = asdict(User('Alice', 25))
    assert d == {'name': 'Alice', 'age': 25}

if __name__ == '__main__':
    test_basic()
    test_frozen()
    test_post_init()
    test_default_factory()
    test_asdict()
    print('All Day 17 tests passed!')
