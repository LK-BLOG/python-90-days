# Day 84: Permission System - 权限系统

## 1. 权限基础概念

权限系统是 Agent 安全运行的基石。一个没有权限控制的 Agent 就像一个没有门的房子——谁都能进来搞破坏。

### 权限的三要素

```
权限 = 主体(Subject) + 动作(Action) + 资源(Resource)
```

- **主体**：谁？用户、角色、系统进程
- **动作**：做什么？读、写、执行、管理
- **资源**：对什么？文件、API、数据库、工具

### 权限模型对比

| 模型 | 描述 | 复杂度 | 适用场景 |
|------|------|--------|----------|
| ACL  | 直接给用户分配权限 | 低 | 小型系统 |
| RBAC | 通过角色间接分配 | 中 | 企业系统 |
| ABAC | 基于属性的动态控制 | 高 | 复杂环境 |
| ReBAC| 基于关系的权限传播 | 中高 | 社交平台 |

## 2. RBAC 实现

RBAC (Role-Based Access Control) 是最主流的权限模型。核心思想：**不直接给用户权限，而是给用户分配角色，角色再关联权限。**

```python
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Set, Optional

# ========== 权限定义 ==========
class Action(Enum):
    """支持的操作类型"""
    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    EXECUTE = "execute"
    MANAGE = "manage"

@dataclass(frozen=True)
class Permission:
    """权限对象：资源 + 操作的组合"""
    resource: str          # 资源标识，如 "file", "api.weather"
    action: Action         # 操作类型

    def __str__(self):
        return f"{self.resource}:{self.action.value}"

# ========== 角色定义 ==========
@dataclass
class Role:
    """角色：一组权限的集合"""
    name: str
    permissions: Set[Permission] = field(default_factory=set)

    def has_permission(self, perm: Permission) -> bool:
        # MANAGE 权限包含所有子操作
        if Permission(self.resource, Action.MANAGE) in self.permissions:
            return True
        return perm in self.permissions

# ========== RBAC 引擎 ==========
class RBACEngine:
    """RBAC 权限引擎"""

    def __init__(self):
        self.roles: Dict[str, Role] = {}
        self.user_roles: Dict[str, Set[str]] = {}  # user -> roles

    def add_role(self, role: Role):
        self.roles[role.name] = role

    def assign_role(self, username: str, role_name: str):
        if role_name not in self.roles:
            raise ValueError(f"角色不存在: {role_name}")
        self.user_roles.setdefault(username, set()).add(role_name)

    def check_permission(self, username: str, permission: Permission) -> bool:
        """检查用户是否拥有某个权限"""
        user_roles = self.user_roles.get(username, set())
        for role_name in user_roles:
            role = self.roles[role_name]
            if role.has_permission(permission):
                return True
        return False

    def get_user_permissions(self, username: str) -> Set[Permission]:
        """获取用户的所有权限（角色合并）"""
        perms = set()
        for role_name in self.user_roles.get(username, set()):
            perms |= self.roles[role_name].permissions
        return perms
```

## 3. 装饰器做权限检查

装饰器是 Python 中实现权限检查的优雅方式。把权限逻辑和业务逻辑分离。

```python
import functools
from typing import Callable, Optional

# ========== 权限上下文 ==========
class PermissionContext:
    """当前请求的权限上下文（线程安全）"""
    _current_user: Optional[str] = None
    _rbac_engine: Optional[RBACEngine] = None

    @classmethod
    def set_user(cls, username: str):
        cls._current_user = username

    @classmethod
    def set_engine(cls, engine: RBACEngine):
        cls._rbac_engine = engine

    @classmethod
    def get_user(cls) -> str:
        if not cls._current_user:
            raise PermissionError("未设置当前用户")
        return cls._current_user

    @classmethod
    def check(cls, resource: str, action: Action) -> bool:
        user = cls.get_user()
        perm = Permission(resource, action)
        return cls._rbac_engine.check_permission(user, perm)

# ========== 权限装饰器 ==========
def require_permission(resource: str, action: Action):
    """
    权限检查装饰器

    用法:
        @require_permission("file", Action.READ)
        def read_file(path): ...
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            user = PermissionContext.get_user()
            perm = Permission(resource, action)
            if not PermissionContext.check(resource, action):
                raise PermissionError(
                    f"用户 '{user}' 无权执行 "
                    f"'{func.__name__}' ({perm})"
                )
            # 记录审计日志
            AuditLogger.log(user, action.value, resource, func.__name__)
            return func(*args, **kwargs)
        return wrapper
    return decorator

def require_role(role_name: str):
    """角色检查装饰器"""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            user = PermissionContext.get_user()
            engine = PermissionContext._rbac_engine
            if role_name not in engine.user_roles.get(user, set()):
                raise PermissionError(
                    f"用户 '{user}' 不具备角色 '{role_name}'"
                )
            return func(*args, **kwargs)
        return wrapper
    return decorator
```

## 4. 权限存储

真实系统中权限需要持久化。支持内存、数据库等多种后端。

