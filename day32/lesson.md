# Day 32 课程：测试体系

## 第一部分：pytest 深入

### 1.1 fixture 基础

import pytest

@pytest.fixture
def sample_data():
    return {'users': [{'name': 'Alice', 'age': 30}, {'name': 'Bob', 'age': 25}]}

@pytest.fixture
def db_connection():
    conn = create_connection()
    yield conn          # yield 之前是 setup
    conn.close()        # yield 之后是 teardown

def test_get_users(sample_data, db_connection):
    users = sample_data['users']
    assert len(users) == 2

### 1.2 conftest.py — 共享 fixture

# tests/conftest.py
@pytest.fixture
def api_client():
    from fastapi.testclient import TestClient
    from my_app import app
    return TestClient(app)

conftest.py 中的 fixture 自动被同级及子目录的测试文件发现。

### 1.3 parametrize — 参数化测试

@pytest.mark.parametrize('input_val,expected', [
    ('hello', 5),
    ('', 0),
    ('hello world', 11),
])
def test_word_count(input_val, expected):
    assert word_count(input_val) == expected

### 1.4 mark — 标记测试

@pytest.mark.slow
def test_heavy_computation():
    ...

@pytest.mark.skip(reason='Not ready')
def test_not_ready():
    ...

# 运行: pytest -m "not slow"

### 1.5 fixture 作用域

@pytest.fixture(scope='function')  # 每个测试函数
def per_test(): ...

@pytest.fixture(scope='class')
def per_class(): ...

@pytest.fixture(scope='module')
def per_module(): ...

@pytest.fixture(scope='session')
def per_session(): ...

---

## 第二部分：Mock 和测试替身

### 2.1 unittest.mock

from unittest.mock import Mock, MagicMock, patch, AsyncMock

# Mock 对象
mock_user = Mock()
mock_user.get_name.return_value = 'Alice'
mock_user.get_name.assert_called_once()

# patch 装饰器
@patch('my_module.requests.get')
def test_fetch_data(mock_get):
    mock_get.return_value.json.return_value = {'key': 'value'}
    result = fetch_data('http://api.com')
    assert result == {'key': 'value'}

# AsyncMock
@patch('my_module.async_fetch', new_callable=AsyncMock)
async def test_async(mock_fetch):
    mock_fetch.return_value = {'data': 1}
    result = await async_fetch('url')

### 2.2 测试替身类型

# Dummy — 不用的数据
# Stub — 返回固定值
# Spy — 记录调用，调用真实方法
# Mock — 完全模拟行为
# Fake — 简化的真实实现（如内存数据库）

---

## 第三部分：测试覆盖率

pip install pytest-cov

pytest --cov=my_package --cov-report=html
pytest --cov=my_package --cov-fail-under=80

---

## 第四部分：TDD 红绿重构

Red   -> 写失败的测试
Green -> 写最少代码让测试通过
Refactor -> 重构代码

---

## 第五部分：测试金字塔

        /  E2E  \           <- 少量，慢
       / Integration \      <- 适量
    /   Unit Tests    \     <- 大量，快

比例：70% 单元 / 20% 集成 / 10% E2E

## 常见错误
1. 测试依赖执行顺序 -> 每个测试独立
2. Mock 太多 -> 测的是 Mock 不是逻辑
3. 不测边界情况
4. fixture 泄漏

## 动手练习
1. 用 parametrize 写 5 个测试
2. 用 Mock 模拟外部 API
3. 配置 pytest-cov 达到 80%
4. TDD 实现 Stack 类
