class A:
    def show(self): return "A"
class B(A):
    def show(self): return "B->" + super().show()
class C(A):
    def show(self): return "C->" + super().show()
class D(B, C):
    def show(self): return "D->" + super().show()

print(D().show())  # D->B->C->A
print([c.__name__ for c in D.__mro__])
