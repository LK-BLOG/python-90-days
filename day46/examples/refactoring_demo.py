\"\"\"完整反模式识别与重构演示\"\"\"

# ===== 反SOLID的遗留代码 =====

class GodOrderSystemBad:
    \"\"\"
    反模式集合：
    - God Object (SRP违反): 一个类干所有事
    - Switch链 (OCP违反): 新增支付方式要改代码
    - 基本类型偏执: 用字符串代表支付类型
    - Feature Envy: 频繁访问其他类的数据
    \"\"\"

    def create_order(self, customer_name: str, items: list[dict], payment_type: str) -> dict:
        # SRP违反：订单创建逻辑
        order = {
            \"customer\": customer_name,
            \"items\": items,
            \"total\": sum(i[\"price\"] * i[\"qty\"] for i in items),
        }

        # OCP违反：switch链
        if payment_type == \"credit_card\":
            print(f\"Processing credit card: \\")
        elif payment_type == \"paypal\":
            print(f\"Processing PayPal: \\")
        elif payment_type == \"crypto\":
            print(f\"Processing crypto: \\")
        else:
            raise ValueError(f\"Unknown payment: {payment_type}\")

        # SRP违反：邮件通知
        print(f\"Sending confirmation to {customer_name}\")

        # SRP违反：库存更新
        for item in items:
            print(f\"Updating stock for {item['name']}\")

        return order


# ===== 重构后的代码 =====
from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class OrderItem:
    name: str
    price: float
    quantity: int

    @property
    def subtotal(self) -> float:
        return self.price * self.quantity


@dataclass
class Order:
    customer: str
    items: list[OrderItem]
    payment_method: str = \"\"

    @property
    def total(self) -> float:
        return sum(item.subtotal for item in self.items)


class PaymentProcessor(ABC):
    @abstractmethod
    def process(self, amount: float) -> bool: ...


class CreditCardPayment(PaymentProcessor):
    def process(self, amount: float) -> bool:
        print(f\"Credit card: charged \\")
        return True


class PayPalPayment(PaymentProcessor):
    def process(self, amount: float) -> bool:
        print(f\"PayPal: charged \\")
        return True


class CryptoPayment(PaymentProcessor):
    def process(self, amount: float) -> bool:
        print(f\"Crypto: charged \\")
        return True


class NotificationService:
    def send_order_confirmation(self, order: Order) -> None:
        print(f\"Sending confirmation to {order.customer}\")


class InventoryService:
    def update_stock(self, item: OrderItem) -> None:
        print(f\"Stock updated: {item.name} -{item.quantity}\")


class OrderService:
    def __init__(
        self,
        payment: PaymentProcessor,
        notification: NotificationService,
        inventory: InventoryService,
    ):
        self._payment = payment
        self._notification = notification
        self._inventory = inventory

    def create_order(self, customer: str, items: list[OrderItem]) -> Order:
        order = Order(customer=customer, items=items)
        self._payment.process(order.total)
        self._notification.send_order_confirmation(order)
        for item in order.items:
            self._inventory.update_stock(item)
        return order


if __name__ == \"__main__\":
    items = [
        OrderItem(\"Python Book\", 59.99, 2),
        OrderItem(\"Keyboard\", 129.99, 1),
    ]

    order_service = OrderService(
        payment=CreditCardPayment(),
        notification=NotificationService(),
        inventory=InventoryService(),
    )

    order = order_service.create_order(\"Alice\", items)
    print(f\"\\nOrder total: \\")
