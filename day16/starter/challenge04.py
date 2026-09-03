# Day 16 - Challenge 4: 可调用对象
# 难度: ⭐⭐⭐☆☆
#
# 要求: 实现 __call__ 创建可调用累加器
# 参考 challenge.md

"""
可调用对象挑战 — 让类实例可以像函数一样被调用

核心知识点:
- __call__: 使实例可调用
- 闭包 vs __call__ 的选择
- 函数式编程模式
"""

from typing import Callable, Any


class Accumulator:
    """可调用累加器 — 实例可以像函数一样调用

    Example:
        acc = Accumulator(0)
        acc(5)    # 返回 5, 内部值为 5
        acc(3)    # 返回 8, 内部值为 8
        acc.value # 8
    """

    def __init__(self, initial: float = 0, op: str = "add"):
        """初始化累加器

        Args:
            initial: 初始值
            op: 运算类型 ("add", "mul", "max", "min")
        """
        # TODO: 设置初始值和运算类型
        pass

    def __call__(self, value: float) -> float:
        """执行累加运算

        Args:
            value: 要累加的值

        Returns:
            运算后的当前值
        """
        # TODO: 根据 op 类型执行不同运算
        pass

    @property
    def value(self) -> float:
        """当前值"""
        return self._value

    def reset(self) -> None:
        """重置为初始值"""
        pass

    def __repr__(self) -> str:
        return f"Accumulator(value={self._value}, op={self._op!r})"


class RetryableFunction:
    """可重试的函数包装器 — __call__ + 异常处理

    Example:
        @RetryableFunction(max_retries=3)
        def unstable():
            import random
            if random.random() < 0.5:
                raise ConnectionError("timeout")
            return "success"

        result = unstable()  # 自动重试
    """

    def __init__(self, func: Callable = None, max_retries: int = 3,
                 delay: float = 0.1):
        self.func = func
        self.max_retries = max_retries
        self.delay = delay
        self.retry_count = 0

    def __call__(self, *args, **kwargs) -> Any:
        """调用函数，失败时自动重试

        Returns:
            函数返回值

        Raises:
            最后一次失败的异常
        """
        # TODO: 循环 max_retries 次
        # 成功则返回，失败则记录并继续
        pass

    def __repr__(self) -> str:
        return f"RetryableFunction(func={self.func.__name__ if self.func else None})"


class Pipeline:
    """函数管道 — 把多个函数串起来调用

    Example:
        pipe = Pipeline(
            lambda x: x.strip(),
            lambda x: x.lower(),
            lambda x: x.replace(" ", "_"),
        )
        pipe("  Hello World  ")  # "hello_world"
    """

    def __init__(self, *functions: Callable):
        self.functions = list(functions)

    def __call__(self, value: Any) -> Any:
        """依次执行管道中的函数"""
        # TODO: 用 reduce 或循环依次调用
        pass

    def __or__(self, other: Callable) -> "Pipeline":
        """支持 pipe1 | func 的链式写法"""
        # TODO: 返回新的 Pipeline（原函数 + other）
        pass

    def __repr__(self) -> str:
        names = [f.__name__ for f in self.functions]
        return f"Pipeline({' -> '.join(names)})"


# ---- 测试 ----
if __name__ == "__main__":
    print("=== 可调用对象测试 ===")

    # 累加器
    acc = Accumulator(0, "add")
    print(f"acc(10) = {acc(10)}")
    print(f"acc(5) = {acc(5)}")
    print(f"当前值: {acc.value}")

    # 乘法累加器
    mul_acc = Accumulator(1, "mul")
    print(f"mul(3) = {mul_acc(3)}")
    print(f"mul(4) = {mul_acc(4)}")

    # 管道
    pipe = Pipeline(
        lambda x: x.strip(),
        lambda x: x.lower(),
        lambda x: x.replace(" ", "_"),
    )
    print(f"管道: {pipe('  Hello World  ')}")

    print("✅ Challenge 04 完成")
