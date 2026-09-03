"""Day 84 Example 02: 权限装饰器"""

import functools
from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, Set, Optional, Callable


# ========== 基础类型（简化版） ==========
class Action(Enum):
    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    EXECUTE = "execute"
    MANAGE = "manage"

@dataclass(frozen=True)
class Permission:
    resource: str
    action: Action


# ========== 审计日志（内存版） ==========
class AuditLog:
    """简易审计日志"""
    _entries = []

    @classmethod
    def log(cls, user: str, action: str, resource: str,
            func_name: str, result: str):
        import datetime
        entry = {
            "time": datetime.datetime.now().isoformat(),
            "user": user, "action": action,
            "resource": resource, "function": func_name,
            "result": result,
        }
        cls._entries.append(entry)
        symbol = "✓" if result == "success" else "✗"
        print(f"  [审计] {symbol} {user} → {resource}:{action} via {func_name}")

    @classmethod
    def get_entries(cls, user: str = None) -> list:
        if user:
            return [e for e in cls._entries if e["user"] == user]
        return cls._entries[:]


# ========== 权限上下文 ==========
class PermContext:
    """线程级权限上下文"""
    _user: Optional[str] = None
    _permissions: Set[Permission] = field(default_factory=set)

    @classmethod
    def set(cls, user: str, permissions: Set[Permission]):
        cls._user = user
        cls._permissions = permissions

    @classmethod
    def get_user(cls) -> str:
        if not cls._user:
            raise PermissionError("未设置当前用户上下文")
        return cls._user

    @classmethod
    def has(cls, perm: Permission) -> bool:
        # 检查 MANAGE 覆盖
        manage = Permission(perm.resource, Action.MANAGE)
        return perm in cls._permissions or manage in cls._permissions


# ========== 权限异常 ==========
class PermissionDenied(PermissionError):
    def __init__(self, user: str, resource: str, action: Action):
        self.user = user
        self.resource = resource
        self.action = action
        msg = f"用户 '{user}' 无权执行 '{resource}:{action.value}'"
        super().__init__(msg)


# ========== 装饰器 ==========
def require(resource: str, action: Action):
    """
    单权限装饰器

    用法:
        @require("file", Action.READ)
        def read_file(path): ...
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            user = PermContext.get_user()
            perm = Permission(resource, action)
            if not PermContext.has(perm):
                AuditLog.log(user, action.value, resource, func.__name__, "denied")
                raise PermissionDenied(user, resource, action)
            AuditLog.log(user, action.value, resource, func.__name__, "success")
            return func(*args, **kwargs)
        return wrapper
    return decorator


def require_any(**perms_map):
    """
    多权限装饰器（OR 关系，满足任一即可）

    用法:
        @require_any(file=Action.READ, db=Action.READ)
        def query(...): ...
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            user = PermContext.get_user()
            for resource, action in perms_map.items():
                perm = Permission(resource, action)
                if PermContext.has(perm):
                    AuditLog.log(user, action.value, resource, func.__name__, "success")
                    return func(*args, **kwargs)
            # 全部不满足
            denied_info = ", ".join(
                f"{r}:{a.value}" for r, a in perms_map.items()
            )
            AuditLog.log(user, "multi", denied_info, func.__name__, "denied")
            raise PermissionDenied(user, "multi-resource", Action.READ)
        return wrapper
    return decorator


# ========== 使用示例 ==========
@require("file", Action.READ)
def read_file(path: str) -> str:
    return f"读取文件: {path}"

@require("file", Action.WRITE)
def write_file(path: str, content: str) -> str:
    return f"写入文件: {path} ({len(content)} bytes)"

@require_any(file=Action.READ, db=Action.READ)
def query_data(source: str) -> str:
    return f"查询数据: {source}"


def main():
    # 模拟用户权限
    print("=== 用户 Alice (有读权限) ===")
    PermContext.set("alice", {Permission("file", Action.READ)})

    try:
        print(read_file("/data/config.json"))
    except PermissionDenied as e:
        print(f"  拒绝: {e}")

    try:
        write_file("/data/config.json", "new content")
    except PermissionDenied as e:
        print(f"  拒绝: {e}")

    try:
        print(query_data("file"))
    except PermissionDenied as e:
        print(f"  拒绝: {e}")

    print("\n=== 用户 Bob (有读写权限) ===")
    PermContext.set("bob", {
        Permission("file", Action.READ),
        Permission("file", Action.WRITE),
    })

    try:
        print(read_file("/data/config.json"))
        print(write_file("/data/config.json", "updated"))
    except PermissionDenied as e:
        print(f"  拒绝: {e}")

    # 审计日志
    print(f"\n=== 审计日志 ({len(AuditLog.get_entries())} 条) ===")
    for entry in AuditLog.get_entries():
        print(f"  {entry['result']:>7s} | {entry['user']} | {entry['function']} | {entry['resource']}")


if __name__ == "__main__":
    main()
