from typing import TypedDict, Optional

class UserResponse(TypedDict):
    pass  # TODO: id, name, email (optional)

class ApiResponse(TypedDict):
    pass  # TODO: status, data (UserResponse or None), error (optional)

# Test
if __name__ == "__main__":
    resp: ApiResponse = {
        "status": "success",
        "data": {"id": 1, "name": "Alice", "email": "alice@test.com"},
        "error": None
    }
    print(resp)