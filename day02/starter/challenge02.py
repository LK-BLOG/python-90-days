# Day 2 挑战二：添加和删除背包物品
# 难度：★★☆☆☆
# 目标：练习 append、remove 和列表返回值。


def add_item(items, item):
    """添加一个物品，并返回修改后的列表。"""
    # TODO：使用 append(item)
    # TODO：返回 items
    pass


def remove_item(items, item):
    """删除一个物品。

    如果物品不存在，不要让程序崩溃，直接返回原列表。
    """
    # TODO：先判断 item 是否在 items 中
    # TODO：存在时使用 remove(item)
    # TODO：返回 items
    pass


if __name__ == '__main__':
    bag = ['药水', '木剑']
    print(add_item(bag, '盾牌'))
    print(remove_item(bag, '药水'))
    print(remove_item(bag, '不存在的物品'))
