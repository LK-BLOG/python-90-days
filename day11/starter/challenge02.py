# Day 11 - Challenge 2: 包结构设计
# 难度: ⭐⭐⭐☆☆
#
# 要求: 设计一个包结构，使用 __init__.py、相对导入，避免循环导入
# 参考 challenge.md

"""
包结构设计挑战 — 模拟一个项目包的内部模块划分

要求:
- 模拟 package 结构
- 使用相对导入
- 避免循环导入
- 合理的模块职责划分
"""

# 模拟包结构（全部写在一个文件里用于练习）:
# mypackage/
#   __init__.py      -> 统一导出
#   models.py        -> 数据模型
#   services.py      -> 业务逻辑
#   validators.py    -> 验证逻辑
#   utils.py         -> 工具函数


# ===== models.py 模拟 =====
class User:
    """用户数据模型

    Attributes:
        username: 用户名
        email: 邮箱
        age: 年龄
    """

    def __init__(self, username: str, email: str, age: int = 0):
        # TODO: 实现 __init__，并调用验证
        pass

    def to_dict(self) -> dict:
        """转换为字典"""
        # TODO: 返回 {"username": ..., "email": ..., "age": ...}
        pass

    def __repr__(self) -> str:
        # TODO: 返回 User(username='xxx', email='xxx')
        pass


# ===== validators.py 模拟 =====
def validate_email(email: str) -> bool:
    """验证邮箱格式"""
    # TODO: 检查 @ 和 . 的存在
    pass


def validate_username(username: str) -> bool:
    """验证用户名（3-20字符，字母数字下划线）"""
    # TODO: 长度检查 + 字符检查
    pass


def validate_age(age: int) -> bool:
    """验证年龄（0-150）"""
    # TODO: 类型检查 + 范围检查
    pass


# ===== services.py 模拟 =====
class UserService:
    """用户服务层，处理业务逻辑

    使用组合包含验证器，不直接依赖数据模型的具体实现。
    """

    def __init__(self):
        # TODO: 初始化用户存储（用 list 模拟）
        pass

    def create_user(self, username: str, email: str, age: int = 0) -> User:
        """创建新用户

        Raises:
            ValueError: 验证失败时抛出

        Returns:
            新创建的 User 实例
        """
        # TODO: 调用验证器 -> 创建 User -> 存储 -> 返回
        pass

    def find_user(self, username: str) -> User | None:
        """根据用户名查找用户"""
        # TODO: 遍历存储列表查找
        pass

    def list_all(self) -> list:
        """列出所有用户"""
        # TODO: 返回存储列表的副本
        pass


# ===== utils.py 模拟 =====
def generate_id() -> str:
    """生成简易唯一 ID

    Returns:
        格式为 "user_001" 的字符串
    """
    # TODO: 实现简易 ID 生成器（可以用全局计数器）
    pass


# ===== __init__.py 模拟 — 统一导出 =====
__all__ = ["User", "UserService", "validate_email", "validate_username", "validate_age"]


# ---- 测试 ----
if __name__ == "__main__":
    print("=== 包结构设计测试 ===")

    svc = UserService()

    # 创建用户
    u1 = svc.create_user("alice", "alice@example.com", 25)
    u2 = svc.create_user("bob", "bob@test.org", 30)
    print(u1)
    print(u2)

    # 查找用户
    found = svc.find_user("alice")
    print(f"找到: {found}")

    # 列出所有
    print(svc.list_all())

    # 验证失败
    try:
        svc.create_user("ab", "bad-email", -1)
    except ValueError as e:
        print(f"验证失败: {e}")

    print("✅ Challenge 02 完成")
