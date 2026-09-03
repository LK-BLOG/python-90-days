\"\"\"Day 47: DI练习测试\"\"\"

import pytest


def test_container_bind_resolve():
    from manual_di import Container

    container = Container()
    container.bind(\"value\", lambda: 42)
    assert container.resolve(\"value\") == 42
    assert container.resolve(\"value\") != container.resolve(\"value\")  # 每次新实例


def test_container_singleton():
    from manual_di import Container

    container = Container()
    container.singleton(\"value\", lambda: 42)
    assert container.resolve(\"value\") is container.resolve(\"value\")  # 同一实例


def test_factory_pattern():
    from factory_pattern import PaymentFactory, ServiceRegistry

    proc = PaymentFactory.create(\"credit_card\")
    assert proc.charge(100) is True

    svc = ServiceRegistry.create(\"email\")
    assert hasattr(svc, \"send\")
    assert \"email\" in ServiceRegistry.list_services()


def test_container_reset():
    from manual_di import Container

    container = Container()
    container.singleton(\"key\", lambda: \"val\")
    container.resolve(\"key\")
    container.reset()
    assert not container.has(\"key\")
