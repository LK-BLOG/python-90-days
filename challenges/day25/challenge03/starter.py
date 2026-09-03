"""
Challenge 03: Mock 模拟器 - MockMaster
"""
from typing import Any, Callable, Dict, List, Optional, Tuple
from collections import defaultdict
import functools


class CallRecord:
    """调用记录"""
    
    def __init__(self, args: tuple, kwargs: dict):
        self.args = args
        self.kwargs = kwargs
        self.timestamp = None  # 可选：记录时间戳
    
    def __repr__(self):
        return f"CallRecord(args={self.args}, kwargs={self.kwargs})"


class Mock:
    """Mock 对象"""
    
    def __init__(self, name: str = None, return_value: Any = None,
                 side_effect: Any = None):
        self.name = name
        self._return_value = return_value
        self._side_effect = side_effect
        self._calls: List[CallRecord] = []
        self._call_count = 0
        self._attributes: Dict[str, 'Mock'] = {}
    
    def __call__(self, *args, **kwargs):
        """模拟函数调用
        
        TODO: 实现
        - 记录调用
        - 处理 side_effect
        - 返回 return_value
        """
        pass
    
    def __getattr__(self, name: str) -> 'Mock':
        """支持属性访问
        
        TODO: 实现
        - 返回嵌套 Mock
        - 记录属性访问
        """
        pass
    
    @property
    def return_value(self) -> Any:
        """设置返回值"""
        return self._return_value
    
    @return_value.setter
    def return_value(self, value: Any):
        self._return_value = value
    
    @property
    def call_count(self) -> int:
        """调用次数"""
        return self._call_count
    
    @property
    def calls(self) -> List[CallRecord]:
        """调用记录"""
        return self._calls
    
    @property
    def called(self) -> bool:
        """是否被调用过"""
        return self._call_count > 0
    
    @property
    def call_args(self) -> Optional[Tuple[tuple, dict]]:
        """最后一次调用的参数"""
        if self._calls:
            last = self._calls[-1]
            return (last.args, last.kwargs)
        return None
    
    @property
    def call_args_list(self) -> List[Tuple[tuple, dict]]:
        """所有调用的参数"""
        return [(c.args, c.kwargs) for c in self._calls]
    
    def assert_called(self):
        """断言被调用过"""
        if not self.called:
            raise AssertionError(f"Mock {self.name} 未被调用")
    
    def assert_called_once(self):
        """断言只调用一次"""
        if self._call_count != 1:
            raise AssertionError(
                f"Mock {self.name} 被调用了 {self._call_count} 次，期望 1 次"
            )
    
    def assert_called_with(self, *args, **kwargs):
        """断言最后一次调用参数"""
        if not self._calls:
            raise AssertionError(f"Mock {self.name} 未被调用")
        
        last = self._calls[-1]
        if last.args != args or last.kwargs != kwargs:
            raise AssertionError(
                f"调用参数不匹配: 实际 {last.args}, {last.kwargs} "
                f"期望 {args}, {kwargs}"
            )
    
    def assert_called_once_with(self, *args, **kwargs):
        """断言只调用一次且参数匹配"""
        self.assert_called_once()
        self.assert_called_with(*args, **kwargs)
    
    def reset_mock(self):
        """重置 Mock"""
        self._calls.clear()
        self._call_count = 0
    
    def configure_mock(self, **kwargs):
        """配置 Mock"""
        for key, value in kwargs.items():
            setattr(self, key, value)


class patch:
    """上下文管理器/装饰器形式的 patch"""
    
    def __init__(self, target: str, **kwargs):
        self.target = target
        self.new = kwargs.get('new', Mock())
        self.kwargs = kwargs
        self._original = None
    
    def __enter__(self):
        # TODO: 实现 patch
        return self.new
    
    def __exit__(self, *args):
        # TODO: 恢复原始值
        pass
    
    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            with self:
                return func(*args, **kwargs)
        return wrapper


def test_mock_basic():
    """测试基础 Mock"""
    mock = Mock(return_value=42)
    
    result = mock()
    
    assert result == 42
    mock.assert_called_once()


def test_mock_calls():
    """测试调用记录"""
    mock = Mock()
    
    mock(1, 2, key="value")
    mock(3, 4)
    
    assert mock.call_count == 2
    assert len(mock.calls) == 2


def test_mock_side_effect():
    """测试 side_effect"""
    mock = Mock(side_effect=[1, 2, 3])
    
    assert mock() == 1
    assert mock() == 2
    assert mock() == 3


if __name__ == "__main__":
    print("Mock 模拟器测试")
    test_mock_basic()
    test_mock_calls()
    test_mock_side_effect()
    print("测试通过！")
