"""向量运算符重载"""
class Vector:
    def __init__(self, *args):
        self.coords = list(args)
    @property
    def x(self): return self.coords[0]
    @property
    def y(self): return self.coords[1]
    def __add__(self, other):
        return Vector(*(a+b for a,b in zip(self.coords, other.coords)))
    def __sub__(self, other):
        return Vector(*(a-b for a,b in zip(self.coords, other.coords)))
    def __mul__(self, scalar):
        return Vector(*(a*scalar for a in self.coords))
    def __rmul__(self, scalar):
        return self * scalar
    def __abs__(self):
        return sum(a**2 for a in self.coords)**0.5
    def __eq__(self, other):
        return self.coords == other.coords
    def __repr__(self):
        return f'Vector({", ".join(str(c) for c in self.coords)})'
    def __getitem__(self, index):
        return self.coords[index]
    def __len__(self):
        return len(self.coords)
    def dot(self, other):
        return sum(a*b for a,b in zip(self.coords, other.coords))

v1, v2 = Vector(1, 2), Vector(3, 4)
print(v1 + v2)         # Vector(4, 6)
print(v1 * 3)          # Vector(3, 6)
print(abs(v1))         # 2.236...
print(v1.dot(v2))      # 11
print(v1[0], v1[1])    # 1 2
