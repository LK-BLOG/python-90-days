# Day 1: Boss挑战 — SQL查询构建器

## 项目名称
**SQL Query Builder**

## 目标
用函数参数的灵活组合来构建安全、可读的SQL查询语句。

## 背景
在Web开发中，直接拼接SQL字符串既危险又容易出错。你需要实现一个函数式的SQL构建器，通过参数传递来安全地构建SQL。

## 功能要求

### 核心函数 `build_query()`
```python
def build_query(table, columns="*", where=None, order_by=None,
                limit=None, offset=None, group_by=None, having=None):
    """
    构建SELECT查询
    - table: 表名（必填，仅位置参数）
    - columns: 查询列，默认"*"
    - where: WHERE条件字典 {"列名": ("运算符", "值")}
    - order_by: 排序列
    - limit/offset: 分页
    - group_by/having: 分组
    """
```

### 辅助函数
1. `build_insert(table, **data)` — 构建INSERT语句
2. `build_update(table, where, **set_values)` — 构建UPDATE语句
3. `build_delete(table, **conditions)` — 构建DELETE语句
4. `where_clause(column, op, value)` — 安全的WHERE片段

### 参数绑定
使用 `?` 占位符，返回 (sql_string, params_list)

## 示例
```python
sql, params = build_query("users",
    columns=["name", "email"],
    where={"age": (">", 18), "status": ("=", "active")},
    order_by="name", limit=10)
# SELECT name, email FROM users WHERE age > ? AND status = ? ORDER BY name LIMIT 10
# params: [18, 'active']
```

## 验收标准
1. ✅ SELECT查询正确生成
2. ✅ WHERE支持多种运算符(=, !=, >, <, >=, <=, LIKE, IN, BETWEEN)
3. ✅ INSERT/UPDATE/DELETE正确生成
4. ✅ 参数绑定使用占位符
5. ✅ JOIN子句支持
6. ✅ 所有字符串值安全转义
7. ✅ 组合查询(UNION)支持
