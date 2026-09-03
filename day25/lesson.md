# Day 25 课程：Debug + 测试

## 模块一：Debug 思维

### 1.1 二分法定位

当你知道 Bug 在某个范围内，用二分法缩小范围：

```python
def binary_search_bug(items, is_bug):
    """二分法定位 Bug"""
    low, high = 0, len(items) - 1
    
    while low <= high:
        mid = (low + high) // 2
        result = is_bug(items[mid])
        
        if result == "bug":
            high = mid - 1
        elif result == "ok":
            low = mid + 1
        else:
            # result == "exact" 或边界情况
            return mid
    
    return low  # 返回可能的位置

# 实际使用：在数据中找到问题点
data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# 假设从 index 7 开始数据有问题
for i, v in enumerate(data):
    print(f"index {i}: value {v}")
```

**关键原则：**
- 先确定问题范围
- 每次排除一半
- 打印关键点验证

### 1.2 print 调试

```python
# 基础 print
def process_data(data):
    print(f"[DEBUG] input: {data}")  # 查看输入
    
    result = []
    for item in data:
        print(f"[DEBUG] processing item: {item}")  # 查看循环
        processed = item * 2
        print(f"[DEBUG] result: {processed}")  # 查看结果
        result.append(processed)
    
    print(f"[DEBUG] output: {result}")  # 查看输出
    return result

# 带变量名的 print（Python 3.8+ f-string）
x = 42
print(f"{x=}")  # 输出: x=42

# 打印调用栈
import traceback
def deep_function():
    print("[DEBUG] 调用栈:")
    traceback.print_stack()
```

### 1.3 logging 模块

```python
import logging

# 基础配置
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='app.log'
)

# 创建 logger
logger = logging.getLogger(__name__)

def divide(a, b):
    logger.debug(f"计算: {a} / {b}")
    
    if b == 0:
        logger.error("除数不能为零！")
        raise ValueError("除数不能为零")
    
    result = a / b
    logger.info(f"结果: {result}")
    return result

# 日志级别
logger.debug("调试信息")      # 10
logger.info("普通信息")       # 20
logger.warning("警告")        # 30
logger.error("错误")          # 40
logger.critical("严重错误")   # 50

# 带异常的 logging
try:
    result = divide(10, 0)
except ValueError:
    logger.exception("发生异常")  # 自动包含堆栈信息
```

**logging vs print：**
- print：临时调试，容易忘记删除
- logging：可控制级别，可输出到文件，生产环境必备

---

## 模块二：pdb 调试器

### 2.1 基础用法

```python
# 方法1：在代码中插入断点
def buggy_function():
    x = 1
    y = 2
    breakpoint()  # Python 3.7+
    z = x + y
    return z

# 方法2：命令行启动
# python -m pdb script.py

# 方法3：异常后启动
# python -m pdb -c continue script.py
```

### 2.2 pdb 常用命令

```
l(ist)      - 显示当前代码
n(ext)      - 执行下一行
s(tep)      - 进入函数调用
c(ontinue)  - 继续执行到下一个断点
p(rint)     - 打印变量: p variable
w(here)     - 显示调用栈
b(reak)     - 设置断点: b 10
tbreak      - 临时断点
r(eturn)    - 执行到函数返回
q(uit)      - 退出调试器
h(elp)      - 帮助
```

### 2.3 条件断点

```python
# 在 pdb 中设置条件断点
# b 10, x > 100  # 当 x > 100 时在第10行中断

# 代码中使用
import pdb

def process_items(items):
    for i, item in enumerate(items):
        if item < 0:  # 只在负数时中断
            pdb.set_trace()
        process(item)
```

### 2.4 使用 icecream 进行调试

```python
# icecream 是 print 调试的增强版
# pip install icecream
from icecream import ic

def add(a, b):
    ic(a, b)  # 自动打印变量名和值
    result = a + b
    ic(result)
    return result

# 输出:
# ic| a: 5
# ic| b: 3
# ic| result: 8
```

---

## 模块三：assert 断言

### 3.1 基础用法

