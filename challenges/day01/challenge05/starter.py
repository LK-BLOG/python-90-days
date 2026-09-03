# -*- coding: utf-8 -*-
# 挑战五(Boss)：SQL查询构建器

def where_clause(column, op, value):
    """构建安全的WHERE条件片段"""
    # TODO: 处理 =, !=, >, <, >=, <=, LIKE, IN, BETWEEN
    # IN 需要生成 (?,?,?) 格式
    # BETWEEN 需要两个参数
    pass


def build_query(table, columns="*", where=None, order_by=None,
                limit=None, offset=None, group_by=None, having=None):
    """构建SELECT查询，返回 (sql, params)"""
    # TODO: 构建各部分并拼接
    pass


def build_insert(table, **data):
    """构建INSERT语句"""
    # TODO
    pass


def build_update(table, where, **set_values):
    """构建UPDATE语句"""
    # TODO
    pass


def build_delete(table, **conditions):
    """构建DELETE语句"""
    # TODO
    pass


if __name__ == "__main__":
    sql, params = build_query("users", columns=["name", "email"],
        where={"age": (">", 18), "status": ("=", "active")},
        order_by="name", limit=10)
    print(f"SQL: {sql}")
    print(f"Params: {params}")

    sql, params = build_insert("users", name="张三", age=25)
    print(f"\nSQL: {sql}")
    print(f"Params: {params}")

    sql, params = build_update("users", {"id": 1}, name="李四", age=30)
    print(f"\nSQL: {sql}")
    print(f"Params: {params}")

    sql, params = build_delete("users", id=1)
    print(f"\nSQL: {sql}")
    print(f"Params: {params}")
