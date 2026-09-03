from pydantic import BaseModel, Field
from typing import Optional

# TODO: 定义 UserCreate 模型
class UserCreate(BaseModel):
    # TODO: name (str, 1-50字符)
    # TODO: email (str)
    # TODO: age (int, 0-150)
    # TODO: bio (Optional[str])
    pass

# TODO: 定义 UserResponse 模型
class UserResponse(BaseModel):
    # TODO: id (int)
    # TODO: 继承 UserCreate 的字段
    pass
