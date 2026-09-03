# Day 1 挑战四：参数验证器 (★★★★☆)
# 难度: ★★★★☆
# 要求: 实现参数验证系统，验证函数参数是否符合类型和范围要求。


class ParamValidator:
    """参数验证器 —— 用于验证函数参数是否符合预定义的规则。
    
    用法示例:
        >>> validator = ParamValidator()
        >>> validator.add("age", type=int, min=0, max=150)
        >>> validator.add("name", type=str, min_length=1, max_length=50)
        >>> validator.validate(age=25, name="Alice")   # 通过，无异常
        >>> validator.validate(age=-1, name="")         # 抛出 ValueError
    
    支持的验证规则:
        - type: 期望类型 (int/str/float/list/...)
        - min: 最小值（用于数字类型）
        - max: 最大值（用于数字类型）
        - min_length: 最小长度（用于 str/list）
        - max_length: 最大长度（用于 str/list）
        - choices: 允许的值列表
        - required: 是否必填（默认 True）
    """
    
    def __init__(self):
        """初始化验证器，创建空的规则存储。"""
        # TODO: 初始化一个字典，存储每个参数名对应的验证规则
        # 提示: self._rules = {}
        pass
    
    def add(self, name, **rules):
        """添加一个参数的验证规则。
        
        Args:
            name: 参数名（字符串）
            **rules: 验证规则关键字参数:
                - type (type): 期望的类型
                - min (int|float): 最小值
                - max (int|float): 最大值
                - min_length (int): 最小长度
                - max_length (int): 最大长度
                - choices (list): 允许的值列表
                - required (bool): 是否必填，默认 True
        
        Returns:
            self: 返回自身，支持链式调用
        """
        # TODO: 将 rules 存储到 self._rules[name] 中
        # TODO: 返回 self 以支持链式调用
        pass
    
    def validate(self, **kwargs):
        """验证传入的关键字参数是否符合所有规则。
        
        Args:
            **kwargs: 待验证的参数（键值对）
        
        Raises:
            ValueError: 当参数不符合验证规则时，包含具体的错误信息
            TypeError: 当参数类型不匹配时
        """
        # TODO: 遍历已注册的所有规则
        # TODO: 对每个规则检查对应的 kwargs 值
        # TODO: 收集所有验证错误，一次性抛出（或逐个抛出）
        pass
    
    def _check_type(self, name, value, expected_type):
        """检查值的类型是否匹配。
        
        Args:
            name: 参数名
            value: 实际值
            expected_type: 期望的类型
        
        Raises:
            TypeError: 类型不匹配
        """
        # TODO: 使用 isinstance 检查类型
        pass
    
    def _check_range(self, name, value, rules):
        """检查数值范围和长度范围。
        
        Args:
            name: 参数名
            value: 实际值
            rules: 验证规则字典
        
        Raises:
            ValueError: 超出范围
        """
        # TODO: 检查 min/max（数字类型）
        # TODO: 检查 min_length/max_length（字符串/列表类型）
        pass


def validated(validator):
    """装饰器：自动验证函数参数。
    
    用法:
        @validated(my_validator)
        def register_user(name, age):
            ...
    
    Args:
        validator: ParamValidator 实例
    
    Returns:
        装饰器函数
    """
    # TODO: 实现装饰器，在调用目标函数前先 validate 参数
    pass


# ===== 测试 =====
if __name__ == "__main__":
    validator = ParamValidator()
    validator.add("age", type=int, min=0, max=150)
    validator.add("name", type=str, min_length=1, max_length=50)
    validator.add("role", type=str, choices=["admin", "user", "guest"])
    
    # 正常情况
    try:
        validator.validate(age=25, name="Alice", role="admin")
        print("✅ 验证通过")
    except (ValueError, TypeError) as e:
        print(f"❌ {e}")
    
    # 异常情况
    try:
        validator.validate(age=-1, name="", role="superadmin")
        print("✅ 验证通过")
    except (ValueError, TypeError) as e:
        print(f"❌ {e}")
