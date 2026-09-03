# Day 6 挑战四：防御性编程 (★★★★☆)
# 要求: 用异常处理构建健壮的函数。


def robust_open(filepath, mode="r", encoding="utf-8", fallback=None):
    """健壮的文件打开函数。
    
    处理: 文件不存在、权限不足、编码错误等。
    """
    # TODO: 尝试打开文件，捕获各种异常，返回 fallback
    pass


def safe_json_loads(text, default=None):
    """安全 JSON 解析 —— 解析失败返回默认值。"""
    # TODO: import json，捕获 JSONDecodeError
    pass


def safe_batch_call(func, items, on_error="skip"):
    """批量调用函数 —— 单个失败不影响整体。
    
    Args:
        func: 要调用的函数
        items: 参数列表
        on_error: "skip" 跳过 / "stop" 中止 / "log" 记录后继续
    
    Returns:
        tuple: (成功结果列表, 失败记录列表)
    """
    # TODO: 遍历 items，逐个调用 func，处理异常
    pass


def validate_and_convert(data, schema):
    """根据 schema 验证并转换数据。
    
    schema 格式:
        {"name": str, "age": int, "score": float}
    
    Returns:
        tuple: (转换后的数据, 错误列表)
    """
    # TODO: 遍历 schema，尝试转换每个字段
    # TODO: 收集转换失败的错误
    pass


def retry(func, max_attempts=3, delay=1.0, backoff=2.0,
          exceptions=(Exception,)):
    """增强版重试函数 —— 带指数退避。
    
    Args:
        func: 要重试的函数（无参数）
        max_attempts: 最大尝试次数
        delay: 初始延迟秒数
        backoff: 退避倍数
        exceptions: 需要重试的异常类型
    
    Returns:
        func 的返回值
    
    Raises:
        最后一次异常（所有重试用尽后）
    """
    # TODO: 实现指数退避重试
    pass


# ===== 测试 =====
if __name__ == "__main__":
    results, errors = safe_batch_call(
        lambda x: 10 / x,
        [2, 0, 5, 0, 1],
        on_error="log"
    )
    print(f"成功: {results}")
    print(f"失败: {errors}")
    
    schema = {"name": str, "age": int, "score": float}
    data = {"name": "Alice", "age": "25", "score": "95.5", "bad": object}
    converted, errs = validate_and_convert(data, schema)
    print(f"转换: {converted}")
    print(f"错误: {errs}")
