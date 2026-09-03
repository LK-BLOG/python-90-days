from dataclasses import dataclass

@dataclass
class Address:
    street: str
    city: str

@dataclass
class User:
    name: str
    age: int
    address: Address

u = User('Alice', 25, Address('中关村大街1号', '北京'))
print(u)
