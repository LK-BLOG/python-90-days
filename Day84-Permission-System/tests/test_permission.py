"""Day 84 测试: 权限系统"""

import pytest
from enum import Enum


# 导入被测模块（或自行定义测试用类）
class Action(Enum):
    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    MANAGE = "manage"


# ---------- 测试 Permission ----------
class TestPermission:
    def test_creation(self):
        from dataclasses import dataclass
        @dataclass(frozen=True)
        class Permission:
            resource: str
            action: Action
        p = Permission("file", Action.READ)
        assert p.resource == "file"
        assert p.action == Action.READ

    def test_equality(self):
        from dataclasses import dataclass
        @dataclass(frozen=True)
        class Permission:
            resource: str
            action: Action
        p1 = Permission("file", Action.READ)
        p2 = Permission("file", Action.READ)
        assert p1 == p2

    def test_hash(self):
        from dataclasses import dataclass
        @dataclass(frozen=True)
        class Permission:
            resource: str
            action: Action
        p = Permission("file", Action.READ)
        s = {p, Permission("file", Action.READ)}
        assert len(s) == 1  # 相同权限去重


# ---------- 测试 Role ----------
class TestRole:
    def setup_method(self):
        from dataclasses import dataclass, field
        @dataclass(frozen=True)
        class Permission:
            resource: str
            action: Action
        @dataclass
        class Role:
            name: str
            permissions: set = field(default_factory=set)
            def add_permission(self, perm):
                self.permissions.add(perm)
            def has_permission(self, perm):
                manage = Permission(perm.resource, Action.MANAGE)
                return perm in self.permissions or manage in self.permissions
        self.Role = Role
        self.Permission = Permission

    def test_add_permission(self):
        r = self.Role("test")
        r.add_permission(self.Permission("file", Action.READ))
        assert r.has_permission(self.Permission("file", Action.READ))

    def test_manage_covers_all(self):
        r = self.Role("admin")
        r.add_permission(self.Permission("file", Action.MANAGE))
        assert r.has_permission(self.Permission("file", Action.READ))
        assert r.has_permission(self.Permission("file", Action.WRITE))
        assert r.has_permission(self.Permission("file", Action.DELETE))

    def test_no_cross_resource(self):
        r = self.Role("test")
        r.add_permission(self.Permission("file", Action.MANAGE))
        assert not r.has_permission(self.Permission("db", Action.READ))


# ---------- 测试 RBAC 引擎 ----------
class TestRBACEngine:
    def setup_method(self):
        from dataclasses import dataclass, field
        from typing import Dict, Set

        @dataclass(frozen=True)
        class Permission:
            resource: str
            action: Action
            def __hash__(self):
                return hash((self.resource, self.action))

        @dataclass
        class Role:
            name: str
            permissions: Set = field(default_factory=set)
            def add_permission(self, perm):
                self.permissions.add(perm)
            def has_permission(self, perm):
                manage = Permission(perm.resource, Action.MANAGE)
                return perm in self.permissions or manage in self.permissions

        class RBACEngine:
            def __init__(self):
                self._roles: Dict[str, Role] = {}
                self._user_roles: Dict[str, Set[str]] = {}
            def create_role(self, name):
                r = Role(name)
                self._roles[name] = r
                return r
            def assign_role(self, user, role_name):
                self._user_roles.setdefault(user, set()).add(role_name)
            def check(self, user, resource, action):
                perm = Permission(resource, action)
                for rn in self._user_roles.get(user, set()):
                    r = self._roles.get(rn)
                    if r and r.has_permission(perm):
                        return True
                return False
            def get_user_permissions(self, user):
                perms = set()
                for rn in self._user_roles.get(user, set()):
                    r = self._roles.get(rn)
                    if r:
                        perms |= r.permissions
                return perms

        self.RBACEngine = RBACEngine
        self.Permission = Permission

    def test_basic_check(self):
        e = self.RBACEngine()
        r = e.create_role("reader")
        r.add_permission(self.Permission("file", Action.READ))
        e.assign_role("alice", "reader")
        assert e.check("alice", "file", Action.READ)
        assert not e.check("alice", "file", Action.WRITE)

    def test_user_not_found(self):
        e = self.RBACEngine()
        assert not e.check("nobody", "file", Action.READ)

    def test_multi_role(self):
        e = self.RBACEngine()
        r1 = e.create_role("reader")
        r1.add_permission(self.Permission("file", Action.READ))
        r2 = e.create_role("writer")
        r2.add_permission(self.Permission("file", Action.WRITE))
        e.assign_role("alice", "reader")
        e.assign_role("alice", "writer")
        assert e.check("alice", "file", Action.READ)
        assert e.check("alice", "file", Action.WRITE)
        assert not e.check("alice", "file", Action.DELETE)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
