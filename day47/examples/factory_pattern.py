\"\"\"工厂模式示例\"\"\"

from abc import ABC, abstractmethod
from typing import Any


# === 简单工厂 ===
class PaymentProcessor(ABC):
    @abstractmethod
    def charge(self, amount: float) -> bool: ...


class CreditCardProcessor(PaymentProcessor):
    def charge(self, amount: float) -> bool:
        print(f\"Charged credit card: \\")
        return True


class PayPalProcessor(PaymentProcessor):
    def charge(self, amount: float) -> bool:
        print(f\"Charged PayPal: \\")
        return True


class AlipayProcessor(PaymentProcessor):
    def charge(self, amount: float) -> bool:
        print(f\"Charged Alipay: \\")
        return True


class PaymentFactory:
    \"\"\"简单工厂\"\"\"
    _processors = {
        \"credit_card\": CreditCardProcessor,
        \"paypal\": PayPalProcessor,
        \"alipay\": AlipayProcessor,
    }

    @classmethod
    def create(cls, processor_type: str, **kwargs: Any) -> PaymentProcessor:
        processor_cls = cls._processors.get(processor_type)
        if not processor_cls:
            raise ValueError(f\"Unknown payment type: {processor_type}\")
        return processor_cls(**kwargs)

    @classmethod
    def register(cls, name: str, processor_cls: type) -> None:
        cls._processors[name] = processor_cls


# === 注册表模式 ===
class ServiceRegistry:
    _services: dict[str, type] = {}

    @classmethod
    def register(cls, name: str):
        def decorator(service_cls):
            cls._services[name] = service_cls
            return service_cls
        return decorator

    @classmethod
    def create(cls, name: str, **kwargs: Any):
        if name not in cls._services:
            raise KeyError(f\"Service '{name}' not registered\")
        return cls._services[name](**kwargs)

    @classmethod
    def list_services(cls) -> list[str]:
        return list(cls._services.keys())


@ServiceRegistry.register(\"email\")
class EmailNotification:
    def __init__(self, smtp_host: str = \"smtp.example.com\"):
        self.smtp_host = smtp_host

    def send(self, to: str, message: str) -> None:
        print(f\"[Email via {self.smtp_host}] To: {to}, Msg: {message}\")


@ServiceRegistry.register(\"sms\")
class SMSNotification:
    def __init__(self, api_key: str = \"sk-test\"):
        self.api_key = api_key

    def send(self, to: str, message: str) -> None:
        print(f\"[SMS] To: {to}, Msg: {message}\")


@ServiceRegistry.register(\"push\")
class PushNotification:
    def __init__(self, project_id: str = \"proj-123\"):
        self.project_id = project_id

    def send(self, to: str, message: str) -> None:
        print(f\"[Push via {self.project_id}] To: {to}, Msg: {message}\")


if __name__ == \"__main__\":
    # 简单工厂
    for ptype in [\"credit_card\", \"paypal\", \"alipay\"]:
        proc = PaymentFactory.create(ptype)
        proc.charge(99.99)

    print()

    # 注册表
    print(\"Available services:\", ServiceRegistry.list_services())
    for name in ServiceRegistry.list_services():
        svc = ServiceRegistry.create(name)
        svc.send(\"user@example.com\", \"Hello!\")
