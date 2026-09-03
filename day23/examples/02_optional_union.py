from typing import Optional, Union

def find_user(user_id: int) -> Optional[dict]:
    if user_id > 0:
        return {"id": user_id, "name": "User"}
    return None

def process(value: Union[str, int]) -> str:
    return str(value)

user = find_user(1)
print(user)
print(process(42))
print(process("hello"))