```python
def calculate_average(numbers):
    """计算平均值"""
    assert len(numbers) > 0, "列表不能为空"
    
    total = sum(numbers)
    average = total / len(numbers)
    
    assert isinstance(average, float), "结果应为浮点数"
    assert 0 <= average <= max(numbers), "平均值应在范围内"
    
    return average

# 测试
print(calculate_average([1, 2, 3, 4, 5]))  # 3.0

# 失败的 assert 会抛出 AssertionError
# calculate_average([])  # AssertionError: 列表不能为空
```

### 3.2 assert vs 异常

```python
# assert 用于开发时的"不应该发生"的情况
# 异常用于预期的错误情况

# ✅ 正确：assert 检查内部逻辑
def process_data(data):
    assert data is not None, "data 不应为 None"
    assert isinstance(data, list), "data 应为列表"
    # ... 处理逻辑

# ✅ 正确：异常处理预期错误
def divide(a, b):
    if b == 0:
        raise ValueError("除数不能为零")
    return a / b

# ❌ 错误：用 assert 处理用户输入
def get_age(input_str):
    # 不要用 assert！应该用异常
    assert input_str.isdigit(), "年龄必须是数字"  # ❌
    return int(input_str)
```

### 3.3 最佳实践

```python
# 1. assert 的消息要有信息量
assert x > 0, f"x 必须为正数，当前值: {x}"

# 2. 不要用 assert 验证数据（会被 -O 优化掉）
# 始终使用 raise 验证外部数据
def process_user_input(data):
    if not data:
        raise ValueError("数据不能为空")

# 3. 复杂条件拆分
assert (age >= 0 and age <= 150), f"年龄不合理: {age}"

# 4. 自定义断言函数
def assert_lists_equal(list1, list2):
    assert len(list1) == len(list2), f"长度不同: {len(list1)} vs {len(list2)}"
    for i, (a, b) in enumerate(zip(list1, list2)):
        assert a == b, f"索引 {i} 不同: {a} vs {b}"
```

---

## 模块四：unittest 深入

### 4.1 基础结构

```python
import unittest

class TestCalculator(unittest.TestCase):
    """计算器测试"""
    
    def setUp(self):
        """每个测试方法前执行"""
        self.calc = Calculator()
    
    def tearDown(self):
        """每个测试方法后执行"""
        pass
    
    def test_add(self):
        """测试加法"""
        result = self.calc.add(2, 3)
        self.assertEqual(result, 5)
    
    def test_divide(self):
        """测试除法"""
        result = self.calc.divide(10, 2)
        self.assertEqual(result, 5.0)
    
    def test_divide_by_zero(self):
        """测试除以零"""
        with self.assertRaises(ValueError):
            self.calc.divide(10, 0)

if __name__ == "__main__":
    unittest.main()
```

### 4.2 setUp / tearDown

```python
import tempfile
import os

class TestFileManager(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """整个测试类只执行一次"""
        cls.temp_dir = tempfile.mkdtemp()
    
    @classmethod
    def tearDownClass(cls):
        """整个测试类结束后执行"""
        import shutil
        shutil.rmtree(cls.temp_dir)
    
    def setUp(self):
        """每个测试方法前执行"""
        self.file_path = os.path.join(self.temp_dir, "test.txt")
        with open(self.file_path, "w") as f:
            f.write("initial content")
    
    def tearDown(self):
        """每个测试方法后执行"""
        if os.path.exists(self.file_path):
            os.remove(self.file_path)
    
    def test_read_file(self):
        with open(self.file_path) as f:
            content = f.read()
        self.assertEqual(content, "initial content")
```

### 4.3 Mock 和 patch

```python
from unittest.mock import Mock, patch, MagicMock
import requests

class TestAPIClient(unittest.TestCase):
    
    def test_mock_response(self):
        """Mock 一个对象"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"name": "test"}
        
        self.assertEqual(mock_response.status_code, 200)
        self.assertEqual(mock_response.json(), {"name": "test"})
    
    @patch('requests.get')
    def test_api_call(self, mock_get):
        """Mock requests.get"""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"users": []}
        
        result = fetch_users()
        
        mock_get.assert_called_once_with("https://api.example.com/users")
        self.assertEqual(result, {"users": []})
    
    @patch('os.path.exists')
    def test_file_check(self, mock_exists):
        """Mock 文件系统"""
        mock_exists.return_value = True
        
        result = check_file("/some/path")
        
        self.assertTrue(result)
        mock_exists.assert_called_once_with("/some/path")
```

