# 挑战五(Boss)：多格式报告生成器

## 难度
★★★★★

## 目标
用函数参数构建支持多种输出格式的报告语句。

## 背景
同一份数据需要以不同格式展示。你需要构建一个安全的报告生成器。

## 功能要求

### 核心函数
```python
def build_query(table, columns="*", where=None, order_by=None,
                limit=None, offset=None, group_by=None, having=None)
```

### 辅助函数
```python
def build_insert(table, **data)
def build_update(table, where, **set_values)
def build_delete(table, **conditions)
def where_clause(column, op, value)
```

### 参数绑定
使用 `?` 占位符，返回 (sql_string, params_list)

## 示例
```python
sql, params = build_query("users", columns=["name"], where={"age": (">", 18)}, limit=10)
# "SELECT name FROM users WHERE age > ? LIMIT 10", [18]
```

## 验收标准
1. ✅ text/csv/markdown/html正确
2. ✅ 排序和统计正确
3. ✅ 参数设计灵活
4. ✅ show_total正确
5. ✅ 格式切换正确

