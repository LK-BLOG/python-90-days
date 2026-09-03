class A:
    def greet(self): return "A"
class B(A):
    def greet(self): return "B(" + super().greet() + ")"
class C(A):
    def greet(self): return "C(" + super().greet() + ")"
class D(B, C):
    def greet(self): return "D(" + super().greet() + ")"

print(D().greet())  # D(B(C(A)))
print([c.__name__ for c in D.__mro__])
