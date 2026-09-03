# Day 3: Boss挑战 — 计数器工厂系统

## 目标
用闭包构建灵活的计数器工厂。

## 功能要求
```python
def make_counter(strategy="linear", start=0, step=1, max_val=None):
    """根据不同策略生成计数器"""
    # strategy: linear, exponential, bounded, cycling
```

## 验收标准
1. ✅ linear: 0, 1, 2, 3...
2. ✅ exponential: 1, 2, 4, 8...
3. ✅ bounded: 超过max_val报错
4. ✅ cycling: 达到max_val后从start重新开始
