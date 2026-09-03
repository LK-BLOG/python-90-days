# Day 17 - Challenge 3: 嵌套结构
# 难度: ⭐⭐⭐⭐☆
#
# 要求: 设计嵌套的 dataclass
# 参考 challenge.md

"""
嵌套结构挑战 — 用 dataclass 表达复杂的嵌套数据

核心知识点:
- dataclass 嵌套
- field(default_factory) 避免可变默认值
- 复杂类型注解
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Address:
    """地址"""
    street: str = ""
    city: str = ""
    state: str = ""
    zip_code: str = ""
    country: str = "CN"

    def format(self) -> str:
        """格式化地址"""
        parts = [p for p in [self.street, self.city, self.state, self.zip_code] if p]
        return ", ".join(parts)


@dataclass
class ContactInfo:
    """联系方式"""
    email: str = ""
    phone: str = ""
    address: Address = field(default_factory=Address)


@dataclass
class Item:
    """商品"""
    name: str
    price: float
    quantity: int = 1

    @property
    def subtotal(self) -> float:
        return self.price * self.quantity


@dataclass
class Order:
    """订单 — 嵌套多层 dataclass

    结构:
        Order
        ├── customer_name: str
        ├── contact: ContactInfo
        │   ├── email, phone
        │   └── address: Address
        ├── items: list[Item]
        ├── status: str
        └── notes: str
    """
    customer_name: str
    contact: ContactInfo = field(default_factory=ContactInfo)
    items: list[Item] = field(default_factory=list)
    status: str = "pending"
    notes: str = ""

    @property
    def total(self) -> float:
        """订单总金额"""
        return sum(item.subtotal for item in self.items)

    @property
    def item_count(self) -> int:
        """商品总数"""
        return sum(item.quantity for item in self.items)

    def add_item(self, name: str, price: float, quantity: int = 1) -> None:
        """添加商品"""
        self.items.append(Item(name=name, price=price, quantity=quantity))

    def summary(self) -> str:
        """订单摘要"""
        # TODO: 返回多行摘要字符串
        pass

    def to_dict(self) -> dict:
        """手动序列化为字典"""
        # TODO: 递归转换嵌套 dataclass
        pass


# ---- 测试 ----
if __name__ == "__main__":
    print("=== 嵌套结构测试 ===")

    addr = Address(street="中关村大街1号", city="北京", state="北京", zip_code="100080")
    contact = ContactInfo(email="alice@example.com", phone="138****5678", address=addr)

    order = Order(customer_name="Alice", contact=contact)
    order.add_item("Python 编程", 59.9, 1)
    order.add_item("算法导论", 89.9, 2)

    print(f"订单总额: ¥{order.total:.2f}")
    print(f"商品数: {order.item_count}")
    print(f"收货地址: {order.contact.address.format()}")
    print(order.summary())

    print("✅ Challenge 03 完成")
