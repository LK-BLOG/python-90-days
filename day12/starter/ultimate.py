# Day 12 - Ultimate: 包开发终极挑战
# 难度: ⭐⭐⭐⭐⭐
#
# 要求: 设计一个完整的 CLI 工具包结构，模拟真实项目
# 参考 ultimate_challenge.md

"""
CLI 工具包终极挑战 — 构建一个完整的命令行工具包

模拟: 类似 click 的 CLI 框架核心

包结构:
    cli_toolkit/
        __init__.py
        core.py          -> 核心 CLI 类
        commands.py      -> 命令定义
        decorators.py    -> 装饰器（@option, @argument）
        exceptions.py    -> 自定义异常
        utils.py         -> 工具函数
"""

from dataclasses import dataclass, field
from typing import Callable, Any


# ===== exceptions 模拟 =====
class CLIError(Exception):
    """CLI 基础错误"""
    pass


class CommandNotFoundError(CLIError):
    """命令未找到"""
    pass


class ArgumentError(CLIError):
    """参数错误"""
    pass


class ValidationError(CLIError):
    """验证错误"""
    pass


# ===== decorators 模拟 =====

@dataclass
class Option:
    """命令行选项"""
    name: str
    type_: type = str
    required: bool = False
    default: Any = None
    help: str = ""


@dataclass
class Argument:
    """命令行位置参数"""
    name: str
    type_: type = str
    required: bool = True


def command(name: str = "", help: str = ""):
    """命令装饰器

    用法:
        @command("greet", help="打招呼")
        def greet(name: str):
            print(f"Hello, {name}!")
    """
    def decorator(func: Callable) -> Callable:
        # TODO: 将元信息绑定到函数上（如 func.__command_name__）
        pass
    return decorator


def option(name: str, **kwargs):
    """选项装饰器"""
    def decorator(func: Callable) -> Callable:
        # TODO: 将 Option 追加到函数的 __options__ 列表
        pass
    return decorator


def argument(name: str, **kwargs):
    """位置参数装饰器"""
    def decorator(func: Callable) -> Callable:
        # TODO: 将 Argument 追加到函数的 __arguments__ 列表
        pass
    return decorator


# ===== core 模拟 =====

@dataclass
class Command:
    """命令对象

    Attributes:
        name: 命令名
        func: 命令处理函数
        help: 帮助信息
        options: 选项列表
        arguments: 参数列表
    """
    name: str
    func: Callable
    help: str = ""
    options: list = field(default_factory=list)
    arguments: list = field(default_factory=list)


class CLI:
    """CLI 核心类 — 管理命令和调度"""

    def __init__(self, name: str, version: str = "0.1.0"):
        # TODO: 初始化命令字典、name、version
        pass

    def register(self, command: Command) -> None:
        """注册命令"""
        # TODO: 检查重复 -> 注册到字典
        pass

    def parse_args(self, args: list[str]) -> tuple[str, dict]:
        """解析命令行参数

        Args:
            args: sys.argv[1:] 格式的参数列表

        Returns:
            (command_name, {选项和参数的字典})

        Raises:
            CommandNotFoundError: 命令不存在
            ArgumentError: 参数不足
        """
        # TODO: 提取命令名 -> 解析选项 -> 解析参数
        pass

    def execute(self, args: list[str]) -> Any:
        """执行命令

        Args:
            args: 命令行参数

        Returns:
            命令函数的返回值
        """
        # TODO: parse_args -> 查找命令 -> 调用命令函数
        pass

    def print_help(self) -> None:
        """打印帮助信息"""
        # TODO: 遍历命令，打印名称和帮助
        pass


# ===== 使用示例 =====
@command("greet", help="向用户打招呼")
@argument("name", type_=str)
@option("loud", type_=bool, default=False, help="大声说")
def greet(name: str, loud: bool = False):
    """Greet a user."""
    msg = f"Hello, {name}!"
    print(msg.upper() if loud else msg)


@command("add", help="两数相加")
@argument("a", type_=int)
@argument("b", type_=int)
def add(a: int, b: int):
    """Add two numbers."""
    print(f"{a} + {b} = {a + b}")


# ---- 测试 ----
if __name__ == "__main__":
    print("=== CLI 工具包终极挑战 ===")

    cli = CLI("mycli", version="1.0.0")
    cli.register(Command("greet", greet, "向用户打招呼"))
    cli.register(Command("add", add, "两数相加"))

    # 测试帮助
    cli.print_help()

    # 测试执行
    # cli.execute(["greet", "--name", "World"])
    # cli.execute(["add", "2", "3"])

    print("✅ Ultimate 完成")
