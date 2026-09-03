"""Challenge 3: Mixin 工具箱"""
import json, copy

class JsonMixin:
    # TODO: to_json(), from_json()
    pass

class HashMixin:
    # TODO: 自动生成 __hash__
    pass

class CloneMixin:
    # TODO: clone() 深拷贝
    pass

class User(JsonMixin, HashMixin, CloneMixin):
    def __init__(self, name, age):
        self.name = name
        self.age = age
