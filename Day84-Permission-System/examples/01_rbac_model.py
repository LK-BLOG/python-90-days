"""Day 84 Example 01: RBAC 权限模型"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Set, List


# ========== 操作类型 ==========
class Action(Enum):
    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    EXECUTE = "execute"
    MANAGE = "manage"  # 管理权限，包含所有子操作


# ========== 权限对象 ==========
@dataclass(frozen=True)
class Permission:
    """权限 = 资源 + 操作"""
    resource: str
    action: Action

    def __str__(self):
        return f"{self.resource}:{self.action.value}"


# ========== 角色 ==========
@dataclass
class Role:
    """角色 = 权限集合"""
    name: str
    description: str = ""
    permissions: Set[Permission] = field(default_factory=set)

    def add_permission(self, perm: Permission):
        self.permissions.add(perm)

    def remove_permission(self, perm: Permission):
        self.permissions.discard(perm)

    def has_permission(self, perm: Permission) -> bool:
        # MANAGE 权限包含该资源的所有操作
        manage_perm = Permission(perm.resource, Action.MANAGE)
        if manage_perm in self.permissions:
            return True
        return perm in self.permissions


# ========== RBAC 引擎 ==========
class RBACEngine:
    """基于角色的访问控制引擎"""

    def __init__(self):
        self._roles: Dict[str, Role] = {}
        self._user_roles: Dict[str, Set[str]] = {}

    # --- 角色管理 ---
    def create_role(self, name: str, description: str = "") -> Role:
        role = Role(name=name, description=description)
        self._roles[name] = role
        return role

    def get_role(self, name: str) -> Role:
        return self._roles.get(name)

    # --- 用户-角色映射 ---
    def assign_role(self, username: str, role_name: str):
        if role_name not in self._roles:
            raise ValueError(f"角色 '{role_name}' 不存在")
        self._user_roles.setdefault(username, set()).add(role_name)

    def revoke_role(self, username: str, role_name: str):
        if username in self._user_roles:
            self._user_roles[username].discard(role_name)

    # --- 权限检查 ---
    def check(self, username: str, resource: str, action: Action) -> bool:
        """检查用户对资源是否有指定操作权限"""
        perm = Permission(resource, action)
        for role_name in self._user_roles.get(username, set()):
            role = self._roles.get(role_name)
            if role and role.has_permission(perm):
                return True
        return False

    def get_user_permissions(self, username: str) -> Set[Permission]:
        """获取用户所有权限（角色合并）"""
        perms = set()
        for role_name in self._user_roles.get(username, set()):
            role = self._roles.get(role_name)
            if role:
                perms |= role.permissions
        return perms


# ========== 使用示例 ==========
def main():
    rbac = RBACEngine()

    # 创建角色
    reader = rbac.create_role("reader", "只读角色")
    reader.add_permission(Permission("file", Action.READ))

    editor = rbac.create_role("editor", "编辑角色")
    editor.add_permission(Permission("file", Action.READ))
    editor.add_permission(Permission("file", Action.WRITE))

    admin = rbac.create_role("admin", "管理员")
    admin.add_permission(Permission("file", Action.MANAGE))
    admin.add_permission(Permission("user", Action.MANAGE))

    # 分配角色
    rbac.assign_role("alice", "editor")
    rbac.assign_role("bob", "reader")
    rbac.assign_role("root", "admin")

    # 检查权限
    print("=== 权限检查 ===")
    tests = [
        ("alice", "file", Action.READ),    # True
        ("alice", "file", Action.DELETE),  # False
        ("bob", "file", Action.READ),      # True
        ("bob", "file", Action.WRITE),     # False
        ("root", "file", Action.READ),     # True (MANAGE包含)
        ("root", "file", Action.DELETE),   # True (MANAGE包含)
        ("root", "user", Action.READ),     # True (MANAGE包含)
    ]

    for user, resource, action in tests:
        result = rbac.check(user, resource, action)
        status = "✓" if result else "✗"
        print(f"  {status} {user} → {resource}:{action.value} = {result}")

    # 查看用户所有权限
    print(f"\n=== Alice 的权限 ===")
    for perm in rbac.get_user_permissions("alice"):
        print(f"  - {perm}")


if __name__ == "__main__":
    main()
