# 挑战五(Boss)：SQL查询构建器

## 难度
★★★★★

## 目标
用函数参数构建灵活、安全的SQL查询语句。

## 背景
SQL注入是Web安全第一大威胁。你需要构建一个安全的SQL构建器。

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
1. ✅ SELECT/INSERT/UPDATE/DELETE正确
2. ✅ WHERE支持多种运算符
3. ✅ 参数绑定用占位符
4. ✅ JOIN支持
5. ✅ UNION组合查询
