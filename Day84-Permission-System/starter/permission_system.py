"""Day 84 Starter: 权限系统骨架 - 完成 TODO 部分"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Set, List, Optional, Callable
import functools
import datetime


# ========== 枚举和基础类 ==========
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

    def __str__(self):
        return f"{self.resource}:{self.action.value}"


class PermissionDenied(PermissionError):
    """权限不足异常"""
    def __init__(self, user: str, resource: str, action: Action):
        self.user = user
        self.resource = resource
        self.action = action
        super().__init__(f"'{user}' 无权 '{resource}:{action.value}'")


# ========== 角色 ==========
@dataclass
class Role:
    name: str
    permissions: Set[Permission] = field(default_factory=set)

    def add_permission(self, perm: Permission):
        self.permissions.add(perm)

    def has_permission(self, perm: Permission) -> bool:
        # TODO: 实现权限检查，MANAGE 权限应包含同资源的所有操作
        pass


# ========== RBAC 引擎 ==========
class RBACEngine:
    def __init__(self):
        self._roles: Dict[str, Role] = {}
        self._user_roles: Dict[str, Set[str]] = {}

    def create_role(self, name: str) -> Role:
        # TODO: 创建并注册角色
        pass

    def assign_role(self, username: str, role_name: str):
        # TODO: 给用户分配角色
        pass

    def check(self, username: str, resource: str, action: Action) -> bool:
        # TODO: 检查用户权限
        pass

    def get_user_permissions(self, username: str) -> Set[Permission]:
        # TODO: 获取用户所有权限（角色合并）
        pass


# ========== 权限上下文 ==========
class PermContext:
    _user: Optional[str] = None
    _permissions: Set[Permission] = field(default_factory=set)

    @classmethod
    def set(cls, user: str, permissions: Set[Permission]):
        cls._user = user
        cls._permissions = permissions

    @classmethod
    def get_user(cls) -> str:
        if not cls._user:
            raise PermissionError("未设置用户上下文")
        return cls._user

    @classmethod
    def has(cls, perm: Permission) -> bool:
        # TODO: 检查上下文权限（含 MANAGE 覆盖）
        pass


# ========== 权限装饰器 ==========
def require(resource: str, action: Action):
    """
    权限检查装饰器

    TODO: 实现装饰器逻辑
    - 检查当前用户是否有指定权限
    - 权限不足时抛出 PermissionDenied
    - 记录审计日志
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # TODO: 实现
            pass
        return wrapper
    return decorator


# ========== 审计日志 ==========
class AuditLogger:
    _entries: List[dict] = []

    @classmethod
    def log(cls, user: str, action: str, resource: str,
            function: str, result: str = "success"):
        # TODO: 记录审计条目
        pass

    @classmethod
    def query(cls, user: str = None, result: str = None) -> List[dict]:
        # TODO: 查询审计日志
        pass


# ========== 使用示例 ==========
def main():
    rbac = RBACEngine()

    # 创建角色并分配权限
    reader = rbac.create_role("reader")
    reader.add_permission(Permission("file", Action.READ))

    writer = rbac.create_role("writer")
    writer.add_permission(Permission("file", Action.READ))
    writer.add_permission(Permission("file", Action.WRITE))

    # 分配角色
    rbac.assign_role("alice", "writer")
    rbac.assign_role("bob", "reader")

    # 测试权限
    print("权限测试:")
    for user, resource, action in [
        ("alice", "file", Action.READ),
        ("alice", "file", Action.DELETE),
        ("bob", "file", Action.WRITE),
    ]:
        print(f"  {user} → {resource}:{action.value} = {rbac.check(user, resource, action)}")

    # 使用装饰器保护函数
    # @require("file", Action.WRITE)
    # def save_data(path, data): ...

    # 审计日志
    print("\n审计日志:")
    for entry in AuditLogger.query():
        print(f"  {entry}")


if __name__ == "__main__":
    main()
