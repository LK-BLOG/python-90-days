# Day 2 挑战五：背包管理器
# 难度：★★★★★
# 目标：综合列表、字典、for、append、remove、函数拆分。


def add_item(items, name, kind, price, count=1):
    """创建物品字典并加入背包。"""
    # TODO：创建 {'name': name, 'kind': kind, 'price': price, 'count': count}
    # TODO：加入 items 并返回 items
    WAIT_NOW={'name': name, 'kind': kind, 'price': price, 'count': count}
    items=items+[WAIT_NOW]
    return items


def find_item(items, name):
    """按名称查找第一个物品，找不到返回 None。"""
    # TODO：遍历 items，比较 item['name']
    for item in items:
        if item['name'] == name:
            return item
    return None


def remove_item_by_name(items, name):
    """按名称删除物品，成功返回 True，找不到返回 False。"""
    # TODO：先调用 find_item
    # TODO：找到后从 items 删除
    if find_item(items, name)==None:
        return False
    else:
        items.remove(find_item(items, name))
        bag=items
        return True

def print_inventory(items):
    """逐行打印背包内容。"""
    # TODO：遍历 items，打印名称、类型、价格、数量
    pass


if __name__ == '__main__':
    bag = []
    bag=add_item(bag, '治疗药水', '消耗品', 30, 2)
    bag=add_item(bag, '木剑', '武器', 50, 1)
    print_inventory(bag)
    print('找到：', find_item(bag, '木剑'))
    print('删除成功：', remove_item_by_name(bag, '治疗药水'))
