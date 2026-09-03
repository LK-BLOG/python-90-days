# -*- coding: utf-8 -*-
class AppError(Exception):
    pass

class ValidationError(AppError):
    def __init__(self, field, message):
        self.field = field
        self.message = message
        super().__init__(f"字段 {field}: {message}")

def create_user(name, age):
    if not name:
        raise ValidationError("name", "不能为空")
    return {"name": name, "age": age}

try:
    create_user("", 25)
except ValidationError as e:
    print(f"验证失败: {e}")
    print(f"字段: {e.field}")
