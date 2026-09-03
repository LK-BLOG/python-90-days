# Day 6 挑战二：自定义异常 (★★☆☆☆)
# 要求: 设计并使用自定义异常层次结构。


class AppError(Exception):
    """应用根异常 —— 所有自定义异常的基类。"""
    def __init__(self, message, code=None):
        # TODO: 存储 message 和 error code
        pass


class ValidationError(AppError):
    """数据验证错误。"""
    def __init__(self, field, message, value=None):
        # TODO: 存储字段名、错误信息、触发错误的值
        pass


class NotFoundError(AppError):
    """资源未找到错误。"""
    def __init__(self, resource, identifier):
        # TODO: 存储资源类型和标识符
        pass


class PermissionError(AppError):
    """权限不足错误。"""
    def __init__(self, action, resource):
        # TODO: 存储操作名和资源名
        pass


class RateLimitError(AppError):
    """请求频率超限错误。"""
    def __init__(self, limit, window, retry_after=None):
        # TODO: 存储限制数、时间窗口、重试等待时间
        pass


def validate_user(data):
    """验证用户数据，不合格时抛出 ValidationError。
    
    规则: name 必填(str), age 必须 0-150(int), email 必须含 @
    """
    # TODO: 逐字段验证，收集所有错误后一次性抛出
    pass


def find_user(user_id, users_db):
    """在数据库中查找用户，不存在时抛出 NotFoundError。"""
    # TODO: 查找并处理
    pass


# ===== 测试 =====
if __name__ == "__main__":
    # 测试验证
    try:
        validate_user({"name": "", "age": -5, "email": "bad"})
    except ValidationError as e:
        print(f"验证失败: {e}")
    
    # 测试查找
    db = {1: {"name": "Alice"}, 2: {"name": "Bob"}}
    try:
        find_user(99, db)
    except NotFoundError as e:
        print(f"未找到: {e}")
