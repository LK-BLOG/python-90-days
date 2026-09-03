import json, copy

class JsonMixin:
    def to_json(self):
        return json.dumps(self.__dict__, ensure_ascii=False, indent=2)
    @classmethod
    def from_json(cls, s):
        return cls(**json.loads(s))

class LogMixin:
    def log(self, msg):
        print(f'[{self.__class__.__name__}] {msg}')

class CloneMixin:
    def clone(self):
        return copy.deepcopy(self)

class User(JsonMixin, LogMixin, CloneMixin):
    def __init__(self, name, age):
        self.name, self.age = name, age

u = User("Alice", 25)
u.log("hello")
print(u.to_json())