```python
import json
import time
from abc import ABC, abstractmethod
from pathlib import Path

class PermissionStore(ABC):
    """权限存储抽象基类"""

    @abstractmethod
    def save_roles(self, roles: Dict[str, Role]):
        """保存角色定义"""

    @abstractmethod
    def load_roles(self) -> Dict[str, Role]:
        """加载角色定义"""

    @abstractmethod
    def save_user_roles(self, user_roles: Dict[str, List[str]]):
        """保存用户-角色映射"""

    @abstractmethod
    def load_user_roles(self) -> Dict[str, List[str]]:
        """加载用户-角色映射"""

class JSONPermissionStore(PermissionStore):
    """基于 JSON 文件的权限存储"""

    def __init__(self, config_path: str = "rbac_config.json"):
        self.config_path = Path(config_path)

    def save_roles(self, roles: Dict[str, Role]):
        data = {}
        for name, role in roles.items():
            data[name] = [
                {"resource": p.resource, "action": p.action.value}
                for p in role.permissions
            ]
        self.config_path.write_text(
            json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8"
        )

    def load_roles(self) -> Dict[str, Role]:
        if not self.config_path.exists():
            return {}
        data = json.loads(self.config_path.read_text(encoding="utf-8"))
        roles = {}
        for name, perms_data in data.items():
            perms = {
                Permission(p["resource"], Action(p["action"]))
                for p in perms_data
            }
            roles[name] = Role(name=name, permissions=perms)
        return roles

    def save_user_roles(self, user_roles: Dict[str, List[str]]):
        self.config_path.with_suffix(".users.json").write_text(
            json.dumps(user_roles, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )

    def load_user_roles(self) -> Dict[str, List[str]]:
        path = self.config_path.with_suffix(".users.json")
        if not path.exists():
            return {}
        return json.loads(path.read_text(encoding="utf-8"))
```

## 5. 审计日志

审计日志记录所有权限相关的操作，用于安全审计和问题排查。

```python
import logging
import json
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import List, Optional
from pathlib import Path

@dataclass
class AuditEntry:
    """审计日志条目"""
    timestamp: str
    username: str
    action: str
    resource: str
    function: str
    result: str          # "success" | "denied" | "error"
    details: Optional[str] = None
    ip_address: Optional[str] = None

class AuditLogger:
    """审计日志系统"""

    _logger: Optional[logging.Logger] = None
    _entries: List[AuditEntry] = []

    @classmethod
    def init(cls, log_file: str = "audit.log", level=logging.INFO):
        """初始化审计日志"""
        cls._logger = logging.getLogger("audit")
        cls._logger.setLevel(level)
        handler = logging.FileHandler(log_file, encoding="utf-8")
        handler.setFormatter(
            logging.Formatter("%(asctime)s | %(message)s")
        )
        cls._logger.addHandler(handler)

    @classmethod
    def log(cls, username: str, action: str, resource: str,
            function: str, result: str = "success", details: str = None):
        """记录审计事件"""
        entry = AuditEntry(
            timestamp=datetime.now().isoformat(),
            username=username,
            action=action,
            resource=resource,
            function=function,
            result=result,
            details=details,
        )
        cls._entries.append(entry)
        if cls._logger:
            cls._logger.info(
                f"{username} | {action} | {resource} | "
                f"{function} | {result}"
            )

    @classmethod
    def get_entries(cls, username: str = None,
                    resource: str = None) -> List[AuditEntry]:
        """查询审计日志"""
        entries = cls._entries
        if username:
            entries = [e for e in entries if e.username == username]
        if resource:
            entries = [e for e in entries if e.resource == resource]
        return entries

    @classmethod
    def export_json(cls, path: str):
        """导出审计日志为 JSON"""
        Path(path).write_text(
            json.dumps(
                [asdict(e) for e in cls._entries],
                indent=2, ensure_ascii=False
            ),
            encoding="utf-8"
        )
```

## 6. Agent 工具权限集成

在 Agent 系统中，每次工具调用都应经过权限检查：

```python
from typing import Any, Dict, Callable

class SecureToolRegistry:
    """安全工具注册表：所有工具调用必须过权限检查"""

    def __init__(self, rbac: RBACEngine):
        self.rbac = rbac
        self.tools: Dict[str, Callable] = {}
        self.tool_permissions: Dict[str, Permission] = {}

    def register(self, name: str, permission: Permission):
        """注册工具及其所需权限"""
        def decorator(func: Callable) -> Callable:
            self.tools[name] = func
            self.tool_permissions[name] = permission
            return func
        return decorator

    def call(self, tool_name: str, user: str, **kwargs) -> Any:
        """安全调用工具"""
        if tool_name not in self.tools:
            raise KeyError(f"工具不存在: {tool_name}")

        perm = self.tool_permissions[tool_name]
        if not self.rbac.check_permission(user, perm):
            AuditLogger.log(
                user, perm.action.value, perm.resource,
                tool_name, result="denied"
            )
            raise PermissionError(
                f"用户 '{user}' 无权调用工具 '{tool_name}'"
            )

        AuditLogger.log(
            user, perm.action.value, perm.resource,
            tool_name, result="success"
        )
        return self.tools[tool_name](**kwargs)
```

## 关键要点

1. **RBAC 是核心**：用户-角色-权限三层模型，解耦且灵活
2. **装饰器是利器**：权限检查和业务逻辑分离，代码干净
3. **审计不可少**：安全系统必须有日志，出了事能查
4. **存储要灵活**：支持 JSON 文件、数据库等不同后端
5. **工具级权限**：Agent 的每个工具调用都必须过权限关

## 下一步

完成 [挑战练习](challenge.md) 和 [终极挑战](ultimate_challenge.md) 来巩固所学知识。