### 4.4 参数化测试

```python
# unittest 没有原生参数化，用 subTest
class TestMath(unittest.TestCase):
    
    def test_addition(self):
        test_cases = [
            (1, 2, 3),
            (0, 0, 0),
            (-1, 1, 0),
            (100, 200, 300),
        ]
        
        for a, b, expected in test_cases:
            with self.subTest(a=a, b=b):
                result = add(a, b)
                self.assertEqual(result, expected)
```

---

## 模块五：pytest 基础

### 5.1 基础测试

```python
# test_math.py
def add(a, b):
    return a + b

def test_add_positive():
    assert add(2, 3) == 5

def test_add_negative():
    assert add(-1, -1) == -2

def test_add_zero():
    assert add(0, 5) == 5

# 运行: pytest test_math.py -v
```

### 5.2 fixture

```python
import pytest

@pytest.fixture
def sample_data():
    """提供测试数据"""
    return {"users": [{"name": "Alice"}, {"name": "Bob"}]}

@pytest.fixture
def temp_file(tmp_path):
    """提供临时文件"""
    file = tmp_path / "test.txt"
    file.write_text("hello")
    return file

def test_process_data(sample_data):
    result = process(sample_data)
    assert len(result["users"]) == 2

def test_read_file(temp_file):
    content = temp_file.read_text()
    assert content == "hello"

# fixture 作用域
@pytest.fixture(scope="session")
def db_connection():
    """整个测试会话只创建一次"""
    conn = create_connection()
    yield conn
    conn.close()

@pytest.fixture(scope="module")
def expensive_computation():
    """每个模块只执行一次"""
    return compute_heavy_thing()
```

### 5.3 conftest.py

```python
# conftest.py - 共享的 fixtures
import pytest

@pytest.fixture
def api_client():
    returnAPIClient(base_url="http://localhost:8000")

@pytest.fixture
def auth_token():
    return "test-token-12345"

# 自定义标记
def pytest_configure(config):
    config.addinivalue_line("markers", "slow: 慢速测试")
    config.addinivalue_line("markers", "integration: 集成测试")
```

### 5.4 conftest 和标记

```python
import pytest

@pytest.mark.slow
def test_large_dataset():
    """标记为慢速测试"""
    data = list(range(1000000))
    result = process(data)
    assert len(result) > 0

@pytest.mark.integration
def test_full_workflow():
    """集成测试"""
    pass

# 跳过测试
@pytest.mark.skip(reason="暂时跳过")
def test_not_ready():
    pass

@pytest.mark.skipif(
    sys.version_info < (3, 10),
    reason="需要 Python 3.10+"
)
def test_new_feature():
    pass

# 预期失败
@pytest.mark.xfail(reason="已知 Bug")
def test_known_bug():
    assert False
```

### 5.5 parametrize 参数化

```python
import pytest

@pytest.mark.parametrize("input_val,expected", [
    (1, 2),
    (2, 4),
    (3, 6),
    (0, 0),
    (-1, -2),
])
def test_double(input_val, expected):
    assert double(input_val) == expected

# 多参数
@pytest.mark.parametrize("a,b,expected", [
    (1, 2, 3),
    (0, 0, 0),
    (-1, 1, 0),
])
def test_add(a, b, expected):
    assert add(a, b) == expected

# 组合参数
@pytest.mark.parametrize("x", [1, 2, 3])
@pytest.mark.parametrize("y", [10, 20])
def test_multiply(x, y):
    assert multiply(x, y) == x * y
```

### 5.6 异常测试

```python
def test_raises_exception():
    with pytest.raises(ValueError, match="不能为零"):
        divide(10, 0)

def test_raises_type_error():
    with pytest.raises(TypeError):
        add("a", 1)
```

### 5.7 常用 pytest 插件

```bash
# 安装插件
pip install pytest-cov      # 覆盖率
pip install pytest-xdist     # 并行测试
pip install pytest-mock      # Mock 增强
pip install pytest-randomly  # 随机顺序
pip install pytest-timeout   # 超时控制

# 使用
pytest --cov=src --cov-report=html  # 覆盖率
pytest -n 4                          # 4 个进程并行
pytest --timeout=30                  # 每个测试最多 30 秒
pytest --randomly-seed=12345         # 固定随机种子
```

