# Day 1 挑战五：简单文本表格
# 难度：★★★★★


def format_table(*headers, rows):
    """把表头和二维数据格式化成简单文本表格。

    示例：
        format_table(
            "姓名", "年龄", "城市",
            rows=[("Alice", 25, "北京"), ("Bob", 30, "上海")]
        )

    返回：
        姓名 | 年龄 | 城市
        Alice | 25 | 北京
        Bob | 30 | 上海
    """
    lines = []

    # TODO：先把 headers 用 " | " 连成第一行，加入 lines。
    # TODO：遍历 rows；每一行先把数字转成字符串，再用 " | " 连起来。
    # TODO：最后 return "\n".join(lines)
    pass


if __name__ == "__main__":
    table = format_table(
        "姓名", "年龄", "城市",
        rows=[("Alice", 25, "北京"), ("Bob", 30, "上海")],
    )
    print(table)
