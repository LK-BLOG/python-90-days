# Day 2 挑战三：筛选物品
# 难度：★★★☆☆
# 目标：从列表中的字典筛选出符合条件的新列表。


def get_expensive_items(items, minimum_price):
    """返回价格大于等于 minimum_price 的物品。

    输入：
        items = [
            {'name': '药水', 'price': 30},
            {'name': '木剑', 'price': 50},
        ]
        minimum_price = 40

    返回：
        [{'name': '木剑', 'price': 50}]
    """
    result = []

    # TODO：遍历 items
    # TODO：读取 item['price']
    # TODO：符合条件时把 item append 到 result
    # TODO：返回 result
    pass


if __name__ == '__main__':
    bag = [
        {'name': '药水', 'price': 30},
        {'name': '木剑', 'price': 50},
        {'name': '盾牌', 'price': 80},
    ]
    print(get_expensive_items(bag, 50))
