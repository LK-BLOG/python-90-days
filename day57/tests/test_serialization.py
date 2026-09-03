\"\"\"Day 57: 序列化测试\"\"\"

import json
import pytest


def test_json_serializer():
    from multi_format import JSONSerializer
    s = JSONSerializer()
    data = {\"name\": \"Alice\", \"scores\": [95, 87]}
    serialized = s.dumps(data)
    assert isinstance(serialized, bytes)
    assert s.loads(serialized) == data


def test_registry():
    from multi_format import registry
    s = registry.get(\"json\")
    assert s.content_type == \"application/json\"


def test_pydantic_serialization():
    from pydantic_serial import Article
    from datetime import datetime

    a = Article(title=\"Test\", content=\"Content\", created_at=datetime(2024, 1, 1))
    j = a.model_dump_json()
    data = json.loads(j)
    assert data[\"title\"] == \"Test\"