---

## 模块六：测试覆盖率

### 6.1 coverage.py 使用

```bash
# 安装
pip install coverage

# 运行并收集覆盖率
coverage run -m pytest tests/

# 生成报告
coverage report                    # 终端报告
coverage html                      # HTML 报告
coverage xml                       # XML 报告（CI 用）

# 配置 .coveragerc
[run]
source = src
omit = */tests/*, */migrations/*

[report]
fail_under = 80
show_missing = true
exclude_lines =
    pragma: no cover
    def __repr__
    if __name__ == .__main__
    raise NotImplementedError
```

### 6.2 覆盖率目标

```
语句覆盖率：> 80%（必须）
分支覆盖率：> 70%（推荐）
函数覆盖率：100%（每个函数至少调用一次）
```

### 6.3 pytest-cov 集成

```bash
# 运行测试并生成覆盖率
pytest --cov=myproject tests/
pytest --cov=myproject --cov-report=html tests/

# 最低覆盖率要求
pytest --cov=myproject --cov-fail-under=80 tests/
```

---

## 模块七：TDD 基础

### 7.1 红-绿-重构 循环

```python
# 1. 红：先写失败的测试
def test_add():
    assert add(2, 3) == 5  # 失败！add 不存在

# 2. 绿：写最少的代码让测试通过
def add(a, b):
    return 2 + 3  # 硬编码，但测试通过

# 3. 重构：改进代码
def add(a, b):
    return a + b  # 正确实现
```

### 7.2 TDD 示例：栈

```python
# 步骤 1：写测试
def test_empty_stack():
    stack = Stack()
    assert stack.is_empty()
    assert len(stack) == 0

def test_push():
    stack = Stack()
    stack.push(1)
    assert not stack.is_empty()
    assert len(stack) == 1

def test_pop():
    stack = Stack()
    stack.push(1)
    stack.push(2)
    assert stack.pop() == 2
    assert stack.pop() == 1
    assert stack.is_empty()

def test_peek():
    stack = Stack()
    stack.push(1)
    assert stack.peek() == 1
    assert len(stack) == 1

# 步骤 2：实现（每次只让一个测试通过）
class Stack:
    def __init__(self):
        self._items = []
    
    def is_empty(self):
        return len(self._items) == 0
    
    def push(self, item):
        self._items.append(item)
    
    def pop(self):
        return self._items.pop()
    
    def peek(self):
        return self._items[-1]
    
    def __len__(self):
        return len(self._items)
```

---

## 模块八：测试最佳实践

### 8.1 测试命名

```python
# 好的命名：描述测试什么
def test_user_registration_with_valid_email_succeeds():
    pass

def test_user_registration_with_duplicate_email_raises_error():
    pass

def test_user_registration_with_invalid_email_raises_value_error():
    pass

# 不好的命名
def test_register():  # ❌ 太模糊
    pass
```

### 8.2 AAA 模式（Arrange-Act-Assert）

```python
def test_calculate_total():
    # Arrange（准备）
    items = [
        {"name": "apple", "price": 1.0},
        {"name": "banana", "price": 0.5},
    ]
    tax_rate = 0.1
    
    # Act（执行）
    total = calculate_total(items, tax_rate)
    
    # Assert（断言）
    expected = 1.65  # (1.0 + 0.5) * 1.1
    assert abs(total - expected) < 0.01
```

### 8.3 测试目录结构

```
tests/
├── conftest.py
├── unit/
│   ├── test_models.py
│   ├── test_services.py
│   └── test_utils.py
├── integration/
│   ├── test_api.py
│   └── test_database.py
└── e2e/
    └── test_workflow.py
```

---

## 常见错误汇总

| 错误 | 原因 | 解决 |
|------|------|------|
| 测试不运行 | 文件名不是 test_*.py | 确保文件名以 test 开头 |
| fixture 找不到 | 不在 conftest.py 或同目录 | 把 fixture 放 conftest.py |
| assert 失败信息不清楚 | 没写消息 | `assert x == 5, f"期望 5，得到 {x}"` |
| mock 没生效 | patch 路径错误 | patch 使用者所在模块的路径 |
| 覆盖率低 | 只测了正常路径 | 添加边界和异常测试 |
