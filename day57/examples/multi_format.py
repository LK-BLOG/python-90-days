\"\"\"多格式序列化层\"\"\"

import json
from abc import ABC, abstractmethod
from typing import Any

try:
    import msgpack
except ImportError:
    msgpack = None

try:
    import yaml
except ImportError:
    yaml = None


class Serializer(ABC):
    \"\"\"序列化器抽象接口\"\"\"

    @abstractmethod
    def dumps(self, data: Any) -> bytes: ...

    @abstractmethod
    def loads(self, data: bytes) -> Any: ...

    @property
    @abstractmethod
    def content_type(self) -> str: ...


class JSONSerializer(Serializer):
    def dumps(self, data: Any) -> bytes:
        return json.dumps(data, default=str, ensure_ascii=False).encode()

    def loads(self, data: bytes) -> Any:
        return json.loads(data)

    @property
    def content_type(self) -> str:
        return \"application/json\"


class MsgPackSerializer(Serializer):
    def dumps(self, data: Any) -> bytes:
        if msgpack is None:
            raise ImportError(\"pip install msgpack\")
        return msgpack.packb(data, default=str)

    def loads(self, data: bytes) -> Any:
        if msgpack is None:
            raise ImportError(\"pip install msgpack\")
        return msgpack.unpackb(data, raw=False)

    @property
    def content_type(self) -> str:
        return \"application/msgpack\"


class YAMLSerializer(Serializer):
    def dumps(self, data: Any) -> bytes:
        if yaml is None:
            raise ImportError(\"pip install pyyaml\")
        return yaml.dump(data, allow_unicode=True).encode()

    def loads(self, data: bytes) -> Any:
        if yaml is None:
            raise ImportError(\"pip install pyyaml\")
        return yaml.safe_load(data)

    @property
    def content_type(self) -> str:
        return \"application/yaml\"


class SerializationRegistry:
    \"\"\"序列化器注册表\"\"\"

    def __init__(self):
        self._serializers: dict[str, Serializer] = {}
        self._default = \"json\"

    def register(self, name: str, serializer: Serializer) -> None:
        self._serializers[name] = serializer

    def get(self, name: str | None = None) -> Serializer:
        name = name or self._default
        if name not in self._serializers:
            raise KeyError(f\"Unknown serializer: {name}\")
        return self._serializers[name]

    def from_content_type(self, content_type: str) -> Serializer:
        for s in self._serializers.values():
            if s.content_type == content_type:
                return s
        return self.get()  # fallback to default


# 默认注册表
registry = SerializationRegistry()
registry.register(\"json\", JSONSerializer())
registry.register(\"msgpack\", MsgPackSerializer())
registry.register(\"yaml\", YAMLSerializer())


if __name__ == \"__main__\":
    data = {\"users\": [{\"name\": \"Alice\", \"age\": 30}, {\"name\": \"Bob\", \"age\": 25}]}

    for name in [\"json\", \"msgpack\", \"yaml\"]:
        try:
            serializer = registry.get(name)
            serialized = serializer.dumps(data)
            deserialized = serializer.loads(serialized)
            print(f\"{name}: {len(serialized)} bytes, content-type: {serializer.content_type}\")
            assert deserialized == data
        except ImportError as e:
            print(f\"{name}: {e}\")
