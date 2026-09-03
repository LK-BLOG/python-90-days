# Day 1 挑战二：配置合并器 (★★☆☆☆)
# 难度: ★★☆☆☆
# 要求: 实现一个配置合并函数，支持嵌套字典合并和覆盖策略。

def merge_config(default, override, strategy="override"):
    """合并两个配置字典，支持三种合并策略。
    
    功能说明:
        将 override 字典中的配置合并到 default 字典中，根据 strategy 参数
        决定合并行为。处理嵌套字典时有不同表现。
    
    策略说明:
        - "override": override 完全覆盖 default（包括嵌套字典整体替换）
        - "deep":     递归合并嵌套字典，非字典值用 override 覆盖
        - "keep":     保留 default 中已有的值，只添加 override 中的新键
    
    示例:
        >>> default = {"db": {"host": "localhost", "port": 3306}, "debug": False}
        >>> override = {"db": {"port": 5432}, "debug": True}
        >>> merge_config(default, override, strategy="deep")
        {"db": {"host": "localhost", "port": 5432}, "debug": True}
    
    Args:
        default: 默认配置字典（基础配置）
        override: 覆盖配置字典（要合并进来的配置）
        strategy: 合并策略，可选 "override"/"deep"/"keep"，默认 "override"
    
    Returns:
        dict: 合并后的新字典（不修改原始字典）
    
    Raises:
        ValueError: 当 strategy 不是三种合法值之一时
    
    注意:
        - 返回的是新字典，不会修改传入的 default 或 override
        - deep 策略只对 dict 类型的值进行递归合并
    """
    # TODO: 步骤1 - 验证 strategy 参数的合法性
    # TODO: 步骤2 - 深拷贝 default 作为结果（避免修改原字典）
    # TODO: 步骤3 - 根据 strategy 分支处理:
    #   - override: 直接用 update 覆盖
    #   - keep: 只添加 default 中不存在的键
    #   - deep: 递归合并嵌套字典
    pass


def deep_merge(base, override):
    """递归深度合并两个字典（内部辅助函数）。
    
    功能说明:
        递归遍历两个字典，对于值都是 dict 的键进行递归合并，
        否则用 override 的值覆盖 base 的值。
    
    Args:
        base: 基础字典
        override: 覆盖字典
    
    Returns:
        dict: 深度合并后的新字典
    """
    # TODO: 实现递归合并逻辑
    # TODO: 处理 base 或 override 不是 dict 的情况
    pass


def flatten_config(config, prefix=""):
    """将嵌套字典展平为点号分隔的键值对。
    
    功能说明:
        将 {"db": {"host": "localhost"}} 展平为 {"db.host": "localhost"}
    
    Args:
        config: 嵌套字典
        prefix: 当前键的前缀（递归时使用）
    
    Returns:
        dict: 展平后的字典
    """
    # TODO: 实现字典展平逻辑
    # TODO: 递归处理嵌套字典，拼接点号分隔的键名
    pass


# ===== 测试 =====
if __name__ == "__main__":
    default = {"db": {"host": "localhost", "port": 3306}, "debug": False}
    override = {"db": {"port": 5432}, "debug": True}
    
    print("=== deep 策略 ===")
    print(merge_config(default, override, strategy="deep"))
    # {"db": {"host": "localhost", "port": 5432}, "debug": True}
    
    print("\n=== override 策略 ===")
    print(merge_config(default, override, strategy="override"))
    # {"db": {"port": 5432}, "debug": True}
    
    print("\n=== keep 策略 ===")
    print(merge_config(default, override, strategy="keep"))
    # {"db": {"host": "localhost", "port": 3306}, "debug": False}
    
    print("\n=== 展平测试 ===")
    nested = {"a": {"b": {"c": 1}}, "d": 2}
    print(flatten_config(nested))
    # {"a.b.c": 1, "d": 2}
