# Day 25 - Challenge 4: 测试生成器
# 难度: ⭐⭐⭐⭐
# 分析函数签名，自动生成边界测试、类型测试，输出 pytest 格式

import ast
import inspect
import textwrap
from dataclasses import dataclass, field
from typing import Any


@dataclass
class ParameterInfo:
    """函数参数信息"""
    name: str
    annotation: str
    default: Any = None
    has_default: bool = False


@dataclass
class FunctionInfo:
    """函数分析信息"""
    name: str
    docstring: str = ""
    parameters: list[ParameterInfo] = field(default_factory=list)
    return_annotation: str = "None"
    source_code: str = ""


class TestGenerator:
    """测试代码自动生成器

    分析 Python 函数签名，自动生成 pytest 格式的测试代码。
    """

    def __init__(self):
        # TODO: 定义类型 -> 测试值的映射
        self._type_test_values: dict[str, list] = {}

    def analyze_function(self, func: callable) -> FunctionInfo:
        """分析一个函数的签名

        Args:
            func: 目标函数

        Returns:
            FunctionInfo 对象
        """
        # TODO: 使用 inspect 获取参数签名
        # TODO: 提取类型注解、默认值
        # TODO: 获取源代码
        ...

    def generate_boundary_tests(self, info: FunctionInfo) -> str:
        """生成边界测试用例

        根据参数类型自动生成边界值：
        - int: 0, -1, 1, MAX_INT
        - str: "", "a", 长字符串
        - list: [], [1], [1,2,3]
        - float: 0.0, -1.0, 1e10

        Args:
            info: 函数分析信息

        Returns:
            pytest 测试代码字符串
        """
        # TODO: 为每个参数类型生成边界值
        # TODO: 组合生成多个测试用例
        ...

    def generate_type_tests(self, info: FunctionInfo) -> str:
        """生成类型测试用例（传入错误类型应报错）

        Args:
            info: 函数分析信息

        Returns:
            pytest 测试代码字符串
        """
        # TODO: 为每个参数生成错误类型的测试
        ...

    def generate_exception_tests(self, info: FunctionInfo) -> str:
        """根据 docstring 中的 Raises 信息生成异常测试

        Args:
            info: 函数分析信息

        Returns:
            pytest 测试代码字符串
        """
        # TODO: 解析 docstring 中的 Raises 描述
        # TODO: 生成 pytest.raises 测试
        ...

    def generate_all(self, func: callable) -> str:
        """为函数生成完整测试文件

        Args:
            func: 目标函数

        Returns:
            完整的 pytest 测试文件内容
        """
        # TODO: 调用所有生成器，组装为完整测试文件
        ...


# ==================== 示例函数（用于测试生成） ====================
def add(a: int, b: int) -> int:
    """两数相加

    Args:
        a: 第一个加数
        b: 第二个加数

    Returns:
        两数之和

    Raises:
        TypeError: 参数类型不是数字
    """
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("参数必须是数字")
    return a + b


# ==================== 测试 ====================
if __name__ == "__main__":
    gen = TestGenerator()
    test_code = gen.generate_all(add)
    print(test_code)
