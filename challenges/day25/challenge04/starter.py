"""
Challenge 04: 测试生成器 - TestGen
"""
import ast
import inspect
from typing import Any, Callable, Dict, List, Optional, get_type_hints
from pathlib import Path
import textwrap


class FunctionAnalyzer:
    """函数分析器"""
    
    def __init__(self, func: Callable):
        self.func = func
        self.name = func.__name__
        self.module = func.__module__
        self.signature = inspect.signature(func)
        self.source = None
        selfast_node = None
        
        # 尝试获取源代码
        try:
            self.source = inspect.getsource(func)
            self.ast_node = ast.parse(textwrap.dedent(self.source))
        except (OSError, SyntaxError):
            pass
    
    def get_parameters(self) -> List[Dict[str, Any]]:
        """获取参数信息
        
        TODO: 实现
        - 解析函数参数
        - 提取类型注解
        - 获取默认值
        """
        params = []
        for name, param in self.signature.parameters.items():
            params.append({
                'name': name,
                'kind': param.kind,
                'default': param.default,
                'annotation': param.annotation,
                'has_default': param.default != inspect.Parameter.empty,
                'has_annotation': param.annotation != inspect.Parameter.empty,
            })
        return params
    
    def get_return_type(self) -> Optional[type]:
        """获取返回类型"""
        if self.signature.return_annotation != inspect.Signature.empty:
            return self.signature.return_annotation
        return None


class TestCaseGenerator:
    """测试用例生成器"""
    
    def __init__(self):
        self.test_cases = []
    
    def generate_from_function(self, func: Callable) -> str:
        """从函数生成测试代码
        
        TODO: 实现
        - 分析函数
        - 生成测试用例
        - 输出 pytest 格式
        """
        analyzer = FunctionAnalyzer(func)
        params = analyzer.get_parameters()
        
        test_code = f"def test_{func.__name__}():\n"
        test_code += f"    \"\"\"测试 {func.__name__}\"\"\"\n"
        
        # TODO: 生成具体测试代码
        
        return test_code
    
    def generate_boundary_tests(self, func: Callable) -> str:
        """生成边界测试
        
        TODO: 实现
        - 分析参数类型
        - 生成边界值
        - 处理空值/None
        """
        pass
    
    def generate_type_tests(self, func: Callable) -> str:
        """生成类型测试
        
        TODO: 实现
        - 根据类型注解生成测试
        - 处理复杂类型
        """
        pass
    
    def generate_exception_tests(self, func: Callable) -> str:
        """生成异常测试
        
        TODO: 实现
        - 检查函数可能的异常
        - 生成异常测试用例
        """
        pass


def generate_test_file(module_path: str, output_path: str = None) -> str:
    """从模块生成测试文件
    
    TODO: 实现
    - 解析模块
    - 找到所有函数/类
    - 为每个生成测试
    """
    pass


def generate_test_for_class(cls: type) -> str:
    """为类生成测试代码
    
    TODO: 实现
    - 分析类的方法
    - 生成 setUp
    - 为每个方法生成测试
    """
    pass


if __name__ == "__main__":
    # 示例函数
    def add(a: int, b: int) -> int:
        """两数相加"""
        return a + b
    
    def divide(a: float, b: float) -> float:
        """除法"""
        if b == 0:
            raise ValueError("除数不能为零")
        return a / b
    
    def process_items(items: list) -> list:
        """处理列表"""
        return [x * 2 for x in items if isinstance(x, (int, float))]
    
    # 生成测试
    generator = TestCaseGenerator()
    
    print("=== 为 add 生成测试 ===")
    print(generator.generate_from_function(add))
    
    print("\n=== 为 divide 生成测试 ===")
    print(generator.generate_from_function(divide))
    
    print("\n=== 为 process_items 生成测试 ===")
    print(generator.generate_from_function(process_items))
