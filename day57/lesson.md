# Day 57 课程：序列化 & 数据格式

## 第一部分：序列化概述

### 1.1 什么是序列化
序列化 = 把Python对象转换为可存储/传输的格式（JSON/Binary/YAML）
反序列化 = 从格式还原为Python对象

### 1.2 常见格式对比
| 格式 | 可读 | 大小 | 速度 | 适用场景 |
|------|------|------|------|---------|
| JSON | ✅ | 中 | 中 | Web API |
| YAML | ✅ | 大 | 慢 | 配置文件 |
| MessagePack | ❌ | 小 | 快 | 微服务通信 |
| Protobuf | ❌ | 最小 | 最快 | gRPC/高性能 |
| Pickle | ❌ | 中 | 最快 | Python内部 |

---

## 第二部分：Pydantic v2高级序列化

### 2.1 自定义序列化
`python
from pydantic import BaseModel, field_serializer, model_serializer
from datetime import datetime

class Article(BaseModel):
    title: str
    content: str
    created_at: datetime

    @field_serializer("created_at")
    def serialize_date(self, v: datetime) -> str:
        return v.strftime("%Y-%m-%d")

    model_config = {"json_encoders": {datetime: lambda v: v.isoformat()}}
`

### 2.2 多格式输出
`python
class Article(BaseModel):
    title: str
    content: str

    def to_json(self) -> str:
        return self.model_dump_json()

    def to_xml(self) -> str:
        return f"<article><title>{self.title}</title><content>{self.content}</content></article>"

    def to_dict(self) -> dict:
        return self.model_dump()
`

---

## 第三部分：marshmallow

### 3.1 基本使用
`python
from marshmallow import Schema, fields, validate, post_load

class UserSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    email = fields.Email(required=True)
    age = fields.Int(validate=validate.Range(min=0, max=150))
    created_at = fields.DateTime(dump_only=True)

schema = UserSchema()
data = schema.load({"name": "Alice", "email": "alice@test.com", "age": 30})
json_str = schema.dumps(data)
`

### 3.2 自定义字段和验证
`python
class TagField(fields.Field):
    def _serialize(self, value, attr, obj):
        return ",".join(value) if isinstance(value, list) else value

    def _deserialize(self, value, attr, data):
        return value.split(",") if isinstance(value, str) else value
`

---

## 第四部分：Protocol Buffers

### 4.1 定义schema
`protobuf
// article.proto
syntax = "proto3";

message Article {
    int32 id = 1;
    string title = 2;
    string content = 3;
    repeated string tags = 4;
    int64 created_at = 5;
}
`

### 4.2 Python使用
`python
# 编译: protoc --python_out=. article.proto
import article_pb2

article = article_pb2.Article()
article.id = 1
article.title = "Hello"
article.content = "World"

# 序列化
binary = article.SerializeToString()

# 反序列化
article2 = article_pb2.Article()
article2.ParseFromString(binary)
`

---

## 第五部分：MessagePack

`python
import msgpack

# 序列化
data = {"name": "Alice", "scores": [95, 87, 92]}
packed = msgpack.packb(data)

# 反序列化
unpacked = msgpack.unpackb(packed, raw=False)
# 比JSON小30-50%，快2-3倍
`

---

## 本课总结

| 格式 | 推荐场景 |
|------|---------|
| JSON | Web API、配置 |
| YAML | 配置文件 |
| Protobuf | gRPC、高性能 |
| MessagePack | 微服务、缓存 |
| Pickle | Python内部、临时存储 |
